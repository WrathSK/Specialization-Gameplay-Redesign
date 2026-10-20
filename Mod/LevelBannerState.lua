-- B254: disposable, detached UI projection of canonical facts. No persistent writes.
SPCLevelBannerState={}
function SPCLevelBannerState.Start(P,shared)
 local d={views={},revision=0};shared.LevelBanners=d
 local dirty={};local initialized=false
 local function key(pid,id)return pid..':'..id end
 local function mark(pid,id)
  if not P.IsTestPlayer(pid) then return end
  if id~=nil then dirty[key(pid,id)]={pid,id};return end
  local player=Players[pid];if not player then return end
  for _,c in player:GetCities():Members()do dirty[key(pid,c:GetID())]={pid,c:GetID()}end
  for k,v in pairs(d.views)do if v.owner==pid then dirty[k]={pid,v.cityID}end end
 end
 local function all()
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then mark(pid)end end
 end
 local function signature(v)
  if not v then return ''end
  return table.concat({v.owner,v.cityID,v.x,v.y,v.specialization or '',v.potential or -1,v.active or -1,v.activeStatus or ''},':')
 end
 function d.Flush()
  if not initialized then initialized=true;all()end
  local todo=dirty;dirty={}
  for k,ref in pairs(todo)do
   local pid,id=ref[1],ref[2];local player=Players[pid];local c=player and player:GetCities():FindID(id)
   local v
   if c and c:GetOwner()==pid then
    local ok,f=pcall(shared.EffectiveFacts.Read,pid,c)
    v={owner=pid,cityID=id,x=c:GetX(),y=c:GetY(),specialization=ok and f.specialization or nil,
     potential=ok and f.potential or nil,active=ok and f.active or nil,activeStatus=ok and f.activeStatus or 'UNKNOWN'}
   end
   if signature(v)~=signature(d.views[k])then d.views[k]=v;d.revision=d.revision+1 end
  end
 end
 local prior=shared.OnPermanentCityWrite
 shared.OnPermanentCityWrite=function(c,reason)
  if prior then prior(c,reason)end
  if c then mark(c:GetOwner(),c:GetID())end
 end
 local function hook(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','PlayerTurnActivated'})do hook(name,function(pid)mark(pid)end)end
 for _,name in ipairs({'CityAddedToMap','CityRemovedFromMap'})do hook(name,mark)end
 -- Transfer has a different native signature; rare ownership events refresh local projections.
 hook('CityTransfered',all)
 hook('LoadScreenClose',function()all();d.Flush()end)
 hook('GameCoreEventPublishComplete',d.Flush)
 hook('GameCoreEventPlaybackComplete',d.Flush)
end
