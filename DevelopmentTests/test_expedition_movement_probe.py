"""B219 actual probe + Gate envelope isolation; native collisions remain unknown."""
import re
import sqlite3
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import test_expedition_spy_task as base
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
from read_expedition_trace import GATE_PATTERN


def ready(ui=False):
    l=base.gate();lines=[];l.globals().print=lines.append
    l.execute("""
      req('CREATE','base');insightRecords['CIVILIZATION_TARGET:PEOPLE']={civ='CIVILIZATION_TARGET',category='PEOPLE',turn=70}
      units[50]=unit(50,103,2,3,3);foreignUnits[7]=unit(7,101,3,15,9)
      info[101]={UnitType='UNIT_CIVILIAN',FormationClass='FORMATION_CLASS_CIVILIAN',Spy=false,Stackable=false}
      info[100].Name='TEAM';info[103].Name='SPY'
      function makePlot(x,y)
       return {GetX=function()return x end,GetY=function()return y end,IsWater=function()return water==true end,IsImpassable=function()return impassable==true end}
      end
      Map={GetPlot=function(x,y)if not noTarget then return makePlot(x,y)end end,
       GetAdjacentPlot=function(x,y,d)if not noPad then return makePlot(x+d,y-1)end end}
      eventLists={}
      function event(name)
       local fs={};eventLists[name]=fs
       return {Add=function(fn)fs[#fs+1]=fn end,Remove=function(fn)for i,f in ipairs(fs)do if f==fn then table.remove(fs,i);return end end end}
      end
      for _,name in ipairs({'UnitMoveComplete','UnitTeleported','PlayerTurnActivated','UnitRemovedFromMap','LoadScreenClose'})do Events[name]=event(name)end
      function fire(name,...)for _,f in ipairs(eventLists[name])do f(...)end end
      GameEvents.SPC_ExpeditionMovementRequest={Add=function(fn)probe=fn end}
      calls={};stages=0;moveCalls=0
      UnitManager.PlaceUnit=function(u,x,y)
       calls[#calls+1]='PlaceUnit';stages=stages+1
       if stages==1 then
        if stageThrow then error('STAGE_NATIVE_ERROR',0)end
        if stageNoop then return end
        u.x=x+(stageOffset and 1 or 0);u.y=y
        if stageDisplace then foreignUnits[7].x=16 end
        if addOccupant then foreignUnits[8]=unit(8,101,3,15,9)end
       else
        if nativeThrow then error('MOVE_NATIVE_ERROR',0)end
        if not nativeNoop then u.x=x+(offset and 1 or 0);u.y=y end
        if displace then foreignUnits[7].x=16 end
        if wrongType then u.type_=101 end
        if removeSubject then units[u.id]=nil end
       end
       fire('UnitTeleported',u.owner,u.id,x,y)
      end
      UnitManager.MoveUnit=function(u,x,y)
       calls[#calls+1]='MoveUnit';moveCalls=moveCalls+1
       if nativeThrow then error('MOVE_NATIVE_ERROR',0)end
       if not nativeNoop then u.x=x+(offset and 1 or 0);u.y=y end
       if displace then foreignUnits[7].x=16 end
       fire('UnitMoveComplete',u.owner,u.id,x,y)
      end
      function packet(id,method,token)
       local u=units[id or 40]
       return {Token=token or 'trial',UnitID=u.id,Method=method or 'PlaceUnit',X=15,Y=9,SampleTurn=currentTurn,
        NativeOperation=-1,FromX=u.x,FromY=u.y,Kind=u.type_,Name=u.name}
      end
      baselineWrites=storeWrites;baselineEnvelopeCount=0;for _ in pairs(gameProperties)do baselineEnvelopeCount=baselineEnvelopeCount+1 end
      savedBefore=shared.ExpeditionGate.Training.Read(2)
      P.VERSION='P0-B-219.246'
    """)
    l.execute((R/'Mod/ExpeditionMovementProbe.lua').read_text());l.execute('SPCExpeditionMovementProbe.Start(P,shared)')
    if ui:
        l.execute("""
          SPCP0=P;include=function()end
          Controls={};function control(id)
           local c={};Controls[id]=c
           function c:SetText(s)self.text=s end;function c:SetHide(v)self.hidden=v end
           function c:IsHidden()return self.hidden end;function c:SetDisabled(v)self.disabled=v end
           function c:RegisterCallback(button,fn)self.click=fn end
          end
          ContextPtr={SetInitHandler=function(self,fn)init=fn end,SetShutdown=function(self,fn)shutdown=fn end,
           SetInputHandler=function(self,fn)input=fn end,SetUpdate=function()error('NO_TIMER')end}
          Locale={Lookup=function(k,...)local args={...};for i,v in ipairs(args)do args[i]=tostring(v)end;return k..':'..table.concat(args,',')end}
          Mouse={eLClick=1};KeyEvents={KeyDown=1,KeyUp=2};Keys={VK_M=77,VK_ESCAPE=27}
          LuaEvents={SPC_ExpeditionMovementOpen=event('open')}
          Events.GameCoreEventPublishComplete=event('publish')
          selected=40;Game.GetLocalPlayer=function()return 2 end
          Map.GetPlotByIndex=function(id)if id==123 then return makePlot(15,9)end end
          PlayerOperations={EXECUTE_SCRIPT=1};sent=0
          UI={GetHeadSelectedUnit=function()return units[selected]end,GetCursorPlotID=function()return cursor or 123 end,
           RequestPlayerOperation=function(pid,op,p)
            sent=sent+1;lastPacket=p;if sendThrow then error('unknown send')end
            if not defer then probe(pid,p)end
           end}
        """)
        for e in ET.parse(R/'Mod/UI/ExpeditionMovementProbe.xml').iter():
            if e.get('ID'): l.globals().control(e.get('ID'))
        l.execute((R/'Mod/UI/ExpeditionMovementProbe.lua').read_text());l.execute("init();fire('open');input(KeyEvents.KeyUp,Keys.VK_M)")
    return l,lines


class MovementProbe(unittest.TestCase):
    def invariant(self,l):
        l.execute("""
          assert(storeWrites==baselineWrites and insightWrites==0 and properties==0 and destroys==0 and initCalls==1)
          local now=shared.ExpeditionGate.Training.Read(2)
          local function same(a,b)
           if type(a)~=type(b)then return false end
           if type(a)~='table'then return a==b end
           for k,v in pairs(a)do if not same(v,b[k])then return false end end
           for k,v in pairs(b)do if a[k]==nil then return false end end;return true
          end
          assert(same(now,savedBefore),'saved state changed')
          local count=0;for _ in pairs(gameProperties)do count=count+1 end;assert(count==baselineEnvelopeCount)
          assert(insightRecords['CIVILIZATION_TARGET:PEOPLE'].turn==70)
        """)

    def test_both_types_both_primitives_same_occupied_target(self):
        for id in [40,50]:
            for method in ['PlaceUnit','MoveUnit']:
                with self.subTest(id=id,method=method):
                    l,lines=ready();l.execute(f"probe(2,packet({id},'{method}'));assert(ExposedMembers.SPC_ExpeditionMovementReply.status=='EXACT')")
                    l.execute(f"assert(#calls==2 and calls[1]=='PlaceUnit' and calls[2]=='{method}');assert(units[{id}].x==15 and units[{id}].y==9);assert(foreignUnits[7].x==15 and foreignUnits[7].y==9)")
                    l.execute('assert(not shared.ExpeditionGate.Training.Available(2) and not shared.ExpeditionGate.Training.NoUnits(2))')
                    self.invariant(l)
                    self.assertTrue(any('pad=15,8' in s for s in lines))
                    self.assertTrue(all(GATE_PATTERN.fullmatch(s) for s in lines if 'movementProbe=' in s))

    def test_offset_and_noop_are_observations_never_repaired(self):
        for mode in ['offset=true','nativeNoop=true']:
            for method in ['PlaceUnit','MoveUnit']:
                with self.subTest(mode=mode,method=method):
                    l,_=ready();l.execute(mode+f";probe(2,packet(40,'{method}'));assert(ExposedMembers.SPC_ExpeditionMovementReply.status=='NOT_EXACT' and #calls==2)")
                    self.invariant(l)

    def test_duplicate_new_token_and_formal_actions_cannot_repeat_after_mutation(self):
        l,_=ready();l.execute("""
          p=packet();probe(2,p);probe(2,p);probe(2,packet(50,'MoveUnit','next'))
          assert(#calls==2 and ExposedMembers.SPC_ExpeditionMovementReply.reason=='RELOAD_REQUIRED')
          req('READ','r');req('TASK','t',40);req('END','e',40);ownTurn(2)
          assert(ExposedMembers.SPC_ExpeditionGateReply.error=='MOVEMENT_PROBE_RELOAD_REQUIRED')
        """);self.invariant(l)

    def test_preflight_rejections_make_no_calls_or_lock(self):
        changes=["p.SampleTurn=0","p.NativeOperation=27","p.FromX=99","p.Kind=999","p.Name='changed'","p.Method='Destroy'",
         "p.UnitID=999","p.X=-1","noTarget=true","water=true","impassable=true","visible=false","noPad=true",
         "foreignUnits={}","info[101].FormationClass='MILITARY'","UnitManager.MoveUnit=nil;p.Method='MoveUnit'",
         "info[101].Spy=true","units[40].name='changed'","city.token='changed'","units[40].operation=27"]
        for change in changes:
            with self.subTest(change=change):
                l,_=ready();l.execute("p=packet();"+change+";probe(2,p);assert(#calls==0 and not ExposedMembers.SPC_ExpeditionMovementReply.reload)")
                self.invariant(l)

    def test_unbound_active_or_unknown_gate_is_not_testable(self):
        for change in ["nativeDispatch('depart')", "shared.ExpeditionGate=nil", "units[40]=nil"]:
            with self.subTest(change=change):
                l,_=ready();l.execute("p=packet(50);"+change+";n=storeWrites;probe(2,p);assert(#calls==0 and storeWrites==n)")

    def test_source_and_occupant_limits_stop_before_movement(self):
        l,_=ready();l.execute("for i=8,16 do foreignUnits[i]=unit(i,101,3,15,9)end;probe(2,packet());assert(#calls==0 and ExposedMembers.SPC_ExpeditionMovementReply.reason=='OCCUPANTS_LIMIT')")
        self.invariant(l)

    def test_staging_failures_never_execute_candidate(self):
        for mode in ['stageNoop=true','stageOffset=true','stageThrow=true','stageDisplace=true','addOccupant=true']:
            with self.subTest(mode=mode):
                l,_=ready();l.execute(mode+";probe(2,packet(40,'MoveUnit'));assert(#calls==1 and moveCalls==0 and ExposedMembers.SPC_ExpeditionMovementReply.reload)")
                self.invariant(l)

    def test_error_displacement_or_identity_loss_is_terminal(self):
        for mode in ['nativeThrow=true','displace=true','wrongType=true','removeSubject=true']:
            with self.subTest(mode=mode):
                l,_=ready();l.execute(mode+";probe(2,packet());assert(ExposedMembers.SPC_ExpeditionMovementReply.status=='STOP' and #calls==2)")
                self.invariant(l)

    def test_unknown_outcome_later_events_only_observe_no_resumption(self):
        l,lines=ready();l.execute("nativeNoop=true;probe(2,packet(40,'MoveUnit'));units[40].x=15;units[40].y=9;fire('UnitTeleported',2,40,15,9);assert(#calls==2)")
        self.assertTrue(any('TELEPORT_EVENT' in s and 'actual=15,9' in s for s in lines))
        self.invariant(l)

    def test_unrelated_events_ignored_and_history_bounded(self):
        l,lines=ready();l.execute('probe(2,packet())');n=len(lines)
        l.execute("for i=1,20 do fire('UnitTeleported',3,40,3,3);fire('UnitMoveComplete',2,50,3,3)end")
        self.assertEqual(len(lines),n)
        l.execute("for i=1,30 do fire('UnitTeleported',2,40,3,3)end");n=len(lines)
        l.execute("fire('UnitMoveComplete',2,40,3,3)");self.assertEqual(len(lines),n);self.invariant(l)

    def test_watch_closes_on_turn_load_or_removal_without_unlock(self):
        for evt,args in [('PlayerTurnActivated','2'),('LoadScreenClose',''),('UnitRemovedFromMap','2,40')]:
            with self.subTest(evt=evt):
                l,lines=ready();l.execute(f"probe(2,packet());fire('{evt}',{args})".replace(",)",")"));n=len(lines)
                l.execute("fire('UnitTeleported',2,40,3,3);probe(2,packet(50,'PlaceUnit','again'));assert(#calls==2)")
                self.assertEqual(sum('TELEPORT_EVENT' in s for s in lines[n:]),0);self.invariant(l)

    def test_arrived_team_binding_and_history_stay_unchanged(self):
        l,_=ready();l.execute("nativeDispatch('depart');arrival(41,true,false);baselineWrites=storeWrites;savedBefore=shared.ExpeditionGate.Training.Read(2);probe(2,packet(41,'MoveUnit'));assert(#calls==2)")
        self.invariant(l)

    def test_no_eager_engine_calls_and_old_gameplay_unchanged_without_probe(self):
        l,_=ready();l.execute("assert(#calls==0);nativeDispatch('depart');arrival(41,true,false);assert(req('READ','normal').phase=='ARRIVED' and #calls==0)")

    def test_read_and_initialize_do_not_mutate(self):
        l,_=ready();l.execute("local a=shared.ExpeditionGate.MovementProbeRead(2);assert(a.unitID==40 and a.sourceCity==1 and #calls==0)")
        self.invariant(l)


class MovementUI(unittest.TestCase):
    def test_real_ui_marks_pins_and_sends_one_request(self):
        l,lines=ready(True);l.execute("Controls.Move.click();assert(sent==1 and #calls==2 and lastPacket.X==15 and lastPacket.Y==9 and lastPacket.UnitID==40);Controls.Place.click();assert(sent==1)")
        self.assertTrue(any('UI_READ' in s for s in lines) is False)
        l.execute("fire('publish');assert(Controls.Report.text:find('RELOAD'));Controls.Read.click();assert(sent==1)")
        self.assertTrue(any('UI_READ' in s for s in lines))
        self.assertTrue(all(GATE_PATTERN.fullmatch(s) for s in lines if 'movementProbe=' in s))

    def test_unknown_send_and_pending_never_retransmit(self):
        for mode in ['sendThrow=true','defer=true']:
            with self.subTest(mode=mode):
                l,_=ready(True);l.execute(mode+";Controls.Place.click();Controls.Read.click();Controls.Move.click();Controls.Close.click();fire('open');Controls.Move.click();assert(sent==1)")

    def test_late_reply_after_close_is_consumed_without_reopening(self):
        l,_=ready(True);l.execute("defer=true;Controls.Move.click();Controls.Close.click();probe(2,lastPacket);fire('publish');assert(Controls.Window.hidden and Controls.Report.text:find('RELOAD'))")

    def test_native_unknown_changed_unit_and_missing_target_no_send(self):
        for mode in ['units[40].operation=9','units[40].GetSpyOperation=nil',"units[40].name='x'","units[40].type_=101"]:
            with self.subTest(mode=mode):
                l,_=ready(True);l.execute(mode+";Controls.Move.click();assert(sent==0 and #calls==0)")
        l,_=ready(True);l.execute("fire('open');Controls.Move.click();assert(sent==0)")

    def test_bounded_ui_reads_and_event_cleanup(self):
        l,lines=ready(True);l.execute("Controls.Move.click();for i=1,20 do fire('publish');Controls.Read.click()end;shutdown()")
        self.assertEqual(sum('movementProbe=UI_READ' in s for s in lines),4)
        l.execute("assert(#eventLists.open==0 and #eventLists.publish==0)")

    def test_preflight_fix_can_resubmit_without_reloading(self):
        l,_=ready(True);l.execute("noPad=true;Controls.Move.click();assert(#calls==0 and not Controls.Move.disabled);noPad=false;Controls.Move.click();assert(sent==2 and #calls==2)")

    def test_ui_and_gameplay_contain_no_timer_or_property_writer(self):
        src=''.join((R/p).read_text() for p in ['Mod/ExpeditionMovementProbe.lua','Mod/UI/ExpeditionMovementProbe.lua'])
        for forbidden in ['SetUpdate','SetProperty','RequestOperation(', 'InitUnit(', 'Destroy(', 'AddExpeditionInsight','SetSpy','ChangeEraScore']:
            self.assertNotIn(forbidden,src)

    def test_package_localization_and_p0_entry(self):
        doc=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot()
        paths=[e.text.strip() for e in doc.findall('./Files/File')]
        for p in ['ExpeditionMovementProbe.lua','UI/ExpeditionMovementProbe.lua','UI/ExpeditionMovementProbe.xml']:
            self.assertEqual(paths.count(p),1)
        self.assertEqual(len(doc.findall(".//AddUserInterfaces[@id='SPC_ExpeditionMovementUI']")),0)
        ET.parse(R/'Mod/UI/ExpeditionMovementProbe.xml')
        db=sqlite3.connect(':memory:');db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))')
        db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        lua=(R/'Mod/UI/ExpeditionMovementProbe.lua').read_text();xml=(R/'Mod/UI/ExpeditionMovementProbe.xml').read_text()
        keys=set(re.findall(r"L\('([A-Z_]+)'",lua))|set(re.findall('LOC_SPC_MOVE_PROBE_([A-Z_]+)',xml))
        keys.discard('STATUS_');keys.update({'STATUS_EXACT','STATUS_NOT_EXACT','STATUS_STOP'})
        for key in keys:self.assertEqual(db.execute('select count(*) from LocalizedText where Tag=?',('LOC_SPC_MOVE_PROBE_'+key,)).fetchone()[0],2,key)
        panel=(R/'Mod/UI/P0Panel.lua').read_text()
        self.assertNotIn('Controls.ExpeditionGateButton:RegisterCallback(Mouse.eRClick',panel)
        self.assertNotIn('SPCExpeditionMovementProbe.Start(P,shared)',(R/'Mod/Gameplay.lua').read_text())
        db.close()

if __name__=='__main__':unittest.main()
