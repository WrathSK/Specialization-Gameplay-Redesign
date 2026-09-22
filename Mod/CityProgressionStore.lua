-- E2 first slice: one explicit same-owner progression cutover. Not a global city registry.
SPCCityProgressionStore={KEY='SPC_CITY_PROGRESSION_E2_V1'}
function SPCCityProgressionStore.Start(P,shared)
 local M=SPCCityIdentityRead;local cp=M.Copy;local KEY=SPCCityProgressionStore.KEY
 local d={exitStatus="NOT_CONFIRMED",exitErrors={}};shared.CityProgressionStore=d
 local exits,finished,attempts={},{},{};local exitBusy=false
 local root,fault,busy;local ready=false
 local kinds={RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a) do if not same(v,b[k]) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function source(c)
  local s={ref=ref(c),values={}}
  for _,n in ipairs({'TOKEN','JOURNAL','FLOW','INVEST'}) do s.values[n]=c:GetProperty(M.Keys[n])end
  s.ledger=Game:GetProperty('SPC_DEV_BINDING_B013_P'..s.ref.owner)
  return cp(s)
 end
 local function validate(r)
  assert(type(r)=='table' and r.schema==1 and (r.stage=='PREPARED' or r.stage=='ACTIVE' or r.stage=='HELD_TRANSFER')
   and type(r.revision)=='number' and r.revision>=1 and r.revision%1==0,'STORE_SCHEMA')
  assert(type(r.origin)=='table' and type(r.base)=='table' and kinds[r.base.specialization] and r.base.potential==1,'STORE_SCOPE')
  -- Reuse the established bounded structural validator; live pending debit is checked
  -- by EffectiveFacts and InvestmentAction, not interpreted as a fresh import.
  local inv=cp(r.investment);if inv then inv.pending=nil end
  local v={TOKEN=r.base.token,JOURNAL=r.base,FLOW={schema=1,owner=r.base.owner,cityID=r.base.cityID,
   x=r.base.x,y=r.base.y,token=r.base.token,revision=1,stage='DONE',facts=r.base,target=r.base},INVEST=inv}
  assert(M.Preview({ref=r.origin,values=v,ledger=r.binding}).state=='LOCAL_CANDIDATE','STORE_RECORD_INVALID')
  if r.loss then
   assert(r.stage=='HELD_TRANSFER' and same(r.loss.origin,r.origin) and r.loss.evidence=='CityTransfered+live_reference'
    and type(r.loss.target)=='table' and type(r.loss.target.owner)=='number' and r.loss.target.owner>=0
    and r.loss.target.owner~=r.origin.owner and type(r.loss.target.cityID)=='number'
    and r.loss.target.x==r.origin.x and r.loss.target.y==r.origin.y,'STORE_LOSS_EVIDENCE')
  end
  assert(r.stage~='PREPARED' or type(r.source)=='table','STORE_PREPARED_SOURCE')
 end
 -- Called by every old writer before entering player-wide error/repair handling.
 function d.Owns(c)
  if not ready then return true end -- unreadable root: never assume legacy authority
  if not root then return false end
  if type(root)~='table' or type(root.origin)~='table' then return true end
  local r=root.origin
  return c and ((c:GetX()==r.x and c:GetY()==r.y) or (c:GetOwner()==r.owner and c:GetID()==r.cityID)) or false
 end
 local function active(pid,c)
  assert(ready and not fault and root and root.stage=='ACTIVE','PROGRESSION_HELD')
  assert(P.IsTestPlayer(pid) and pid==root.origin.owner and same(ref(c),root.origin),'PROGRESSION_REFERENCE_CHANGED')
  return root
 end
 function d.Base(pid,c)return cp(active(pid,c).base)end
 function d.Investment(pid,c)return cp(active(pid,c).investment)end
 local function save(nextValue)
  assert(not fault,'STORE_WRITE_HELD');validate(nextValue)
  assert(same(Game:GetProperty(KEY),root),'STORE_STALE')
  root=cp(nextValue) -- suppress reentrant legacy writers before engine write
  local ok,err=pcall(function()
   P.SetProperty(Game,KEY,cp(nextValue))
   assert(same(Game:GetProperty(KEY),nextValue),'STORE_WRITE_UNCONFIRMED')
  end)
  if not ok then fault=tostring(err);error(fault)end
 end
 function d.WriteInvestment(pid,c,old,nextValue)
  local r=active(pid,c);assert(same(r.investment,old),'STALE_LEDGER')
  local n=cp(r);n.investment=cp(nextValue);n.revision=n.revision+1;save(n)
 end
 local function activate(c)
  assert(root.stage=='PREPARED' and same(source(c),root.source),'IMPORT_SOURCE_CHANGED')
  assert(P.IsTestPlayer(root.origin.owner),'IMPORT_PLAYER_CHANGED')
  local n=cp(root);n.stage='ACTIVE';n.source=nil;n.revision=n.revision+1;save(n)
 end
 function d.Import(pid,c)
  assert(not busy,'IMPORT_BUSY');busy=true
  local ok,err=pcall(function()
   assert(ready and not fault and c and P.IsTestPlayer(pid) and c:GetOwner()==pid,'SELECT_OWN_CITY')
   if root then assert(same(ref(c),root.origin) and root.stage=='ACTIVE','ONE_CITY_ONLY_OR_HELD');return end
   local s=source(c);assert(M.Preview(s).state=='LOCAL_CANDIDATE','IMPORT_LEGACY_INCOMPLETE')
   assert(kinds[s.values.JOURNAL.specialization],'FOUR_PROFESSIONS_ONLY')
   local f=shared.EffectiveFacts.Read(pid,c);assert(not f.investmentPending,'IMPORT_PENDING')
   save({schema=1,stage='PREPARED',revision=1,origin=cp(s.ref),base=cp(s.values.JOURNAL),
    investment=cp(s.values.INVEST),binding=cp(s.ledger),source=s})
   activate(c)
  end)
  busy=false
  if not ok then return '进度迁移暂停：'..tostring(err)..'\n未回退旧账本；请保留测试档。'end
  return d.Describe(pid,c)
 end
 function d.Describe(pid,c)
  if not ready or fault then return '进度保存暂停：'..tostring(fault or '尚未就绪')..'\n不会使用旧记录补写。'end
  if not root then return '尚未迁移。请选择完整的己方四专业城市，右键“迁移进度”。\n先保留独立的迁移前存档；本批只支持一城同Owner测试。'end
  if root.origin.owner~=pid then return '本记录不属于当前玩家。'end
  if root.stage~='ACTIVE' then return '永久进度保留，能力休眠；退出：'..d.exitStatus..(next(d.exitErrors) and '（暂停模块：'..(function()local t={};for n in pairs(d.exitErrors)do t[#t+1]=n end;table.sort(t);return table.concat(t,'、')end)()..'）' or '')..'\n失城／夺回恢复留后续批次；勿继续投资。'end
  c=c or CityManager.GetCityAt(root.origin.x,root.origin.y)
  local ok,f=pcall(shared.EffectiveFacts.Read,pid,c)
  if not ok then return '进度记录已保存；当前事实未确认：'..tostring(f)end
  return P.VERSION..' | 城市进度保存\n'..f.specialization..' | Potential '..f.potential..' | ACTIVE '..tostring(f.active)
   ..'\n已完成投资：'..f.investmentCount..' | 待完成事务：'..tostring(f.investmentPending)
   ..'\n来源：独立Game记录；旧City账本冻结。\n仅同Owner读档／继续投资；回滚必须使用迁移前存档。'
 end
 local function restore()
  local ok,err=pcall(function()
   root=cp(Game:GetProperty(KEY));if root then validate(root)end;ready=true
  end)
  if not ok then fault=tostring(err);ready=false end
 end
 restore() -- before Binding/Journal/Flow/Investment register load callbacks
 -- No absence/failed getter is confirmation. A matched native ownership event is required.
 function d.IsExitTarget(c,loss)
  if not ready or fault or not root or not root.loss or not loss or not same(loss,root.loss) then return false end
  local ok,r=pcall(ref,c)
  return ok and same(r,loss.target) and r.owner~=root.origin.owner
 end
 function d.RegisterExit(name,fn)
  assert(type(fn)=='function' and not exits[name],'EXIT_REGISTRATION_CONFLICT');exits[name]=fn
 end
 -- Only module-supplied exact IDs: no DB/catalog enumeration or prefix matching.
 function d.RemoveOwned(c,loss,names)
  assert(d.IsExitTarget(c,loss),'EXIT_NOT_CONFIRMED')
  local rows,seen={},{};local buildings=c:GetBuildings()
  for _,name in ipairs(names) do
   assert(not seen[name],'EXIT_DUPLICATE_ID');seen[name]=true
   local row=assert(P.Info('Buildings',name),'EXIT_DEFINITION_MISSING '..name)
   assert(row.InternalOnly==true or row.InternalOnly==1,'EXIT_NON_INTERNAL_BUILDING')
   local has=P.HasBuilding(buildings,row.Index);assert(type(has)=='boolean','EXIT_CARRIER_UNKNOWN')
   rows[#rows+1]={id=row.Index,has=has}
  end
  for _,r in ipairs(rows) do if r.has then
   assert(d.IsExitTarget(c,loss),'EXIT_REFERENCE_CHANGED')
   P.RemoveBuilding(buildings,r.id)
   assert(P.HasBuilding(buildings,r.id)==false,'EXIT_REMOVE_UNCONFIRMED')
  end end
 end
 function d.ExitConfirmed()
  if exitBusy or not ready or fault or not root or not root.loss then return end
  local ok,c=pcall(CityManager.GetCityAt,root.origin.x,root.origin.y)
  if not ok or not c or not d.IsExitTarget(c,root.loss) then d.exitStatus='TARGET_UNAVAILABLE';return end
  exitBusy=true;local names={};for name in pairs(exits)do names[#names+1]=name end
  table.sort(names,function(a,b)if a=='NetworkBridge' then return b~='NetworkBridge' end;if b=='NetworkBridge' then return false end;return a<b end)
  for _,name in ipairs(names)do if not finished[name] and (attempts[name] or 0)<3 then
   attempts[name]=(attempts[name] or 0)+1
   local good,err=pcall(exits[name],c,cp(root.loss))
   if good then finished[name]=true;d.exitErrors[name]=nil else d.exitErrors[name]=tostring(err)end
  end end
  d.exitStatus=#names>0 and 'WITHDRAWN' or 'NO_EXIT_MODULES'
  for _,name in ipairs(names)do if not finished[name] then d.exitStatus='PARTIAL_HELD' end end
  exitBusy=false
 end
 local function reconcile(newOwner,newID,oldOwner)
  if not ready or fault or not root then return end
  local ok,err=pcall(function()
   local c=CityManager.GetCityAt(root.origin.x,root.origin.y)
   if not c then d.observation='UNKNOWN_CITY';return end
   local current=ref(c)
   if type(current.owner)~='number' or current.owner<0 or type(current.cityID)~='number' then d.observation='UNKNOWN_OWNER';return end
   if same(current,root.origin) and root.stage=='PREPARED' then activate(c)
   elseif not root.loss and current.owner~=root.origin.owner and oldOwner==root.origin.owner
    and newOwner==current.owner and newID==current.cityID then
    local n=cp(root);n.stage='HELD_TRANSFER';n.source=nil;n.revision=n.revision+1
    n.loss={origin=cp(root.origin),target=current,evidence='CityTransfered+live_reference'};save(n)
   end
   d.observation='READABLE'
  end)
  if not ok then d.observation='UNKNOWN: '..tostring(err)end
  d.ExitConfirmed()
 end
 local function listen(ns,name,fn)local e=P.Field(ns,name);if e and e.Add then e.Add(fn)end end
 listen(Events,'LoadScreenClose',reconcile)
 -- Bounded single-location observation; no generic publish/playback/hover work.
 listen(Events,'CityTransfered',reconcile)
 for _,name in ipairs({'CityAddedToMap','CityRemovedFromMap','CityInitialized'})do listen(Events,name,function()reconcile()end)end
 listen(GameEvents,'CityBuilt',function()reconcile()end)
end
