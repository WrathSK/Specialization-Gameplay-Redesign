-- E2 first slice: one explicit same-owner progression cutover. Not a global city registry.
SPCCityProgressionStore={KEY='SPC_CITY_PROGRESSION_E2_V1'}
function SPCCityProgressionStore.Start(P,shared)
 local M=SPCCityIdentityRead;local cp=M.Copy;local KEY=SPCCityProgressionStore.KEY
 local d={exitStatus="NOT_CONFIRMED",exitErrors={}};shared.CityProgressionStore=d
 local exits,finished,attempts={},{},{};local exitBusy=false;local runningExit;local exitReads={}
 local returns={};function d.RegisterReturn(name,fn)assert(not returns[name]);returns[name]=fn end
 -- Fixed latest slot per native event; session-only evidence, never identity authority.
 local eventNames={'CityTransfered','CityConquered','CityAddedToMap','CityRemovedFromMap','CityInitialized','CityBuilt'}
 local nativeEvents={};local eventSequence=0
 local root,fault,busy;local ready=false
 local foreignSeen=false;local transition;local transitionFault;local conquest;local foundation
 local function observe(name,...)
  if not root then return end
  eventSequence=eventSequence+1
  local row={sequence=eventSequence,turn=Game.GetCurrentGameTurn(),argc=select('#',...)}
  for i=1,math.min(6,row.argc)do
   local v=select(i,...);local t=type(v)
   if t=='number' or t=='boolean' then row[i]=v else row[i]=t=='nil' and 'nil' or '<'..t..'>' end
  end
  nativeEvents[name]=row
 end
 local kinds={RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a) do if not same(v,b[k]) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function validTransition(proof,loss,current)
  if type(proof)~='table' or (proof.version~=1 and proof.version~=2) or not loss or not same(proof.from,loss.target)
   or not same(proof.to,current) or type(proof.turn)~='number' or proof.turn<0 or proof.turn%1~=0 then return false end
  local r,a,i,t=proof.removed,proof.added,proof.initialized,proof.transferred
  if not (type(r)=='number' and type(a)=='number' and type(i)=='number' and type(t)=='number'
   and r>=1 and r%1==0 and a%1==0 and i%1==0 and t%1==0 and r<a and a<i and i<t) then return false end
  if proof.version==2 then
   local c,b=proof.conquest,proof.foundation
   if type(c)~='table' or type(b)~='table' or c.fromOwner~=loss.target.owner or not same(c.to,current)
    or not same(b.to,current) or c.turn~=proof.turn or b.turn~=proof.turn then return false end
   local cs,bs=c.sequence,b.sequence
   return type(cs)=='number' and type(bs)=='number' and cs>=1 and bs>=1 and cs%1==0 and bs%1==0 and cs<r and bs<t
  end
  return true
 end
 local function source(c)
  local s={ref=ref(c),values={}}
  for _,n in ipairs({'TOKEN','JOURNAL','FLOW','INVEST','TEMPLATES'}) do s.values[n]=c:GetProperty(M.Keys[n])end
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
   x=r.base.x,y=r.base.y,token=r.base.token,revision=1,stage='DONE',facts=r.base,target=r.base},INVEST=inv,TEMPLATES=r.templates}
  assert(M.Preview({ref=r.origin,values=v,ledger=r.binding}).state=='LOCAL_CANDIDATE','STORE_RECORD_INVALID')
  if r.current then
   assert((r.returnEvidence=='CityTransfered+original_binding' or (r.returnEvidence=='NATIVE_TRANSITION_V1' and validTransition(r.returnProof,r.lastLoss,r.current))) and r.lastLoss and same(r.lastLoss.origin,r.origin)
    and r.lastLoss.target.owner~=r.origin.owner and type(r.currentFirst)=='table' and r.currentFirst.turn==r.base.first.turn
    and r.current.owner==r.origin.owner and type(r.current.cityID)=='number' and r.current.cityID>=0 and r.current.cityID%1==0
    and r.current.x==r.origin.x and r.current.y==r.origin.y and type(r.currentFirst)=='table'
    and r.currentFirst.type==r.base.first.type and type(r.currentFirst.districtID)=='number','STORE_CURRENT_REFERENCE')
  end
  if r.loss then
   assert(r.stage=='HELD_TRANSFER' and same(r.loss.origin,r.origin) and r.loss.evidence=='CityTransfered+live_reference'
    and type(r.loss.target)=='table' and type(r.loss.target.owner)=='number' and r.loss.target.owner>=0
    and r.loss.target.owner~=r.origin.owner and type(r.loss.target.cityID)=='number'
    and r.loss.target.x==r.origin.x and r.loss.target.y==r.origin.y,'STORE_LOSS_EVIDENCE')
  end
  assert(r.referenceInvalidated==nil or r.referenceInvalidated==true,'STORE_REFERENCE_INVALIDATION')
  assert(r.stage~='PREPARED' or type(r.source)=='table','STORE_PREPARED_SOURCE')
 end
 -- Called by every old writer before entering player-wide error/repair handling.
 function d.Owns(c)
  if not ready then return true end -- unreadable root: never assume legacy authority
  if not root then return false end
  if type(root)~='table' or type(root.origin)~='table' then return true end
  local r=root.origin
  return c and c:GetX()==r.x and c:GetY()==r.y or false -- old cityID may be reused elsewhere
 end
 function d.IsRecaptured(c)return root and root.current~=nil and d.Owns(c) or false end
 local function active(pid,c)
  assert(ready and not fault and root and root.stage=='ACTIVE','PROGRESSION_HELD')
  assert(P.IsTestPlayer(pid) and pid==root.origin.owner and same(ref(c),root.current or root.origin),'PROGRESSION_REFERENCE_CHANGED')
  assert(not root.referenceInvalidated,'PROGRESSION_REFERENCE_REMOVED')
  if root.current then
   local token=c:GetProperty(M.Keys.TOKEN)
   if root.returnEvidence=='NATIVE_TRANSITION_V1' then
    assert(validTransition(root.returnProof,root.lastLoss,root.current) and (token==nil or token==root.base.token),'PROGRESSION_BINDING_CONFLICT')
   else assert(token==root.base.token,'PROGRESSION_BINDING_UNAVAILABLE')end
  end
  return root
 end
 local function projected(r,v,investment)
  v=cp(v);if not v or not r.current then return v end
  local a=investment and v.anchor or v;a.cityID=r.current.cityID;a.first=cp(r.currentFirst)
  return v
 end
 function d.Base(pid,c)local r=active(pid,c);return projected(r,r.base,false)end
 function d.Investment(pid,c)local r=active(pid,c);return projected(r,r.investment,true)end
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
 -- Session-only transition assembly. Never reconstruct an incomplete chain at load.
 local function track(name,owner,id,x,y)
  if not ready or fault or not root then return end
  local current=root.current or root.origin
  if name=='CityRemovedFromMap' and root.stage=='ACTIVE' and owner==current.owner and id==current.cityID then
   if not root.referenceInvalidated then local n=cp(root);n.referenceInvalidated=true;n.revision=n.revision+1;save(n)end
  end
  if not root.loss or root.stage~='HELD_TRANSFER' then return end
  local old=root.loss.target;local turn=Game.GetCurrentGameTurn()
  if name=='CityRemovedFromMap' and owner==old.owner and id==old.cityID then
   if not foreignSeen then transitionFault='RETURN_FOREIGN_REFERENCE_UNOBSERVED';return end
   if transition then
    if transition.turn~=turn then transitionFault='RETURN_CHAIN_CONFLICT'end
    return -- identical repeated removal is not another generation
   end
   transition={version=1,from=cp(old),turn=turn,removed=eventSequence}
  elseif (name=='CityAddedToMap' or name=='CityInitialized') and x==old.x and y==old.y then
   if not transition then transitionFault='RETURN_CHAIN_ORDER';return end
   if transition.turn~=turn or owner~=root.origin.owner or type(id)~='number' or id<0 or id%1~=0 then
    transitionFault='RETURN_CHAIN_CONFLICT';return
   end
   local endpoint={owner=owner,cityID=id,x=x,y=y}
   if transition.to and not same(transition.to,endpoint) then transitionFault='RETURN_CHAIN_CONFLICT';return end
   transition.to=endpoint
   if name=='CityAddedToMap' then
    if not transition.added then transition.added=eventSequence end
   elseif not transition.added then transitionFault='RETURN_CHAIN_ORDER'
   elseif not transition.initialized then transition.initialized=eventSequence end
  elseif name=='CityRemovedFromMap' and transition and transition.to
   and owner==transition.to.owner and id==transition.to.cityID then transitionFault='RETURN_CHAIN_TARGET_REMOVED'
  elseif name=='CityBuilt' and x==old.x and y==old.y then
   local row={to={owner=owner,cityID=id,x=x,y=y},turn=turn,sequence=eventSequence}
   if foundation and (not same(foundation.to,row.to) or foundation.turn~=turn) then transitionFault='RETURN_FOUNDATION_CONFLICT'
   elseif not foundation then foundation=row end
  end
 end
 local function trackConquest(newOwner,oldOwner,newID,x,y)
  if not ready or fault or not root or not root.loss or root.stage~='HELD_TRANSFER' then return end
  local old=root.loss.target
  if x~=old.x or y~=old.y then return end
  if newOwner~=root.origin.owner or oldOwner~=old.owner or type(newID)~='number' or newID<0 or newID%1~=0 then
   transitionFault='RETURN_CONQUEST_CONFLICT';return
  end
  local row={fromOwner=oldOwner,to={owner=newOwner,cityID=newID,x=x,y=y},turn=Game.GetCurrentGameTurn(),sequence=eventSequence}
  if conquest and (not same(conquest.to,row.to) or conquest.turn~=row.turn) then transitionFault='RETURN_CONQUEST_CONFLICT'
  elseif not conquest then conquest=row end
 end
 local function trackSafely(name,...)
  local ok=pcall(track,name,...)
  if not ok then transitionFault='RETURN_CHAIN_READ_FAILED' end
 end
 function d.WriteInvestment(pid,c,old,nextValue)
  local r=active(pid,c);assert(same(projected(r,r.investment,true),old),'STALE_LEDGER')
  local n=cp(r);n.investment=cp(nextValue);if n.investment then n.investment.anchor.cityID=r.origin.cityID;n.investment.anchor.first=cp(r.base.first)end;n.revision=n.revision+1;save(n)
 end
 -- Only the existing Standardization module owns interpretation of this ledger.
 function d.ReadTemplates(c)
  local r=active(c:GetOwner(),c)
  if not r.templatesCaptured then
   assert(not r.current,'TEMPLATES_HISTORY_UNAVAILABLE')
   local n=cp(r);n.templates=c:GetProperty(M.Keys.TEMPLATES);n.templatesCaptured=true;n.revision=n.revision+1;save(n)
  end
  assert(not root.current or root.base.specialization~='INDUSTRY' or root.templates~=nil,'TEMPLATES_HISTORY_UNAVAILABLE')
  return cp(root.templates)
 end
 function d.WriteTemplates(c,old,value)
  local r=active(c:GetOwner(),c);assert(r.templatesCaptured and same(r.templates,old),'TEMPLATES_STALE')
  local n=cp(r);n.templates=cp(value);n.revision=n.revision+1;save(n)
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
   if root then assert(same(ref(c),root.current or root.origin) and root.stage=='ACTIVE','ONE_CITY_ONLY_OR_HELD');return end
   local s=source(c);assert(M.Preview(s).state=='LOCAL_CANDIDATE','IMPORT_LEGACY_INCOMPLETE')
   assert(kinds[s.values.JOURNAL.specialization],'FOUR_PROFESSIONS_ONLY')
   local f=shared.EffectiveFacts.Read(pid,c);assert(not f.investmentPending,'IMPORT_PENDING')
   save({schema=1,stage='PREPARED',revision=1,origin=cp(s.ref),base=cp(s.values.JOURNAL),
    investment=cp(s.values.INVEST),binding=cp(s.ledger),templates=cp(s.values.TEMPLATES),templatesCaptured=true,source=s})
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
  if root.stage~='ACTIVE' then return '永久进度保留，能力休眠；退出：'..d.exitStatus..(next(d.exitErrors) and '（暂停模块：'..(function()local t={};for n in pairs(d.exitErrors)do t[#t+1]=n end;table.sort(t);return table.concat(t,'、')end)()..'）' or '')..'\n恢复：'..((d.observation or ''):match('RETURN_[A-Z_]+') or '等待匹配夺回事件')..'；未确认时勿投资。'end
  c=c or CityManager.GetCityAt(root.origin.x,root.origin.y)
  local ok,f=pcall(shared.EffectiveFacts.Read,pid,c)
  if not ok then return '进度记录已保存；当前事实未确认：'..tostring(f)end
  return P.VERSION..' | 城市进度保存\n'..f.specialization..' | Potential '..f.potential..' | ACTIVE '..tostring(f.active)
   ..'\n已完成投资：'..f.investmentCount..' | 待完成事务：'..tostring(f.investmentPending)
   ..'\n来源：独立Game记录；旧City账本冻结。\nACTIVE依当前事实；Network等待当前路线；回滚使用迁移前存档。'
 end
 -- On-demand evidence only. No state writes, refresh, requests or effect application.
 function d.NativeDescribe(pid)
  local ok,out=pcall(function()
   if not root or not ready or fault then return d.Describe(pid)end
   assert(pid==root.origin.owner and P.IsTestPlayer(pid),'E2_WRONG_PLAYER')
   local function label(r)return r and (tostring(r.owner)..'/'..tostring(r.cityID)..' @'..tostring(r.x)..','..tostring(r.y)) or 'NONE'end
   local city=CityManager.GetCityAt(root.origin.x,root.origin.y)
   local readable,live=pcall(ref,city)
   local tokenOK,token=pcall(function()return city:GetProperty(M.Keys.TOKEN)end)
   local receipts=0;for _ in pairs(root.investment and root.investment.investments or {})do receipts=receipts+1 end
   local done,total,checked,removed=0,0,0,0
   for name in pairs(exits)do total=total+1;if finished[name]then done=done+1 end end
   for _,v in pairs(exitReads)do checked=checked+v.checked;removed=removed+v.removed end
   local fOK,f=pcall(shared.EffectiveFacts.Read,pid,city)
   local net=shared.NetworkBridge;local b=net and net.players[pid];local ids={root.origin.cityID}
   if root.current then ids[#ids+1]=root.current.cityID end
   local source,receiver=false,false
   if b then for _,id in ipairs(ids)do
    source=source or (b.sources and b.sources[id]~=nil) or false
    for _,set in pairs(b.recipients or {})do receiver=receiver or set[id]~=nil end
   end end
   local input;local inputState='NO_CURRENT_INPUT'
   if readable and live.owner~=pid then inputState='FOREIGN_OWNER_NOT_QUERIED'
   elseif readable then
    local candidate=b and b.input and b.input.cities and b.input.cities[live.cityID]
    local good,reference=pcall(function()return SPCNetworkInput.Reference(city)end)
    if candidate and good and candidate.reference==reference then input=candidate;inputState='MATCHED'
    elseif candidate then inputState='REFERENCE_MISMATCH' end
   end
   local detail={}
   local errors={};for name in pairs(d.exitErrors)do errors[#errors+1]=name end;table.sort(errors)
   for _,name in ipairs(errors)do
    local reason=tostring(d.exitErrors[name]):gsub('[\r\n]+',' '):sub(1,160)
    detail[#detail+1]='退出失败 '..name..' ['..tostring(attempts[name])..'/3] '..reason
   end
   detail[#detail+1]='事件为本次加载后各类最后一次；原始参数，不自动认领：'
   for _,name in ipairs(eventNames)do
    local row=nativeEvents[name]
    if row then
     local args={};for i=1,math.min(6,row.argc)do args[i]=tostring(row[i])end
     detail[#detail+1]='#'..row.sequence..' T'..row.turn..' '..name..'('..table.concat(args,',')..') argc='..row.argc
    end
   end
   if eventSequence==0 then detail[#detail+1]='本次加载未收到上述事件'end
   local binding=not tokenOK and 'UNREADABLE' or token==nil and 'MISSING' or token==root.base.token and 'MATCH' or 'MISMATCH'
   local gate=root.referenceInvalidated and root.stage=='ACTIVE' and 'REFERENCE_REMOVED' or root.stage~='HELD_TRANSFER' and 'NOT_HELD' or not readable and 'CURRENT_REFERENCE_UNREADABLE'
    or live.owner~=root.origin.owner and 'STILL_FOREIGN' or d.returnRejection or 'WAIT_MATCHING_TRANSFER_EVENT'
   local function carrierCount(names)
    if not city then return 'UNKNOWN'end
    local good,n=pcall(function()local count=0;for _,name in ipairs(names)do
     local row=assert(P.Info('Buildings',name));local has=P.HasBuilding(city:GetBuildings(),row.Index)
     assert(type(has)=='boolean');if has then count=count+1 end
    end;return count end);return good and tostring(n) or 'UNKNOWN'
   end
   local housing,gpp={},{};for i=0,8 do housing[#housing+1]='BUILDING_SPC_DEV_LV2_HOUSING_'..i end
   for i=0,7 do gpp[#gpp+1]='BUILDING_SPC_DEV_GPP_RESEARCH_'..i end
   local result=table.concat({P.VERSION..' | E2往返 | T'..Game.GetCurrentGameTurn()..' | '..root.stage,
    '原引用 '..label(root.origin)..' | record rev '..root.revision,
    '原凭据 '..root.base.token..' | 当前匹配 '..binding..' | 恢复依据 '..tostring(root.returnEvidence or '尚未确认'),
    '当前 '..(readable and label(live) or 'UNKNOWN')..' | token '..(tokenOK and tostring(token) or 'UNKNOWN'),
    '永久 '..root.base.specialization..' | Potential '..(1+receipts)..' | 投资 '..receipts,
    '当前ACTIVE '..(fOK and tostring(f.active)..' / '..tostring(f.activeStatus) or '未激活/UNKNOWN'),
    '失城确认 '..(root.loss and label(root.loss.target) or root.lastLoss and ('历史 '..label(root.lastLoss.target)) or 'NONE'),
    '退出 '..d.exitStatus..' | 完成 '..done..'/'..total..' | 核验ID '..checked..' / 移除 '..removed,
    '最近转移 '..(d.lastTransfer or '本次加载未收到'),
    '夺回 '..(root.current and root.stage=='ACTIVE' and not root.referenceInvalidated and 'ACCEPTED' or gate)..' | 最近候选 '..(d.returnCandidate or 'NONE'),
    '转移链 '..(transitionFault or (transition and (transition.initialized and 'READY' or 'INCOMPLETE') or 'NONE'))..' | CityBuilt '..(foundation and (conquest and '待核对征服' or '缺少征服佐证') or 'NONE'),
    '科研实存carrier：支持 '..carrierCount({'BUILDING_SPC_DEV_RESEARCH_SUPPORT'})..' / 住房 '..carrierCount(housing)..' / GPP '..carrierCount(gpp),
    'Network '..(b and b.validity or 'UNKNOWN')..' | epoch '..tostring(net and net.epoch)..' / input '..tostring(b and b.inputRevision)..' / derive '..tostring(b and b.derivedRevision),
    '旧/现本城 source '..tostring(source)..' / receiver '..tostring(receiver)..' | routes '..tostring(b and b.routes and #b.routes or 'UNKNOWN'),
    'Network当前引用 '..inputState..' | '..tostring(input and input.reference or 'NONE')..' | ACTIVE '..tostring(input and input.active or 'NONE'),
    table.concat(detail,'\n'),
    '载体读数≠引擎收益验证；请配合城市收益截图。'},'\n')
   return result
  end)
  local report=ok and out or ('E2诊断 UNKNOWN：'..tostring(out))
  print('[SPC][E2_NATIVE] '..report);return report
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
  local found=0;for _,r in ipairs(rows)do if r.has then found=found+1 end end
  for _,r in ipairs(rows) do if r.has then
   assert(d.IsExitTarget(c,loss),'EXIT_REFERENCE_CHANGED')
   P.RemoveBuilding(buildings,r.id)
   assert(P.HasBuilding(buildings,r.id)==false,'EXIT_REMOVE_UNCONFIRMED')
  end end
  if runningExit then exitReads[runningExit]={checked=#rows,removed=found}end
 end
 function d.ExitConfirmed()
  if exitBusy or not ready or fault or not root or not root.loss then return end
  local ok,c=pcall(CityManager.GetCityAt,root.origin.x,root.origin.y)
  if not ok or not c or not d.IsExitTarget(c,root.loss) then d.exitStatus='TARGET_UNAVAILABLE';return end
  foreignSeen=true
  exitBusy=true;local names={};for name in pairs(exits)do names[#names+1]=name end
  table.sort(names,function(a,b)if a=='NetworkBridge' then return b~='NetworkBridge' end;if b=='NetworkBridge' then return false end;return a<b end)
  for _,name in ipairs(names)do if not finished[name] and (attempts[name] or 0)<3 then
   attempts[name]=(attempts[name] or 0)+1
   runningExit=name;local good,err=pcall(exits[name],c,cp(root.loss));runningExit=nil
   if good then finished[name]=true;d.exitErrors[name]=nil else d.exitErrors[name]=tostring(err)end
  end end
  d.exitStatus=#names>0 and 'WITHDRAWN' or 'NO_EXIT_MODULES'
  for _,name in ipairs(names)do if not finished[name] then d.exitStatus='PARTIAL_HELD' end end
  exitBusy=false
 end
 local function recapture(c,current,newOwner,newID,oldOwner)
  if not root.loss or root.stage~='HELD_TRANSFER' or newOwner~=root.origin.owner
   or oldOwner~=root.loss.target.owner or newID~=current.cityID or current.owner~=newOwner then return false end
  d.returnCandidate=current.owner..'/'..current.cityID..' from '..tostring(oldOwner)
  d.returnRejection=nil -- latest matched attempt; diagnostics only
  assert(P.IsTestPlayer(newOwner),'RETURN_PLAYER_UNCONFIRMED')
  local token=c:GetProperty(M.Keys.TOKEN);local proof
  if token~=root.base.token then
   assert(token==nil,'RETURN_BINDING_CONFLICT')
   assert(not transitionFault,transitionFault)
   assert(foreignSeen and transition,'RETURN_CHAIN_MISSING')
   proof=cp(transition);proof.transferred=eventSequence
   if foundation then
    assert(conquest,'RETURN_NEW_FOUNDATION')
    proof.version=2;proof.conquest=cp(conquest);proof.foundation=cp(foundation)
    assert(validTransition(proof,root.loss,current),'RETURN_FOUNDATION_CONFLICT')
   elseif conquest then
    assert(conquest.turn==proof.turn and conquest.fromOwner==root.loss.target.owner and same(conquest.to,current)
     and conquest.sequence<proof.removed,'RETURN_CONQUEST_CONFLICT')
   end
   assert(proof.turn==Game.GetCurrentGameTurn() and validTransition(proof,root.loss,current),'RETURN_CHAIN_INCOMPLETE')
  end
  local count=0;for name in pairs(exits)do count=count+1;assert(finished[name],'RETURN_WITHDRAWAL_UNCONFIRMED')end
  assert(count>0,'RETURN_WITHDRAWAL_UNCONFIRMED')
  assert(not root.investment or root.investment.pending==nil,'RETURN_PENDING_INVESTMENT')
  -- Rebind the current district reference, never invent new historical completion.
  local first
  for _,district in Players[newOwner]:GetDistricts():Members()do
   local city=district:GetCity();local row=P.Info('Districts',district:GetType())
   if city and same(ref(city),current) and row and row.DistrictType==root.base.first.type and district:IsComplete() then
    assert(not first,'RETURN_DISTRICT_AMBIGUOUS');first=cp(root.base.first);first.districtID=district:GetID()
   end
  end
  assert(first,'RETURN_DISTRICT_UNAVAILABLE')
  local n=cp(root)
  if n.base.specialization=='INDUSTRY' then
   -- Never backfill AI-era buildings as player history. B096 saves without a
   -- pre-loss template snapshot remain held rather than guessing an empty ledger.
   if n.templatesCaptured and n.templates then
    assert(shared.Standardization and shared.Standardization.ValidateRetained,'RETURN_TEMPLATE_VALIDATOR_UNAVAILABLE')
    shared.Standardization.ValidateRetained(c,n.templates)
   end -- missing pre-loss history holds Standardization reads, not Identity/Potential
  end
  -- Reset samples/quotes before making facts available. No callback applies yields.
  for _,fn in pairs(returns)do fn(root.origin.owner,c)end
  n.lastLoss=n.loss;n.loss=nil;n.stage='ACTIVE';n.current=current;n.currentFirst=first;n.returnEvidence=proof and 'NATIVE_TRANSITION_V1' or 'CityTransfered+original_binding';n.returnProof=proof;n.referenceInvalidated=nil
  n.revision=n.revision+1;save(n)
  finished={};attempts={};transition=nil;transitionFault=nil;conquest=nil;foundation=nil;foreignSeen=false;d.exitErrors={};d.exitStatus='NOT_CONFIRMED';d.returnStatus='CONFIRMED_CURRENT_FACTS_REQUIRED'
  return true
 end
 local function reconcile(newOwner,newID,oldOwner)
  if not ready or fault or not root then return end
  if newOwner~=nil then d.lastTransfer=tostring(oldOwner)..' → '..tostring(newOwner)..'/'..tostring(newID)end
  local ok,err=pcall(function()
   local c=CityManager.GetCityAt(root.origin.x,root.origin.y)
   if not c then d.observation='UNKNOWN_CITY';return end
   local current=ref(c)
   if type(current.owner)~='number' or current.owner<0 or type(current.cityID)~='number' then d.observation='UNKNOWN_OWNER';return end
   if recapture(c,current,newOwner,newID,oldOwner) then return
   elseif same(current,root.origin) and root.stage=='PREPARED' then activate(c)
   elseif not root.loss and current.owner~=root.origin.owner and oldOwner==root.origin.owner
    and newOwner==current.owner and newID==current.cityID then
    local n=cp(root);n.stage='HELD_TRANSFER';n.source=nil;n.revision=n.revision+1
    n.loss={origin=cp(root.origin),target=current,evidence='CityTransfered+live_reference'};save(n)
    finished={};attempts={};d.exitErrors={};transition=nil;transitionFault=nil;conquest=nil;foundation=nil;foreignSeen=false
   end
   d.observation='READABLE'
  end)
  if not ok then d.observation='UNKNOWN: '..tostring(err);d.returnRejection=tostring(err):match('RETURN_[A-Z_]+') or d.returnRejection end
  d.ExitConfirmed()
 end
 local function listen(ns,name,fn)local e=P.Field(ns,name);if e and e.Add then e.Add(fn)end end
 listen(Events,'LoadScreenClose',reconcile)
 -- Bounded single-location observation; no generic publish/playback/hover work.
 listen(Events,'CityTransfered',function(...)pcall(observe,'CityTransfered',...);reconcile(...)end)
 -- Conquest is supporting evidence only; never accepts without the full transfer chain.
 listen(GameEvents,'CityConquered',function(...)
  pcall(observe,'CityConquered',...)
  if not pcall(trackConquest,...) then transitionFault='RETURN_CHAIN_READ_FAILED'end
 end)
 for _,name in ipairs({'CityAddedToMap','CityRemovedFromMap','CityInitialized'})do
  listen(Events,name,function(...)pcall(observe,name,...);trackSafely(name,...);reconcile()end)
 end
 listen(GameEvents,'CityBuilt',function(...)pcall(observe,'CityBuilt',...);trackSafely('CityBuilt',...);reconcile()end)
end
