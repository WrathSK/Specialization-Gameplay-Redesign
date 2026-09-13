"""D0010 mode contract; MOCK_ONLY proofs, no runtime registration or game writes."""
from pathlib import Path
import json,sqlite3
from lupa.lua55 import LuaRuntime
P=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
l.globals().Conquest=l.execute((P/'ConquestInitialization.lua').read_text())
l.globals().Family=l.execute((P/'DistrictFamily.lua').read_text())
c=sqlite3.connect((P.parent/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
rows=lambda q:l.table_from([l.table_from(dict(r)) for r in c.execute(q)])
l.globals().registry=l.globals().Family.Build(rows('select DistrictType from Districts'),rows('select * from DistrictReplaces'));c.close()
l.execute('''
local c={contextSource='MOCK_ONLY',cityUID='city-a',owner=1,eligibility='ENABLED',transitionID='conquest-1'}
local proof={contextSource='MOCK_ONLY',cityUID='city-a',fromOwner=0,toOwner=1,transitionID='conquest-1',
 status='OWNERSHIP_TRANSITION_COMPLETE',permanentFacts='VERIFIED_NO_IDENTITY_NO_PRIOR_SPECIALIZATION'}
local function district(name,id,complete)
 local d=Family.Resolve(registry,name);assert(d.status=='READY');d.districtUID=id;d.complete=complete;return d
end
local snapshot={status='COMPLETE_AT_TRANSITION',transitionID='conquest-1',boundary=9,districts={
 district('DISTRICT_SEOWON','d1',true),district('DISTRICT_HANSA','d2',true),district('DISTRICT_COMMERCIAL_HUB','d3',false),
 district('DISTRICT_GOVERNMENT','d4',true),district('DISTRICT_SEOWON','d1',true)}}
local function event(sequence,name,id)
 return {contextSource='MOCK_ONLY',delivery='LIVE_COMPLETION',cityUID='city-a',owner=1,transitionID='conquest-1',sequence=sequence,
 district=district(name,id,true)}
end
-- A: complete legal/replacement families; deduplicate; unfinished/non-v01 excluded.
local a=Conquest.Initialize(nil,c,proof,snapshot);assert(a.status=='READY',a.reason);a=a.record
assert(a.mode=='LEGACY_CLAIM' and a.legacySet.RESEARCH and a.legacySet.INDUSTRY and not a.legacySet.COMMERCE)
assert(a.identity==nil and a.potential==nil)
snapshot.districts[3].complete=true
local repeated=Conquest.Initialize(a,c,proof,snapshot);assert(not repeated.changed and not repeated.record.legacySet.COMMERCE)
-- Unlimited ordinary completions do not lock identity or expand candidate set.
for i=10,110 do
 local e=Conquest.Complete(a,c,event(i,'DISTRICT_COMMERCIAL_HUB','d3'));assert(e.status=='READY' and not e.changed)
 assert(not e.record.identity and not e.record.legacySet.COMMERCE)
end
assert(Conquest.Claim(a,c,'COMMERCE').status=='UNKNOWN')
local claims=Conquest.AvailableClaims(a,c);assert(claims.claims.RESEARCH and claims.claims.INDUSTRY)
claims.claims.COMMERCE=true;assert(not Conquest.AvailableClaims(a,c).claims.COMMERCE) -- no alias
local locked=Conquest.Claim(a,c,'INDUSTRY');assert(locked.changed and locked.record.identity=='INDUSTRY' and locked.record.potential==1)
assert(next(Conquest.AvailableClaims(locked.record,c).claims)==nil)
assert(not Conquest.Claim(locked.record,c,'RESEARCH').changed)
assert(not Conquest.Complete(locked.record,c,event(200,'DISTRICT_CAMPUS','d5')).changed)
assert(a.identity==nil) -- no mutation of input/save record
-- B: unfinished-only snapshot is empty; no claims, only later LIVE completion.
local empty={status='COMPLETE_AT_TRANSITION',transitionID='conquest-1',boundary=9,
 districts={district('DISTRICT_COMMERCIAL_HUB','d3',false)}}
local b=Conquest.Initialize(nil,c,proof,empty).record
assert(b.mode=='NORMAL_FIRST_COMPLETION' and next(b.legacySet)==nil)
assert(next(Conquest.AvailableClaims(b,c).claims)==nil)
assert(Conquest.Claim(b,c,'COMMERCE').status=='UNKNOWN')
assert(Conquest.Complete(b,c,event(9,'DISTRICT_CAMPUS','d1')).status=='UNKNOWN')
local load=event(10,'DISTRICT_CAMPUS','d1');load.delivery='LOAD_REPLAY';assert(Conquest.Complete(b,c,load).status=='UNKNOWN')
local first=Conquest.Complete(b,c,event(10,'DISTRICT_COMMERCIAL_HUB','d3'));assert(first.record.identity=='COMMERCE' and first.record.potential==1)
assert(Conquest.Complete(first.record,c,event(11,'DISTRICT_CAMPUS','d1')).record.identity=='COMMERCE')
assert(Conquest.Initialize(b,c,proof,snapshot).record.mode=='NORMAL_FIRST_COMPLETION')
-- C: existing identity always goes to permanent transfer, never touches a snapshot.
local poison=setmetatable({},{__index=function() error('MUST_NOT_SCAN_EXISTING_IDENTITY') end})
proof.permanentFacts='VERIFIED_EXISTING_IDENTITY'
assert(Conquest.Initialize(nil,c,proof,poison).status=='INHERIT_REQUIRED')
proof.permanentFacts='UNKNOWN';assert(Conquest.Initialize(nil,c,proof,empty).status=='UNKNOWN')
proof.permanentFacts='VERIFIED_NO_IDENTITY_NO_PRIOR_SPECIALIZATION'
-- Never replace a missing/incomplete boundary with an empty snapshot or delayed scan.
empty.status='PARTIAL';assert(Conquest.Initialize(nil,c,proof,empty).status=='UNKNOWN');empty.status='COMPLETE_AT_TRANSITION'
proof.status='OWNERSHIP_CHANGING';assert(Conquest.Initialize(nil,c,proof,empty).status=='UNKNOWN');proof.status='OWNERSHIP_TRANSITION_COMPLETE'
assert(Conquest.Initialize(nil,c,nil,snapshot).status=='UNKNOWN') -- old-save does not invent conquest
local unmapped=district('DISTRICT_CAMPUS','d1',true);unmapped.mappingStatus='UNREVIEWED'
empty.districts={unmapped};assert(Conquest.Initialize(nil,c,proof,empty).status=='UNKNOWN')
c.owner=2;assert(Conquest.Initialize(a,c,proof,snapshot).status=='UNKNOWN');c.owner=1
c.eligibility='DISABLED';assert(Conquest.Initialize(nil,c,proof,snapshot).status=='UNKNOWN');c.eligibility='ENABLED'
saved=a;context=c
''')
def plain(t):return {k:plain(v) if hasattr(v,'items') else v for k,v in t.items()}
serialized=json.dumps(plain(l.globals().saved));ctx=json.dumps(plain(l.globals().context))
n=LuaRuntime(unpack_returned_tuples=True)
def table(v):return n.table_from({k:table(x) for k,x in v.items()}) if isinstance(v,dict) else v
n.globals().Conquest=n.execute((P/'ConquestInitialization.lua').read_text());n.globals().saved=table(json.loads(serialized));n.globals().ctx=table(json.loads(ctx))
n.execute("""
local r=Conquest.Initialize(saved,ctx,nil,nil);assert(r.status=='READY' and not r.changed)
assert(r.record.mode=='LEGACY_CLAIM' and r.record.legacySet.RESEARCH and not r.record.identity)
assert(not r.record.legacySet.COMMERCE)
assert(Conquest.Claim(r.record,ctx,'RESEARCH').record.identity=='RESEARCH')
""")
print('LOCAL_SIMULATION_PASS: D0010 A/B/C mode separation, frozen deduplicated reviewed replacement candidates, no later expansion/auto-lock, claim closure, post-boundary completion, JSON/new-VM restore without rescan, unknown/old-save refusal. No native transfer/Claim proof.')
