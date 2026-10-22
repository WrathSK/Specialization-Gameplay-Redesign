"""L3: distinguish saved foreign hydration from genuine malformed return sequences."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1]
l=runpy.run_path(str(R/'DevelopmentTests/test_b102_e2_foundation.py'))['l']
l.execute(r"""
local KEY=SPCCityProgressionStore.KEY
local function hydrate(name,owner,id)Events[name].Fire(owner or 62,id or 40,4,5)end
local function built()GameEvents.CityBuilt.Fire(0,88,4,5)end
local function conquer()GameEvents.CityConquered.Fire(0,62,88,4,5)end
local function finish()built();conquer();removed();added();initialized();transferred()end
-- Both load notification orders, repeated initialization, all supported identities.
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
 for _,first in ipairs({'CityAddedToMap','CityInitialized'})do
  held(kind);local before=encode(e2Record())
  hydrate(first);hydrate('CityAddedToMap');hydrate('CityInitialized');hydrate(first)
  assert(encode(e2Record())==before,'hydration persisted new state')
  assert(not pcall(shared.EffectiveFacts.Read,0,c),'foreign hydration activated city')
  -- Cross a load boundary while still foreign; hydrate again, then actual screenshot order.
  boot();districts();hydrate('CityInitialized');hydrate('CityAddedToMap')
  local retained=e2Record();finish();local accepted=e2Record()
  assert(accepted.stage=='ACTIVE',d.Status(c).observation)
  assert(encode(retained.base)==encode(accepted.base) and encode(retained.investment)==encode(accepted.investment))
  assert(accepted.returnProof.version==2 and s.values.TOKEN==nil)
  local rev=accepted.revision;transferred();assert(e2Record().revision==rev)
  boot();districts();assert(shared.EffectiveFacts.Read(0,c).potential==3)
 end
end
-- Hydration exemption must not require conquest; existing no-CityBuilt return remains valid.
held();hydrate('CityAddedToMap');hydrate('CityInitialized');chain()
assert(e2Record().stage=='ACTIVE',d.Status(c).observation)
-- Wrong owner/ID, premature original-owner add, and old-reference events after the
-- transition has begun remain faults. A later removal or hydration cannot erase them.
for _,case in ipairs({'wrongowner','wrongid','premature','afterremove','afterconquest','afterbuilt','initbeforeadd'})do
 held()
 if case=='wrongowner' then hydrate('CityAddedToMap',9,40)
 elseif case=='wrongid' then hydrate('CityAddedToMap',62,99)
 elseif case=='premature' then hydrate('CityAddedToMap',0,88)
 elseif case=='afterremove' then removed();hydrate('CityInitialized')
 elseif case=='afterconquest' then conquer();hydrate('CityAddedToMap')
 elseif case=='afterbuilt' then built();hydrate('CityAddedToMap')
 elseif case=='initbeforeadd' then removed();s.ref.owner=0;s.ref.cityID=88;initialized()end
 hydrate('CityAddedToMap');finish()
 assert(e2Record().stage=='HELD_TRANSFER',case)
 assert(not pcall(shared.EffectiveFacts.Read,0,c),case)
 local before=encode(e2Record());local report=d.NativeDescribe(0,c)
 assert(report:find('首次拒绝',1,true),report)
 assert(encode(e2Record())==before)
end
-- First-fault slot retains the early notification even after same event is overwritten.
held();hydrate('CityAddedToMap',62,99);hydrate('CityAddedToMap');finish()
local report=d.NativeDescribe(0,c)
assert(report:find('CityAddedToMap(62,99,4,5)',1,true),report)
-- No chain completed / mid-transition reload still cannot authorize recapture.
held();hydrate('CityAddedToMap');transferred();assert(e2Record().stage=='HELD_TRANSFER')
held();hydrate('CityAddedToMap');built();conquer();removed();added();boot();districts();initialized();transferred()
assert(e2Record().stage=='HELD_TRANSFER')
print('B103 LOCAL_SIMULATION_PASS: exact foreign load hydration, repeat/init order, four identities, held/accepted coldload, permanent ledgers, strict conflict/order rejection, bounded first fault, no token rewrite')
""")
