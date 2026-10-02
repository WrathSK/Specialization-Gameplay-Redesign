-- P0-K: session facts only. No Property, carrier, yield or persistent ledger writes.
include('GreatWorkCatalog')
include('NetworkInput')
SPCGreatWorkFacts={}
local F=SPCGreatWorkFacts
function F.Hex(s)return (s:gsub('.',function(c)return string.format('%02x',string.byte(c))end))end
function F.Unhex(s)
 assert(#s%2==0 and not s:find('[^0-9a-f]'),'GW_REFERENCE_ENCODING')
 return (s:gsub('..',function(c)return string.char(tonumber(c,16))end))
end
function F.Plan(catalog,works)
 local out={count=0,eraCount=0,eras={},works={},excluded={}}
 for _,w in ipairs(works) do
  local meta=catalog.works[w.type]
  if meta then
   out.count=out.count+1
   if not out.eras[meta.era] then out.eras[meta.era]=0;out.eraCount=out.eraCount+1 end
   out.eras[meta.era]=out.eras[meta.era]+1
   out.works[#out.works+1]={id=w.id,type=w.type,building=w.building,slot=w.slot,era=meta.era,category=meta.category,name=meta.name,eraSource=meta.eraSource}
  else out.excluded[#out.excluded+1]={id=w.id,type=w.type,building=w.building,slot=w.slot,reason=catalog.excluded[w.type] or 'UNSUPPORTED_TYPE'} end
 end
 return out
end
-- One cached building index and one slot read feed both independent interpretations.
function F.Collector(P)
 local ids={};for b in GameInfo.Buildings() do ids[#ids+1]=b.Index end;table.sort(ids)
 return function(c)
  local buildings=c:GetBuildings();local raw,legacy={},{}
  for _,bid in ipairs(ids) do if P.HasBuilding(buildings,bid) then
   local n=buildings:GetNumGreatWorkSlots(bid)
   assert(type(n)=='number' and n>=0 and n%1==0 and n<=256,'GW_SLOT_COUNT')
   for slot=0,n-1 do
    local id=buildings:GetGreatWorkInSlot(bid,slot)
    if id~=nil and id~=-1 then
     assert(type(id)=='number' and id>=0 and id%1==0,'GW_INSTANCE_ID')
     local row=assert(P.Info('GreatWorks',buildings:GetGreatWorkTypeFromIndex(id)),'GW_TYPE_UNAVAILABLE')
     raw[#raw+1]={id=id,type=row.GreatWorkType,building=bid,slot=slot}
     legacy[#legacy+1]={id=id,type=row.GreatWorkType}
     assert(#raw<=4096,'GW_WORK_LIMIT')
    end
   end
  end end
  table.sort(raw,function(a,b)return a.id<b.id end)
  table.sort(legacy,function(a,b)return a.id<b.id end)
  return raw,legacy
 end
end
function F.Start(P,shared)
 if shared.GreatWorkFacts and shared.GreatWorkFacts.Shutdown then shared.GreatWorkFacts.Shutdown()end
 local catalog=SPCGreatWorkCatalog.Build(P)
 -- Engine contexts use this existing monotonic session namespace pattern.
 ExposedMembers.SPC_GreatWorkEpoch=(ExposedMembers.SPC_GreatWorkEpoch or 0)+1
 local d={epoch=ExposedMembers.SPC_GreatWorkEpoch,ack=0,revision=0,state='UNKNOWN',catalogCount=catalog.count,inputRevision=0,dirtyScope={all=true,cities={}}}
 local cities,index={},{};local signature;local hooks={}
 shared.GreatWorkFacts=d
 local function rebuild()
  index={};d.state='VERIFIED'
  if d.dirtyScope.all or next(d.dirtyScope.cities) then d.state='UNKNOWN' end
  for cid,r in pairs(cities) do
   if r.availability~='KNOWN' then d.state='UNKNOWN' end
   for era,n in pairs(r.eras or {}) do
    index[era]=index[era] or {};index[era][cid]=n
   end
  end
 end
 local function invalidate(cid)
  if cities[cid] then
   cities[cid]=nil;signature=nil;d.revision=d.revision+1
   d.inputRevision=d.inputRevision+1;d.dirtyScope.cities[cid]=true;rebuild()
  end
 end
 function d.Reset()
  ExposedMembers.SPC_GreatWorkEpoch=math.max(ExposedMembers.SPC_GreatWorkEpoch or 0,d.epoch)+1
  d.epoch=ExposedMembers.SPC_GreatWorkEpoch;d.ack=0;d.state='UNKNOWN';signature=nil
  for _,r in pairs(cities) do r.availability='UNKNOWN' end
 end
 local function reference(c)
  for _,method in ipairs({'GetOwner','GetID','GetX','GetY'})do
   local v=c[method](c);assert(type(v)=='number' and v>=0 and v%1==0,'GW_CURRENT_REFERENCE_UNKNOWN')
  end
  return SPCNetworkInput.Reference(c)
 end
 local function receive(pid,p)
  assert(p.FactsEpoch==d.epoch,'GW_STALE_EPOCH')
  assert(type(p.Seq)=='number' and p.Seq>0 and p.Seq%1==0,'GW_SEQUENCE')
  if p.Seq<=d.ack then return false end
  d.ack=p.Seq -- processed acknowledgement, never a validity claim
  assert(p.Turn==Game.GetCurrentGameTurn(),'GW_STALE_TURN')
  assert(p.FactsInput==d.inputRevision,'GW_STALE_INPUT')
  assert(type(p.FactsRefs)=='string' and #p.FactsRefs<=200000,'GW_REFERENCE_SIZE')
  assert(type(p.FactsData)=='string' and #p.FactsData<=500000,'GW_SAMPLE_SIZE')
  local candidate,refCount={},0
  for cidText,hex,status in p.FactsRefs:gmatch('(%d+),([0-9a-f]+),([01]);') do
   local cid=tonumber(cidText);assert(not candidate[cid],'GW_DUPLICATE_CITY')
   local c=assert(Players[pid]:GetCities():FindID(cid),'GW_CITY_UNAVAILABLE')
   local ref=F.Unhex(hex)
   assert(reference(c)==ref and c:GetOwner()==pid,'GW_STALE_REFERENCE')
   candidate[cid]={reference=ref,availability=status=='1' and 'KNOWN' or 'UNKNOWN',raw={},name=c:GetName(),owner=pid,x=c:GetX(),y=c:GetY()};refCount=refCount+1
  end
  assert(refCount==p.FactsCities,'GW_CITY_COUNT')
  local canonical={};local ids={};for cid in pairs(candidate)do ids[#ids+1]=cid end;table.sort(ids)
  for _,cid in ipairs(ids)do local r=candidate[cid];canonical[#canonical+1]=cid..','..F.Hex(r.reference)..','..(r.availability=='KNOWN' and '1' or '0')..';'end
  assert(table.concat(canonical)==p.FactsRefs,'GW_REFERENCE_FORMAT')
  local count=0
  for _,c in Players[pid]:GetCities():Members() do count=count+1;assert(count<=512 and c:GetOwner()==pid and candidate[c:GetID()],'GW_INCOMPLETE_SCOPE') end
  assert(count==refCount,'GW_INCOMPLETE_SCOPE')
  local seen,slots,reencoded={},{},{};local workCount=0
  for cidText,bidText,slotText,idText,kind in p.FactsData:gmatch('(%d+),(%d+),(%d+),(%d+),([A-Z0-9_]+);') do
   local cid,bid,slot,id=tonumber(cidText),tonumber(bidText),tonumber(slotText),tonumber(idText)
   local r=assert(candidate[cid],'GW_WORK_CITY');assert(r.availability=='KNOWN','GW_UNKNOWN_WITH_WORKS')
   assert(not seen[id],'GW_DUPLICATE_INSTANCE');seen[id]=true
   local slotkey=cid..':'..bid..':'..slot;assert(not slots[slotkey],'GW_DUPLICATE_SLOT');slots[slotkey]=true
   assert(P.Info('Buildings',bid) and P.Info('GreatWorks',kind),'GW_LOCATION_METADATA')
   workCount=workCount+1;assert(workCount<=4096,'GW_WORK_LIMIT')
   r.raw[#r.raw+1]={id=id,type=kind,building=bid,slot=slot}
   reencoded[#reencoded+1]=cid..','..bid..','..slot..','..id..','..kind..';'
  end
  assert(workCount==p.FactsCount and table.concat(reencoded)==p.FactsData,'GW_WORK_FORMAT')
  local key=p.FactsRefs..'/'..p.FactsData
  if signature==key then
   for cid,r in pairs(cities)do r.availability=candidate[cid].availability end
   d.lastError=nil;d.dirtyScope={all=false,cities={}};rebuild();return true
  end
  for cid,r in pairs(candidate) do
   local old=cities[cid]
   if r.availability=='UNKNOWN' and old and old.reference==r.reference then
    old.availability='UNKNOWN';candidate[cid]=old
   elseif r.availability=='UNKNOWN' then
    r.raw=nil;r.hasConfirmed=false
   else
    local plan=F.Plan(catalog,r.raw);r.raw=nil;r.hasConfirmed=true
    for k,v in pairs(plan)do r[k]=v end
   end
  end
  cities=candidate;signature=key;d.revision=d.revision+1;d.lastError=nil;d.dirtyScope={all=false,cities={}};rebuild();return true
 end
 local function consumerInputs()
  local out={};for cid,r in pairs(cities)do out[cid]={reference=r.reference,eraCount=r.eraCount,availability=r.availability,hasConfirmed=r.hasConfirmed}end;return out
 end
 local function sameInput(a,b)
  return a and b and a.reference==b.reference and a.eraCount==b.eraCount and a.availability==b.availability and a.hasConfirmed==b.hasConfirmed
 end
 function d.Receive(pid,p)
  if not P.IsTestPlayer(pid) then return false,'GW_UNSUPPORTED_OWNER' end
  local before=d.OnConfirmed and consumerInputs()
  local ok,result=pcall(receive,pid,p)
  if not ok then
   d.lastError=tostring(result):match('GW_[A-Z_]+') or 'GW_RECEIVE_ERROR'
   -- Wrong epoch/duplicate packets cannot poison newer confirmed state.
   if p.FactsEpoch==d.epoch and p.Seq==d.ack then d.state='UNKNOWN';for _,r in pairs(cities)do r.availability='UNKNOWN' end;signature=nil end
   return false,d.lastError
  end
  if result and d.OnConfirmed then
   local changed={};local after=consumerInputs()
   for cid,r in pairs(after)do if not sameInput(before[cid],r)then changed[#changed+1]=cid end end
   for cid in pairs(before)do if not after[cid]then changed[#changed+1]=cid end end
   table.sort(changed)
   if #changed>0 then
    local notified=pcall(d.OnConfirmed,pid,changed)
    if not notified then d.consumerError='GW_CONSUMER_UPDATE_FAILED' else d.consumerError=nil end
   end
  end
  return result
 end
 local function current(pid,cid)
  if not P.IsTestPlayer(pid) then return nil end
  local r=cities[cid];if not r then return nil end
  local ok,same=pcall(function()
   local c=Players[pid]:GetCities():FindID(cid)
   if not c then return false end
   local ref=reference(c);return c:GetOwner()==pid and ref==r.reference
  end)
  if ok and not same then invalidate(cid);return nil end
  if not ok then r.availability='UNKNOWN';d.state='UNKNOWN' end
  return r
 end
 local function copy(v)
  if type(v)~='table' then return v end
  local out={};for k,x in pairs(v)do out[k]=copy(x)end;return out
 end
 function d.Read(pid,cid)return copy(current(pid,cid)) end
 function d.Summary(pid,cid)
  local r=current(pid,cid)
  return r and {reference=r.reference,hasConfirmed=r.hasConfirmed,availability=r.availability,eraCount=r.eraCount,count=r.count} or nil
 end
 function d.Domestic(pid,era)
  if not P.IsTestPlayer(pid)then return nil end
  local out={revision=d.revision,availability=d.state,universeComplete=catalog.complete,eras={}}
  for key,source in pairs(index)do if not era or key==era then
   local rows={};for cid,n in pairs(source)do
    local r=current(pid,cid)
    if r then rows[cid]={count=n,reference=r.reference,availability=r.availability,name=r.name}end
   end
   out.eras[key]=rows
  end end
  out.availability=d.state;return out
 end
 local reasons={UNSUPPORTED_TYPE='不在已支持目录',CATEGORY_METADATA='类别元数据变化',ERA_UNAVAILABLE='时代不可确认',UNREVIEWED_ERA='时代不在已审阅来源'}
 local function label(tableName,key)
  local row=P.Info(tableName,key);local name=row and row.Name or key
  return Locale and Locale.Lookup and Locale.Lookup(name) or tostring(name)
 end
 function d.Describe(pid,cid,detail,page)
  local r=current(pid,cid)
  if not r then return '巨作事实：尚未确认本城馆藏。\n等待后台读取；UNKNOWN不是0。' end
  if not r.hasConfirmed then return '巨作事实：本城馆藏尚未确认。\nUNKNOWN不是0；等待后台复核。' end
  local lines={'巨作事实｜'..(Locale and Locale.Lookup and Locale.Lookup(r.name) or r.name)..'｜'..(r.availability=='KNOWN' and '已确认' or '待复核（保留最近确认值）'),
   '合格 '..r.count..' 件｜覆盖 '..r.eraCount..' 个历史时代'}
  local eras={};for era in pairs(r.eras)do eras[#eras+1]=era end;table.sort(eras)
  for _,era in ipairs(eras)do lines[#lines+1]=label('Eras',era)..'：'..r.eras[era]..' 件'end
  if #r.excluded>0 then
   local counts={};for _,w in ipairs(r.excluded)do counts[w.reason]=(counts[w.reason] or 0)+1 end
   local reasonsList={};for why,n in pairs(counts)do reasonsList[#reasonsList+1]=(reasons[why] or why)..' '..n end;table.sort(reasonsList)
   lines[#lines+1]='排除 '..#r.excluded..' 件：'..table.concat(reasonsList,'；')
  end
  if detail then
   local rows={}
   for _,w in ipairs(r.works)do rows[#rows+1]=label('GreatWorks',w.type)..' → '..label('Eras',w.era)..'｜'..w.category:gsub('GREATWORKOBJECT_','')..'｜建筑'..w.building..'/槽位'..w.slot end
   for _,w in ipairs(r.excluded)do rows[#rows+1]=label('GreatWorks',w.type)..'：'..(reasons[w.reason] or w.reason) end
   local universe={};for era in pairs(catalog.eras)do universe[#universe+1]=era end;table.sort(universe)
   for _,era in ipairs(universe)do
    local sources={};for cityID,n in pairs(index[era] or {})do
     local other=current(pid,cityID)
     if other then sources[#sources+1]=(Locale and Locale.Lookup and Locale.Lookup(other.name) or other.name)..' '..n..'件' end
    end
    table.sort(sources)
    rows[#rows+1]=label('Eras',era)..' 国内来源：'..(#sources>0 and table.concat(sources,'、') or (d.state=='VERIFIED' and catalog.complete and '无' or '未确认'))
   end
   local pages=math.max(1,math.ceil(#rows/6));local number=((page or 1)-1)%pages+1
   lines[#lines+1]='作品 / 国内来源 '..number..'/'..pages..'（右键继续）'
   for i=(number-1)*6+1,math.min(#rows,number*6)do lines[#lines+1]=rows[i]end
  end
  if d.state~='VERIFIED' or not catalog.complete then lines[#lines+1]='国内来源尚未完全确认；不将缺项判为不存在。' end
  if d.lastError then lines[#lines+1]='待复核：'..d.lastError end
  return table.concat(lines,'\n')
 end
 local store=shared.CityProgressionStore
 if store then
  store.RegisterExit('GreatWorkFacts',function(c,loss)
   assert(store.IsExitTarget(c,loss),'GW_EXIT_UNCONFIRMED')
   -- Confirmed E2 identity/loss is the authority. origin ID may predate recapture.
   -- Only cached locations of this confirmed target are withdrawn; no new city identity.
   local removed=false
   for cid,r in pairs(cities)do
    if r.owner==loss.origin.owner and r.x==c:GetX() and r.y==c:GetY() then invalidate(cid);removed=true end
   end
   if removed then d.Reset() end
  end)
  store.RegisterReturn('GreatWorkFacts',function()d.Reset()end)
 end
 local function bind(name,fn)
  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn}end
 end
 local function changed(pid,cid)
  if not P.IsTestPlayer(pid)then return end
  d.inputRevision=d.inputRevision+1;d.state='UNKNOWN'
  if cid then d.dirtyScope.cities[cid]=true;if cities[cid]then cities[cid].availability='UNKNOWN'end
  else d.dirtyScope.all=true;for _,r in pairs(cities)do r.availability='UNKNOWN'end end
 end
 for _,name in ipairs({'CityAddedToMap','CityRemovedFromMap'})do
  bind(name,function(pid,cid)changed(pid,type(cid)=='number' and cid or nil)end)
 end
 bind('GreatWorkMoved',function(op,oc,dp,dc)
  changed(op,type(oc)=='number' and oc or nil);changed(dp,type(dc)=='number' and dc or nil)
 end)
 bind('GreatWorkCreated',function(pid,creator,x,y)
  if not P.IsTestPlayer(pid)then return end
  local ok,c=pcall(CityManager.GetCityAt,x,y)
  changed(pid,ok and c and c:GetOwner()==pid and c:GetID() or nil)
 end)
 function d.Shutdown()
  for _,h in ipairs(hooks)do if h.event.Remove then h.event.Remove(h.fn)end end
  hooks={};cities={};index={};d.OnConfirmed=nil
  if shared.GreatWorkFacts==d then shared.GreatWorkFacts=nil end
 end
 return d
end
