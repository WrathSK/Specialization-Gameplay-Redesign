include('SafeCallbacks')
include('EngineeringStudyModel')
include('ExpeditionTrainingDiagnostics')
-- B235: one owner for city study attempts. Reuses Store transaction boundaries
-- and the proven full-production-turn/FinishProgress primitive, not Dialogue quota.
SPCEngineeringStudyProjects={}
function SPCEngineeringStudyProjects.Start(P,shared)
 local M=SPCEngineeringStudyModel;local cp=M.Copy;local store=assert(shared.CityProgressionStore)
 local PROJECT='PROJECT_SPC_ENGINEERING_STUDY';local MARKER='BUILDING_SPC_ENGINEERING_STUDY_ACCESS'
 local d={views={},revision=0};shared.EngineeringStudy=d
 local ready,busy=false,false;local dirty,active,settling,interrupted,finishing,armed={},{},{},{},{},{}
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'ENGINEERING_STUDY')
 local function key(pid,id)return pid..':'..id end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function same(a,b)
  if type(a)~='table' or type(b)~='table'then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function code(e)return tostring(e):match('EST_[A-Z_]+') or tostring(e):match('IH_[A-Z_]+') or 'EST_STATE_UNAVAILABLE'end
 local function mark(pid,id)if P.IsTestPlayer(pid) and type(id)=='number'then dirty[key(pid,id)]={pid,id}end end
 local function markPlayer(pid)if P.IsTestPlayer(pid)then for _,c in Players[pid]:GetCities():Members()do mark(pid,c:GetID())end end end
 local function publish(pid,id,v)
  local k=key(pid,id)
  if same(d.views[k],v)then return end;d.views[k]=v;d.revision=d.revision+1
  if v then trace.Record('ENGINEERING_STUDY',{owner=pid,city=id,phase=v.stage,reason=v.reason,
   count=v.L,eraCount=v.E,taskStart=v.start,taskDue=v.start and v.start+1,readStatus=v.stage=='HELD' and 'PENDING' or 'VERIFIED'})end
 end
 local function safe(pid,id,fn)
  local ok,err=pcall(fn)
  if not ok then local old=d.views[key(pid,id)];publish(pid,id,{stage='HELD',reason=code(err),reference=old and old.reference,token=old and old.token})end
  return ok
 end
 local function read(pid,c)
  local s=store.EngineeringState(pid,c);local f=shared.EffectiveFacts.Read(pid,c)
  assert(f.token==s.token and f.owner==pid and f.cityID==c:GetID(),'EST_REFERENCE_CHANGED')
  local known=f.activeStatus=='KNOWN' and not f.investmentPending
  return s,known,known and f.specialization=='INDUSTRY' and f.active==4
 end
 local function credit(pid)return shared.IndustryHistory.Credit(pid)end
 local function write(pid,c,s,v)
  store.WriteEngineering(pid,c,s.value,v)
  local actual=store.EngineeringState(pid,c)
  assert(same(actual.value,v) and same(actual.reference,s.reference) and actual.token==s.token,'EST_WRITE_UNCONFIRMED')
  return actual
 end
 local function queue(c)
  local q=c:GetBuildQueue();local ok,target=P.Call(q,'CurrentlyBuilding');assert(ok,'EST_QUEUE_UNKNOWN')
  if target~=PROJECT then return q,false end
  local good,n=P.Call(q,'GetSize')
  if not good then
   local v=assert(ExposedMembers.SPC_EngineeringStudyRead,'EST_UI_NOT_READY')(c:GetOwner(),c:GetID())
   assert(same(v.reference,ref(c)) and v.turn==Game.GetCurrentGameTurn() and v.project==PROJECT,'EST_QUEUE_REFERENCE');n=v.size
  end
  assert(type(n)=='number' and n==1,'EST_SINGLE_PROJECT_REQUIRED');return q,true
 end
 local function cancel(pid,c,s,why)
  if s.value and s.value.pending then write(pid,c,s,M.Cancel(s.value,why))end
  local k=key(pid,c:GetID());active[k]=nil;interrupted[k]=nil;armed[k]=nil;mark(pid,c:GetID())
 end
 local function audit(pid,id)
  local c=city(pid,id);local k=key(pid,id)
  if not c or c:GetOwner()~=pid then active[k]=nil;publish(pid,id,nil);return end
  local ok,s,known,eligible=pcall(read,pid,c)
  local good,e=pcall(credit,pid);local L=ok and s.value and s.value.L or 0
  local p=ok and s.value and s.value.pending
  local allowed=ok and known and eligible and good and e.known and (L<e.E or p~=nil)
  local row=assert(P.Info('Buildings',MARKER),'EST_ACCESS_DEFINITION');local b=c:GetBuildings()
  local has=P.HasBuilding(b,row.Index);assert(type(has)=='boolean','EST_ACCESS_UNKNOWN')
  -- UNKNOWN retains an existing access marker only; it never grants access or
  -- cancels a confirmed round by changing the engine's prerequisite underneath it.
  if not ok or not known or (eligible and (not good or not e.known))then allowed=has end
  if has~=allowed then
   if allowed then P.CreateBuilding(c:GetBuildQueue(),row.Index)else P.RemoveBuilding(b,row.Index)end
   assert(P.HasBuilding(b,row.Index)==allowed,'EST_ACCESS_UNCONFIRMED')
  end
  if not ok then error(s)end
  if p then
   active[k]={pid,id}
   if interrupted[k]then cancel(pid,c,s,'EST_PRODUCTION_INTERRUPTED');p=nil
   elseif known and not eligible then cancel(pid,c,s,'EST_QUALIFICATION_LOST');p=nil
   elseif known then
    local _,matches=queue(c)
    if not matches and p.stage=='ACTIVE'then cancel(pid,c,s,'EST_PRODUCTION_INTERRUPTED');p=nil end
   end
  else active[k]=nil end
  local stage=p and p.stage or (eligible and good and e.known and L<e.E and 'AVAILABLE' or 'INELIGIBLE')
  local why=p and p.reason or (not eligible and 'EST_ACTIVE_IV_REQUIRED' or good and e.known and L>=e.E and 'EST_KNOWLEDGE_REACHED' or 'EST_SELECT_PROJECT')
  if not known or not good or not e.known then stage='HELD';why=not known and 'EST_QUALIFICATION_UNKNOWN' or 'EST_E_UNKNOWN'end
  publish(pid,id,{stage=stage,reason=why,L=L,E=good and e.E or nil,start=p and p.start,reference=s.reference,token=s.token})
 end
 local function initialize()
  if ready then return true end
  local status=store.HistoryStartStatus();if status=='WAITING' or status=='HELD'then return false end
  ready=true;for pid in pairs(Players)do markPlayer(pid)end;return true
 end
 function d.Flush()
  if busy or not initialize()then return end;busy=true
  local work=dirty;dirty={};for _,v in pairs(work)do safe(v[1],v[2],function()audit(v[1],v[2])end)end
  busy=false
 end
 function d.Refresh(pid,id)mark(pid,id);d.Flush()end
 function d.CreditChanged(pid)markPlayer(pid)end -- confirmed history commit, no immediate cross-writer reentry
 function d.Request(pid,p)
  if not initialize() or busy or not P.IsTestPlayer(pid) or type(p.CityID)~='number'then return end
  safe(pid,p.CityID,function()
   local c=assert(city(pid,p.CityID),'EST_CITY_UNKNOWN');local s,known,eligible=read(pid,c)
   if interrupted[key(pid,p.CityID)]then cancel(pid,c,s,'EST_PRODUCTION_INTERRUPTED');s=store.EngineeringState(pid,c)end
   local e=credit(pid);assert(known and eligible and e.known,'EST_ENTRY_UNKNOWN')
   assert(p.StartTurn==Game.GetCurrentGameTurn(),'EST_START_STALE')
   local q,matches=queue(c);assert(matches,'EST_PROJECT_NOT_CURRENT');assert(type(P.Field(q,'FinishProgress'))=='function','EST_FINISH_UNAVAILABLE')
   if s.value and s.value.pending then assert(s.value.pending.stage=='ACTIVE','EST_ABANDON_REQUIRED');return end
   write(pid,c,s,M.Begin(s.value,s.token,s.reference,p.StartTurn,e.E));mark(pid,p.CityID)
  end);d.Flush()
 end
 local function completion(pid,id,index)
  if not ready or not P.IsTestPlayer(pid)then return end
  local row=P.Info('Projects',index);if not row or row.ProjectType~=PROJECT then return end
  local k=key(pid,id);if settling[k]then return end;settling[k]=true
  safe(pid,id,function()
   local c=assert(city(pid,id),'EST_CITY_UNKNOWN');local s,known,eligible=read(pid,c);local p=s.value and s.value.pending
   if not p then return end
   if known and not eligible then cancel(pid,c,s,'EST_QUALIFICATION_LOST');return end
   if p.stage=='HELD'then return end
   local now=Game.GetCurrentGameTurn();local e=credit(pid)
   if not known or not e.known or not p.ended or now~=p.start+1 or (p.stage=='CALLING' and armed[k]~=p.id)then
    armed[k]=nil;interrupted[k]=nil;write(pid,c,s,M.Hold(s.value,'EST_COMPLETION_UNCONFIRMED'));mark(pid,id);return
   end
   assert(eligible and s.value.L<e.E,'EST_COMPLETION_INELIGIBLE')
   if p.stage=='ACTIVE'then local _,matches=queue(c);assert(not matches,'EST_COMPLETION_NOT_EXITED')end
   armed[k]=nil -- no replay after ambiguous Store commit or native reentry
   write(pid,c,s,M.Complete(s.value,p.id,now));active[k]=nil;interrupted[k]=nil;mark(pid,id)
   if shared.StandardizationEffects then shared.StandardizationEffects.SourceChanged(pid,id)end
  end)
  settling[k]=nil
 end
 local function advance(pid,ending)
  if not initialize() or busy or not P.IsTestPlayer(pid)then return end
  for _,v in pairs(cp(active))do if v[1]==pid then safe(pid,v[2],function()
   local c=assert(city(pid,v[2]),'EST_CITY_UNKNOWN');local s,known,eligible=read(pid,c);local p=s.value and s.value.pending
   if not p then active[key(pid,v[2])]=nil;return end
   if known and not eligible then cancel(pid,c,s,'EST_QUALIFICATION_LOST');return end
   if not known then return end
   local q,matches=queue(c)
   if not matches and p.stage=='ACTIVE'then cancel(pid,c,s,'EST_PRODUCTION_INTERRUPTED');return end
   if p.stage~='ACTIVE'then return end
   local now=Game.GetCurrentGameTurn()
   if ending and now==p.start then if not p.ended then write(pid,c,s,M.EndTurn(s.value,now))end
   elseif not ending and now>p.start then
    if now~=p.start+1 or not p.ended then cancel(pid,c,s,'EST_FULL_TURN_UNCONFIRMED')
    else
     assert(type(P.Field(q,'FinishProgress'))=='function','EST_FINISH_UNAVAILABLE')
     write(pid,c,s,M.Calling(s.value,now))
     local k=key(pid,v[2]);armed[k]=p.id;finishing[k]=true
     local ok,err=pcall(q.FinishProgress,q);finishing[k]=nil;mark(pid,v[2]);assert(ok,'EST_NATIVE_FINISH_FAILED')
    end
   end
  end)end end;d.Flush()
 end
 local function production(pid,id)
  if not ready or not P.IsTestPlayer(pid)then return end
  local k=key(pid,id)
  if active[k] and not settling[k]then safe(pid,id,function()
   local c=assert(city(pid,id),'EST_CITY_UNKNOWN');local s,known,eligible=read(pid,c);local p=s.value and s.value.pending
   if p and known and not eligible then cancel(pid,c,s,'EST_QUALIFICATION_LOST')
   elseif p then
    local _,matches=queue(c)
    if not matches and p.stage=='ACTIVE'then interrupted[k]=true
    elseif not matches and (p.stage=='HELD' or p.stage=='CALLING' and not finishing[k])then cancel(pid,c,s,'EST_ABANDONED')end
   end
  end)end;mark(pid,id)
 end
 function d.Describe(pid,c)
  local s=store.EngineeringState(pid,c);local L=s.value and s.value.L or 0;local e=credit(pid)
  local f=shared.EffectiveFacts.Read(pid,c);local effective=f.activeStatus=='KNOWN' and f.specialization=='INDUSTRY' and f.active==4
  local v=d.views[key(pid,c:GetID())]
  trace.Record('ENGINEERING_STUDY_REPORT',{owner=pid,city=c:GetID(),count=L,eraCount=e.E,phase=v and v.stage or 'UNKNOWN',reason=v and v.reason or 'EST_NOT_READY'})
  return '工程传统研习｜本城 L：'..L..' / 全国 E：'..(e.known and e.E or '未知')
   ..'\n历史层数保留；当前增强：'..(effective and ('建造 +'..(2*L)..' 个百分点，建筑购买折扣 '..(2*L)..'%') or '暂停（需要工业 ACTIVE IV）')
   ..'\n研习：'..(v and v.stage=='ACTIVE' and '完整一回合进行中' or v and v.stage=='AVAILABLE' and '可从生产列表选择“工程传统研习”' or v and v.reason=='EST_KNOWLEDGE_REACHED' and '已达到当前可研习知识' or '暂不可开始；'..tostring(v and v.reason or 'EST_NOT_READY'))
   ..'\n区域逐模板购买折扣尚无可靠接口，本批未接入；不授予购买权限。'
 end
 local function hook(n,f)local e=P.Field(Events,n);if e and e.Add then e.Add(f)end end
 hook('CityProjectCompleted',completion);hook('CityProductionChanged',production);hook('CityProductionQueueChanged',production)
 hook('GameCoreEventPublishComplete',d.Flush)
 hook('PlayerTurnDeactivated',function(pid)d.Flush();advance(pid,true)end)
 hook('PlayerTurnActivated',function(pid)d.Flush();advance(pid,false)end)
 for _,n in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged'})do hook(n,function(pid)
  for p in pairs(Players)do if P.IsTestPlayer(p) and (type(pid)~='number' or pid<0 or p==pid)then
   for _,v in pairs(cp(active))do if v[1]==p then safe(p,v[2],function()audit(p,v[2])end)end end;markPlayer(p)
  end end
 end)end
 hook('CityInitialized',mark);hook('CityRemovedFromMap',mark)
 hook('LoadScreenClose',function()initialize();for pid in pairs(Players)do markPlayer(pid)end;d.Flush();for pid in pairs(Players)do advance(pid,false)end end)
 store.RegisterExit('EngineeringStudy',function(c,loss)
  store.RemoveOwned(c,loss,{MARKER})
  -- A return can assign a different cityID. Remove only this city's current
  -- reference, not the original ID which may since belong to another city.
  for k,v in pairs(d.views)do if v.reference and v.reference.owner==loss.origin.owner
   and v.reference.x==loss.origin.x and v.reference.y==loss.origin.y then
   active[k]=nil;dirty[k]=nil;interrupted[k]=nil;armed[k]=nil;publish(v.reference.owner,v.reference.cityID,nil)
  end end
 end)
 store.RegisterReturn('EngineeringStudy',function(pid,c)mark(pid,c:GetID())end)
 if shared.FactChanges then shared.FactChanges.RegisterConsumer('EngineeringStudy',function(e)mark(e.player,e.city)end,{kinds={'IDENTITY','POTENTIAL','ACTIVE'}})end
end
