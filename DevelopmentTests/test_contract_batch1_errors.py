"""Contract audit batch 1 (2026-11-25): swallowed errors become visible.

Covers the production error log (SafeCallbacks.Record), the isolated
UI/ErrorProbe printer, the reputation contract that now throws, the reply
transport without format re-validation, and the five reason mappers that keep
raw text. Run from DevelopmentTests with Lupa 2.8 (see README environment).
"""
import re
import unittest
from pathlib import Path

import lupa.lua51 as lua51

MOD = Path(__file__).resolve().parents[1] / 'Mod'


def runtime():
    lua = lua51.LuaRuntime(unpack_returned_tuples=True)
    lua.globals().MOD_ROOT = str(MOD)
    lua.execute("""
      function include(name)
        local path=MOD_ROOT..'/'..name..'.lua'
        local f=io.open(path,'r');if not f then path=MOD_ROOT..'/UI/'..name..'.lua';f=assert(io.open(path,'r'))end
        local src=f:read('*a');f:close();assert(loadstring(src,name))()
      end
    """)
    return lua


class ErrorLog(unittest.TestCase):
    def test_record_dedupes_caps_and_never_changes_flow(self):
        lua = runtime()
        lua.execute("""
          include('SafeCallbacks');shared={}
          SPCSafeCallbacks.Record(shared,'A','boom\\nline2')
          SPCSafeCallbacks.Record(shared,'A','boom\\nline2')
          local log=shared.ErrorLog
          assert(log.seq==1 and #log.entries==1 and log.entries[1].count==2 and log.entries[1].text=='boom line2')
          for i=1,40 do SPCSafeCallbacks.Record(shared,'B',i)end
          assert(log.seq==41 and #log.entries==32 and log.entries[1].seq==10 and log.entries[32].text=='40')
          SPCSafeCallbacks.Record(shared,'C',string.rep('x',900))
          assert(#log.entries[32].text==400)
        """)

    def test_probe_prints_new_entries_once_and_resets_on_new_log(self):
        lua = runtime()
        lua.execute("""
          printed={}
          print=function(s)printed[#printed+1]=s end
          local handlers={}
          local function event()local e={};function e.Add(fn)handlers[#handlers+1]=fn end;return e end
          Events={LocalPlayerTurnBegin=event(),LocalPlayerTurnEnd=event(),GameCoreEventPublishComplete=event()}
          ExposedMembers={}
          include('ErrorProbe')
          local function fire()for _,h in ipairs(handlers)do h()end end
          fire();assert(#printed==0) -- no producer yet
          include('SafeCallbacks');ExposedMembers.SPC_P0={}
          SPCSafeCallbacks.Record(ExposedMembers.SPC_P0,'Store:commerce-tick','attempt to index nil')
          fire();fire()
          assert(#printed==1 and printed[1]=='[SPC][ERR] seq=1 label=Store:commerce-tick attempt to index nil',printed[1])
          SPCSafeCallbacks.Record(ExposedMembers.SPC_P0,'Store:commerce-tick','attempt to index nil')
          fire();assert(#printed==1) -- repeats only count
          ExposedMembers.SPC_P0={} -- new game/load
          SPCSafeCallbacks.Record(ExposedMembers.SPC_P0,'Commerce','x')
          fire();assert(#printed==2 and printed[2]:find('seq=1 label=Commerce x',1,true))
        """)

    def test_collector_allowlists_probe_lines(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('reader', MOD.parent / 'tools/read_expedition_trace.py')
        reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reader)
        line = '[SPC][ERR] seq=3 label=Reply:unit-action TEXT_BUDGET'
        self.assertEqual(reader.hd_line('Lua: ' + line), line)
        self.assertIsNone(reader.hd_line('[SPC][ERR] seq=x label=A b'))

    def test_production_never_refers_to_the_probe(self):
        hits = [p.name for p in MOD.rglob('*.lua') if p.name != 'ErrorProbe.lua' and 'ErrorProbe' in p.read_text(errors='replace')]
        self.assertEqual(hits, [])


class Contracts(unittest.TestCase):
    def test_non_isolated_reputation_violation_throws(self):
        lua = runtime()
        lua.execute("""
          include('CommerceModel')
          local ok,err=pcall(SPCCommerceModel.ReputationInput,{reputation={version=2}},nil,nil,nil)
          assert(not ok and tostring(err):find('COMMERCE_REPUTATION_INVALID'),tostring(err))
          assert(SPCCommerceModel.ReputationInput({},nil,nil,nil).status=='ABSENT')
          local iso=SPCCommerceModel.ReputationInput({reputation={version=2}},nil,{status='CHECK_FAILED'},nil)
          assert(iso.status=='SEVERE_LEAF')
        """)

    def test_reason_mappers_record_uncoded_errors(self):
        for name, label in (('Commerce', 'Commerce'), ('StandardizationEffects', 'Standardization'),
                            ('CrewProjects', 'Crew'), ('Restructuring', 'Restructuring'),
                            ('DevelopmentInvestment', 'DevelopmentInvestment')):
            src = (MOD / (name + '.lua')).read_text()
            body = re.search(r'local function code\((\w)\)\n(.*?)\n end', src, re.S)
            self.assertIsNotNone(body, name)
            self.assertIn("SPCSafeCallbacks.Record(shared,'%s'," % label, body.group(2), name)
        # Restructuring no longer treats an arbitrary upper-case word as a reason.
        lua = runtime()
        lua.execute("""
          shared={};include('SafeCallbacks')
          local src=assert(io.open(MOD_ROOT..'/Restructuring.lua')):read('*a')
          local body=src:match('local function code%(e%)\\n(.-)\\n end')
          code=assert(loadstring('return function(e)\\n'..body..'\\n end'))()
        """)
        lua.execute("""
          assert(code('x: REST_TARGET_CHANGED')=='REST_TARGET_CHANGED')
          assert(code('x: STORE_BUSY')=='STORE_BUSY')
          assert(code('attempt to index field NIL')=='REST_READ_FAILED')
          assert(shared.ErrorLog.entries[1].text=='attempt to index field NIL')
        """)


class Replies(unittest.TestCase):
    def setUp(self):
        self.lua = runtime()
        self.lua.execute("include('PlayerActionReplies')")

    def test_action_reply_budget_identity_and_throw_on_bad_payload(self):
        self.lua.execute("""
          local d=SPCPlayerActionReplies.New(1,'V','UNIT_ACTION')
          local p={Token='T',ReplyChannel='UNIT_ACTION',ReplyEpoch=1,Action='UNIT_ACTION_CONFIRM',UnitID=5}
          assert(d.Publish(0,p,'ok',{status='DONE'})==true)
          local q={Token='U',ReplyChannel='UNIT_ACTION',ReplyEpoch=1,Action='UNIT_ACTION_CONFIRM',UnitID=5}
          local ok,code=d.Publish(0,q,string.rep('x',200001));assert(ok==false and code=='TEXT_BUDGET')
          assert(not pcall(d.Publish,0,q,nil)) -- a producer bug blows up
        """)

    def test_view_targets_presentation(self):
        self.lua.execute("""
          local v=SPCPlayerActionReplies.New(1,'V','UNIT_VIEW')
          local p={Token='T',ReplyChannel='UNIT_VIEW',ReplyEpoch=1,Action='UNIT_ACTION_VIEW',UnitID=5}
          local ok,code=v.PublishView(0,p,{owner=0,unitID=6,token='T'});assert(not ok and code=='VIEW_IDENTITY_CHANGED')
          assert(v.PublishView(0,p,{owner=0,unitID=5,token='T',legal=true,prepared=false,amount=3})==true)
          local row=v.Take(0,'T');assert(row.view.legal==true and row.view.amount==3)
          local t=SPCPlayerActionReplies.New(1,'V','UNIT_TARGETS')
          local tp={Token='T',ReplyChannel='UNIT_TARGETS',ReplyEpoch=1,Action='UNIT_TARGETS_READ',UnitID=5}
          assert(t.PublishTargets(0,tp,{owner=0,unitID=5,token='T',version='V',mode='M',plots={{plot=7}},unknown={{cityID=2,reason='R'}}})==true)
          local tr=t.Take(0,'T').targets;assert(tr.plots[1].plot==7 and tr.unknown[1].reason=='R')
          local big={};for i=1,4097 do big[i]={plot=i}end
          local ok2,code2=t.PublishTargets(0,tp,{owner=0,unitID=5,token='T',version='V',mode='M',plots=big,unknown={}})
          assert(not ok2 and code2=='TARGET_ROWS_LIMIT')
          local c=SPCPlayerActionReplies.New(1,'V','CITY_PRESENTATION')
          local cp={Token='T',ReplyChannel='CITY_PRESENTATION',ReplyEpoch=1,Action='CITY_PRESENTATION_READ',CityID=3}
          local s={owner=0,cityID=3,token='T',potential=2,institutionSummary={known=true,revision=1,reputation={age=4,state='COUNTING'},tradition=false}}
          assert(c.PublishPresentation(0,cp,s)==true)
          local out=c.Take(0,'T').presentation;assert(out.potential==2 and out.institutionSummary.reputation.age==4 and out.institutionSummary.tradition==false)
          s.error=string.rep('e',20001);local ok3,code3=c.PublishPresentation(0,cp,s);assert(not ok3 and code3=='PRESENTATION_TEXT_BUDGET')
        """)


if __name__ == '__main__':
    unittest.main()
