-- E2 first slice: one explicit same-owner progression cutover. Not a global city registry.
SPCCityProgressionStore={KEY='SPC_CITY_PROGRESSION_E2_V1'}
function SPCCityProgressionStore.Start(P,shared)
 local M=SPCCityIdentityRead;local cp=M.Copy;local KEY=SPCCityProgressionStore.KEY
 local d={};shared.CityProgressionStore=d
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
  if root.stage~='ACTIVE' then return '进度记录保留，当前暂停：'..root.stage..'\n失城／夺回恢复留后续批次；勿继续投资。'end
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
 local function reconcile()
  if not ready or fault or not root then return end
  local ok,err=pcall(function()
   local c=CityManager.GetCityAt(root.origin.x,root.origin.y)
   if c and same(ref(c),root.origin) and root.stage=='PREPARED' then activate(c)
   elseif not c or not same(ref(c),root.origin) then
    if root.stage~='HELD_TRANSFER' then local n=cp(root);n.stage='HELD_TRANSFER';n.source=nil;n.revision=n.revision+1;save(n)end
   end
  end)
  if not ok then fault=tostring(err)end
 end
 local function listen(ns,name,fn)local e=P.Field(ns,name);if e and e.Add then e.Add(fn)end end
 listen(Events,'LoadScreenClose',reconcile)
 -- Bounded single-location observation; no generic publish/playback/hover work.
 for _,name in ipairs({'CityTransfered','CityAddedToMap','CityRemovedFromMap','CityInitialized'})do listen(Events,name,reconcile)end
 listen(GameEvents,'CityBuilt',reconcile)
end
