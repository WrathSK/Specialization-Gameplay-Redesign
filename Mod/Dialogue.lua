include('DialogueModel')
include('NetworkInput')
SPCDialogue={}
function SPCDialogue.Start(P,shared)
 local d={ready=false,busy=false,seq={},samples={},paired={},off={},test={},last={},errors={},changes=0,received={},generation=1};shared.Dialogue=d
 local levels={};for _ in GameInfo.Eras() do levels[#levels+1]=true end
 local function set(c,id,want)
  local row=assert(P.Info('Buildings',id),'DIALOGUE_DATABASE_MISSING');local b=c:GetBuildings()
  if P.HasBuilding(b,row.Index)~=want then
   if want then P.CreateBuilding(c:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index) end
   assert(P.HasBuilding(b,row.Index)==want,'DIALOGUE_WRITE_FAILED');d.changes=d.changes+1
  end
 end
 function d.Init()
  if d.ready then return end
  assert(not d.initializing,'DIALOGUE_INIT_BUSY');d.initializing=true
  local ok,why=pcall(function()
   for _,p in pairs(Players) do local cities=p:GetCities();if cities then for _,c in cities:Members() do P.Count('city_scan');
    for n=2,#levels do local id='BUILDING_SPC_B059_D'..n;if P.Info('Buildings',id) then set(c,id,false) end end
    for _,v in ipairs({25,50,100,200}) do local id='BUILDING_SPC_B059_TEST'..v;if P.Info('Buildings',id) then set(c,id,false) end end
    for _,m in ipairs({'CITY','OBJECT'}) do local id='BUILDING_SPC_B055_GW_'..m;if P.Info('Buildings',id) then set(c,id,false) end end
   end end end
  end)
  d.initializing=false -- Only the invocation which acquired this lock releases it.
  if not ok then error(why)end
  d.ready=true
 end
 local owned={};for n=2,#levels do owned['BUILDING_SPC_B059_D'..n]=true end
 for _,v in ipairs({25,50,100,200})do owned['BUILDING_SPC_B059_TEST'..v]=true end
 function d.IsOwnedCarrier(name)return owned[name]==true end
 function d.IsMeaningProbeHeld(pid,c,percent)
  local h=d.meaningOverride
  return h and h.owner==pid and h.city==c:GetID() and h.reference==SPCNetworkInput.Reference(c) and h.percent==percent or false
 end
 function d.ForgetMeaningProbe(pid,cid,reference)
  local h=d.meaningOverride;if h and h.owner==pid and h.city==cid and h.reference==reference then d.meaningOverride=nil;d.meaningQualification=nil end
 end
 -- One current accepted-pair receipt per supported player, never a history.
 -- Only the actual request handler calls this after both receivers return true.
 function d.ConfirmSamplePair(pid,packet)
  local s=d.samples[pid];local f=shared.GreatWorkFacts
  if not P.IsTestPlayer(pid) or not s or not f or s.seq~=packet.Seq or s.generation~=packet.Generation
   or s.turn~=packet.Turn or s.factsEpoch~=packet.FactsEpoch or s.factsInput~=packet.FactsInput
   or s.turn~=Game.GetCurrentGameTurn() or s.generation~=d.generation or s.seq~=d.seq[pid]
   or s.seq~=f.ack or s.factsEpoch~=f.epoch or s.factsInput~=f.inputRevision then return false end
  d.paired[pid]={seq=s.seq,generation=s.generation,turn=s.turn,factsEpoch=s.factsEpoch,factsInput=s.factsInput}
  return true
 end
 -- Meaning's native comparison requires both independent interpretations of
 -- one accepted collection. ACK alone acknowledges processing, not validity.
 function d.IsMeaningSampleCurrent(pid,c,packet)
  local ok,why=pcall(function()
   local s=d.samples[pid];local f=shared.GreatWorkFacts;local pair=d.paired[pid]
   assert(s and f and pair and pair.seq==s.seq and pair.generation==s.generation and pair.turn==s.turn
    and pair.factsEpoch==s.factsEpoch and pair.factsInput==s.factsInput and s.turn==Game.GetCurrentGameTurn() and s.generation==d.generation
    and type(s.seq)=='number' and s.seq==d.seq[pid] and s.seq==f.ack
    and s.factsEpoch==f.epoch and s.factsInput==f.inputRevision,'ME_DIALOGUE_SAMPLE_PAIR_PENDING')
   assert(c:GetOwner()==pid and P.IsTestPlayer(pid) and s.cities[c:GetID()],'ME_DIALOGUE_OWNER')
   local w=f.Summary(pid,c:GetID())
   assert(w and w.availability=='KNOWN' and w.hasConfirmed and w.reference==SPCNetworkInput.Reference(c),'ME_DIALOGUE_SAMPLE_PAIR_PENDING')
   if packet then assert(packet.Seq==s.seq and packet.Generation==s.generation and packet.Turn==s.turn
    and packet.FactsEpoch==s.factsEpoch and packet.FactsInput==s.factsInput,'ME_DIALOGUE_SAMPLE_PAIR_PENDING')end
  end)
  return ok,not ok and (tostring(why):match('ME_[A-Z_]+') or 'ME_DIALOGUE_SAMPLE_PAIR_PENDING') or nil
 end
 -- Current qualification is a single bounded diagnostic projection, not authority.
 local function meaningQualification(pid,c,minimumActive)
  local ok,f=pcall(shared.EffectiveFacts.Read,pid,c)
  d.meaningQualification={owner=pid,city=c:GetID(),reference=SPCNetworkInput.Reference(c),
   specialization=ok and f.specialization or nil,potential=ok and f.potential or nil,
   active=ok and f.active or nil,activeStatus=ok and f.activeStatus or 'UNKNOWN_FACTS'}
  assert(ok,'ME_DIALOGUE_FACT_UNKNOWN')
  assert(f.activeStatus=='KNOWN','ME_DIALOGUE_ACTIVE_UNKNOWN')
  assert(f.specialization=='CULTURE' and (f.active==4 or minimumActive==3 and f.active==3),'ME_DIALOGUE_ACTIVE_REQUIRED')
 end
 function d.HoldMeaningProbe(pid,c,percent,minimumActive)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'ME_DIALOGUE_OWNER')
  assert(percent==0 or percent==100 or percent==200,'ME_DIALOGUE_PERCENT')
  assert(not d.off[pid] and not (d.test[pid] and d.test[pid].city==c:GetID()),'ME_DIALOGUE_OTHER_TEST')
  local ref=SPCNetworkInput.Reference(c);local h=d.meaningOverride
  assert(not h or h.owner==pid and h.city==c:GetID() and h.reference==ref,'ME_DIALOGUE_OTHER_FIXTURE')
  -- Reject before changing the holder: a reentrant request owns no Audit lock.
  assert(not d.busy and not d.initializing,'ME_DIALOGUE_UPDATE_PENDING: BUSY')
  assert(minimumActive==nil or minimumActive==3 or minimumActive==4,'ME_DIALOGUE_GATE')
  d.Init();meaningQualification(pid,c,minimumActive)
  local paired,reason=d.IsMeaningSampleCurrent(pid,c);assert(paired,reason)
  local candidate=h and h.percent==percent and h.minimumActive==(minimumActive or 4) and h or {owner=pid,city=c:GetID(),reference=ref,percent=percent,minimumActive=minimumActive or 4}
  d.meaningOverride=candidate
  local ok,why=pcall(function()
   local updated,updateReason=d.Audit(pid,c:GetID());assert(updated,'ME_DIALOGUE_UPDATE_PENDING: '..tostring(updateReason))
   local p=d.last[pid] and d.last[pid][c:GetID()]
   assert(p and not p.error and p.meaning and p.applied==percent,'ME_DIALOGUE_UNCONFIRMED: '..tostring(p and p.error or 'missing current projection'):sub(1,180))
   local actual,reason=d.ReadMeaningProbe(pid,c);assert(actual==percent,reason or 'ME_DIALOGUE_CARRIER_UNKNOWN')
  end)
  if not ok then
   -- Restore intent only. A partial native write remains visibly unconfirmed;
   -- the exact owned withdrawal path, never a guessed snapshot, handles exit.
   d.meaningOverride=h;error(why)
  end
  return true
 end
 -- Failed cross-module prototype transitions restore only their prior intent.
 -- No native snapshot is replayed: Read still exposes a partial projection.
 function d.RestoreMeaningProbeIntent(pid,c,percent)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'ME_DIALOGUE_OWNER')
  assert(percent==0 or percent==100 or percent==200,'ME_DIALOGUE_PERCENT')
  assert(not d.busy and not d.initializing,'ME_DIALOGUE_UPDATE_PENDING: BUSY')
  local h=d.meaningOverride
  assert(h and h.owner==pid and h.city==c:GetID() and h.reference==SPCNetworkInput.Reference(c),'ME_DIALOGUE_REFERENCE_CHANGED')
  if h.percent~=percent then d.meaningOverride={owner=h.owner,city=h.city,reference=h.reference,percent=percent,minimumActive=h.minimumActive}end
 end
 function d.WithdrawMeaningProbe(pid,c)
  local h=d.meaningOverride
  assert(h and h.owner==pid and h.city==c:GetID() and h.reference==SPCNetworkInput.Reference(c),'ME_DIALOGUE_REFERENCE_CHANGED')
  for name in pairs(owned)do if P.Info('Buildings',name)then set(c,name,false)end end
 end
 function d.ReleaseMeaningProbe(pid,c)
  local h=d.meaningOverride
  assert(h and h.owner==pid and h.city==c:GetID() and h.reference==SPCNetworkInput.Reference(c),'ME_DIALOGUE_REFERENCE_CHANGED')
  d.WithdrawMeaningProbe(pid,c) -- Failed test withdrawal keeps binding/hold.
  d.meaningOverride=nil;d.meaningQualification=nil;return d.Audit(pid,c:GetID()) -- current AUTO; no saved effect replay
 end
 function d.Audit(pid,cid)
  if P.Observe then P.Observe('audit','Dialogue') end
  if not d.ready then return false,'NOT_READY' end
  if d.busy then return false,'BUSY' end
  if not P.IsTestPlayer(pid) then return false,'UNSUPPORTED_OWNER' end
  d.busy=true
  local ok,why=pcall(function()
   local s=d.samples[pid];if cid==nil then d.last[pid]={}else d.last[pid]=d.last[pid] or {};d.last[pid][cid]=nil end
   local output=d.last[pid];local cities=assert(Players[pid]:GetCities(),'CITY_UNAVAILABLE')
   local function visit(c)
    P.Count('city_scan');local id=c:GetID()
    local h=d.meaningOverride
    if h and h.owner==pid and h.city==id and h.reference==SPCNetworkInput.Reference(c) then
     local paired,reason=d.IsMeaningSampleCurrent(pid,c)
     if not paired then
      -- Preserve the held experiment while the request's second interpretation
      -- is pending. It is unconfirmed, never a successful zero or stale read.
      output[id]={applied=nil,error=reason};return
     end
    end
    local valid,p=pcall(function()
     local meaning=shared.CultureMeaningProbe
     -- An exact held zero still needs current qualification/sample checks, but
     -- it cannot mix a positive legacy yield with Meaning. Gate positive paths.
     if meaning and not d.IsMeaningProbeHeld(pid,c,0) then local safe,why=meaning.CanProjectLegacy(pid,c,'Dialogue');assert(safe,why)end
     local f=shared.EffectiveFacts.Read(pid,c)
     local works=s and s.turn==Game.GetCurrentGameTurn() and s.cities[id]
     assert(works,'DIALOGUE_COLLECTION_PENDING')
     local plan=SPCDialogueModel.Plan(P,works);plan.active=f.active;plan.specialization=f.specialization
     plan.sampleSeq=s.seq -- Scalar receipt retained for ordinary projection diagnostics too.
     plan.applied=(not d.off[pid] and f.specialization=='CULTURE' and f.active==4) and plan.percent or 0
     local t=d.test[pid];plan.test=t and t.city==id and t.percent or nil
     if plan.test and not d.off[pid] and f.specialization=='CULTURE' and f.active==4 then plan.applied=plan.test end
     local h=d.meaningOverride
     if h and h.owner==pid and h.city==id and h.reference==SPCNetworkInput.Reference(c) then
      plan.sampleSeq=s.seq;plan.sampleGeneration=s.generation;plan.sampleTurn=s.turn
      plan.sampleEpoch=s.factsEpoch;plan.sampleInput=s.factsInput;plan.reference=h.reference
      local paired,reason=d.IsMeaningSampleCurrent(pid,c);assert(paired,reason)
      plan.meaning=true;plan.test=h.percent
      plan.applied=(not d.off[pid] and f.specialization=='CULTURE' and (f.active==4 or h.minimumActive==3 and f.active==3)) and h.percent or 0
     end
     plan.carrier=plan.applied>0 and ('BUILDING_SPC_B059_'..(plan.test and 'TEST'..plan.test or 'D'..plan.d)) or nil
     return plan
    end)
    if not valid then p={applied=0,error=tostring(p)} end
    local written,writeError=pcall(function()
     local h=d.meaningOverride
     if h and h.owner==pid and h.city==id then assert(c:GetOwner()==pid and SPCNetworkInput.Reference(c)==h.reference,'ME_DIALOGUE_REFERENCE_CHANGED')end
     -- Remove old level first, then add at most one current level.
     for n=2,#levels do if p.carrier~='BUILDING_SPC_B059_D'..n then
      local key='BUILDING_SPC_B059_D'..n;if P.Info('Buildings',key) then set(c,key,false) end
     end end
     for _,v in ipairs({25,50,100,200}) do local key='BUILDING_SPC_B059_TEST'..v;if key~=p.carrier and P.Info('Buildings',key) then set(c,key,false) end end
     if h and h.owner==pid and h.city==id then assert(c:GetOwner()==pid and SPCNetworkInput.Reference(c)==h.reference,'ME_DIALOGUE_REFERENCE_CHANGED')end
     if p.applied>0 then assert(p.d<=#levels,'DIALOGUE_ERA_DIRECTORY');set(c,p.carrier,true)
      if h and h.owner==pid and h.city==id then assert(c:GetOwner()==pid and SPCNetworkInput.Reference(c)==h.reference,'ME_DIALOGUE_REFERENCE_CHANGED')end
     end
    end)
    if not written then p.error=tostring(writeError);p.applied=nil end
    output[id]=p
   end
   if cid~=nil then visit(assert(cities:FindID(cid),'CITY_UNAVAILABLE'))
   else
    -- Keep the iterator/state/control triple returned by the native collection.
    for _,c in cities:Members() do visit(c)end
   end
  end)
  d.busy=false -- Reentrant callers never reach this release.
  if not ok then
   d.errors[pid]='DIALOGUE_AUDIT_FAILED: '..tostring(why):sub(1,180)
   return false,tostring(why):find('CITY_UNAVAILABLE',1,true) and 'CITY_UNAVAILABLE' or 'AUDIT_FAILED'
  end
  return true
 end
 function d.ReadMeaningProbe(pid,c)
  local ok,value=pcall(function()
   local h=d.meaningOverride;assert(h and d.IsMeaningProbeHeld(pid,c,h.percent),'ME_DIALOGUE_REFERENCE_CHANGED')
   meaningQualification(pid,c,h.minimumActive) -- Zero alone cannot prove the held gate.
   local paired,reason=d.IsMeaningSampleCurrent(pid,c);assert(paired,reason)
   local p=d.last[pid] and d.last[pid][c:GetID()];assert(p and not p.error and p.meaning,'ME_DIALOGUE_SAMPLE_PENDING')
   local s=d.samples[pid];assert(p.sampleSeq==s.seq and p.sampleGeneration==s.generation and p.sampleTurn==s.turn
    and p.sampleEpoch==s.factsEpoch and p.sampleInput==s.factsInput and p.reference==SPCNetworkInput.Reference(c),'ME_DIALOGUE_SAMPLE_PENDING')
   assert(p.applied==h.percent,'ME_DIALOGUE_QUALIFICATION_CHANGED')
   local expected=h.percent>0 and ('BUILDING_SPC_B059_TEST'..h.percent) or nil;local b=c:GetBuildings()
   for name in pairs(owned)do local row=P.Info('Buildings',name);if row then
    local has=P.HasBuilding(b,row.Index);assert(type(has)=='boolean','ME_DIALOGUE_CARRIER_UNKNOWN')
    assert(has==(name==expected),'ME_DIALOGUE_PROJECTION_CHANGED')
    if has then assert(b:IsPillaged(row.Index)==false,'ME_DIALOGUE_CARRIER_DAMAGED')end
   end end
   return h.percent
  end)
  return ok and value or nil,not ok and tostring(value):sub(1,240) or nil
 end
 -- B165: explicitly requested coexistence gate. Read current AUTO, never a
 -- saved percent, test override, global OFF or merely a matching UI number.
 function d.ReadNormalForMeaning(pid,c)
  local ok,value=pcall(function()
   assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'ME_DIALOGUE_OWNER')
   assert(not d.meaningOverride and not d.off[pid] and not (d.test[pid] and d.test[pid].city==c:GetID()),'ME_DIALOGUE_OTHER_TEST')
   meaningQualification(pid,c)
   local paired,reason=d.IsMeaningSampleCurrent(pid,c);assert(paired,reason)
   local p=d.last[pid] and d.last[pid][c:GetID()]
   local s=d.samples[pid]
   assert(p and not p.error and not p.meaning and p.sampleSeq==s.seq and p.applied==p.percent,'ME_DIALOGUE_AUTO_PENDING')
   local b=c:GetBuildings()
   for name in pairs(owned)do local row=P.Info('Buildings',name);if row then
    local has=P.HasBuilding(b,row.Index);assert(type(has)=='boolean','ME_DIALOGUE_CARRIER_UNKNOWN')
    assert(has==(name==p.carrier),'ME_DIALOGUE_PROJECTION_CHANGED')
    if has then assert(b:IsPillaged(row.Index)==false,'ME_DIALOGUE_CARRIER_DAMAGED')end
   end end
   return p.applied
  end)
  return ok and value or nil,not ok and tostring(value):sub(1,240) or nil
 end
 -- B176: reuse the held writer for a high-value native comparison. This
 -- controller owns one session fixture and one request receipt, never history.
 function d.CarrierTestNext(pid,c,token,reference)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'DIALOGUE_TEST_OWNER')
  assert(type(token)=='string' and #token>0 and #token<=100,'DIALOGUE_TEST_TOKEN')
  assert(reference==SPCNetworkInput.Reference(c),'DIALOGUE_TEST_REFERENCE_CHANGED')
  local old=d.carrierTestRequest
  if old and old.token==token then
   assert(old.owner==pid and old.reference==reference,'DIALOGUE_TEST_TOKEN_CONFLICT');return
  end
  local t=d.carrierTest
  assert(not t or t.owner==pid and t.city==c:GetID() and t.reference==reference,'DIALOGUE_TEST_OTHER_CITY')
  assert(not shared.CultureMeaningProbe,'DIALOGUE_TEST_OTHER_PROBE')
  if not t then
   assert(not d.meaningOverride,'DIALOGUE_TEST_OTHER_PROBE')
   -- Validate before acquiring a fixture or disturbing the ordinary writer.
   meaningQualification(pid,c,3)
   local paired,why=d.IsMeaningSampleCurrent(pid,c);assert(paired,why)
   t={owner=pid,city=c:GetID(),reference=reference,percent=nil};d.carrierTest=t
  end
  d.carrierTestRequest={owner=pid,reference=reference,token=token}
  local nextPercent=not t.error and (t.percent==nil and 0 or t.percent==0 and 100 or t.percent==100 and 200) or nil
  local ok,why=pcall(function()
   if nextPercent==nil then
    local restored,reason
    if d.meaningOverride then restored,reason=d.ReleaseMeaningProbe(pid,c)
    else
     for name in pairs(owned)do if P.Info('Buildings',name)then set(c,name,false)end end
     restored,reason=d.Audit(pid,c:GetID())
    end
    assert(restored,'DIALOGUE_TEST_RESTORE_PENDING: '..tostring(reason))
    local current=d.last[pid] and d.last[pid][c:GetID()]
    assert(current and not current.error,'DIALOGUE_TEST_RESTORE_UNCONFIRMED')
    d.carrierTest=nil
   else
    d.HoldMeaningProbe(pid,c,nextPercent,3);t.percent=nextPercent;t.error=nil
   end
  end)
  if not ok then t.error=tostring(why):sub(1,180);error(why)end
 end
 function d.DescribeCarrierTest(pid,c)
  local t=d.carrierTest
  local lines={'倍率对照｜临时单城测试；不改变累计记录／已用时代。'}
  if not t then
   lines[#lines+1]='右键：0%基线 → ＋100% → ＋200% → 结束；左键只读。'
   local p=d.last[pid] and d.last[pid][c:GetID()]
   lines[#lines+1]=p and not p.error and ('正常旧倍率：＋'..tostring(p.applied)..'%（不是累计记录）') or '正常旧倍率：待当前馆藏确认。'
  elseif t.owner~=pid or t.city~=c:GetID() or t.reference~=SPCNetworkInput.Reference(c) then
   lines[#lines+1]='测试绑定在另一城市／引用；请回原测试城市，不可在这里推进。'
  else
   local value,reason=d.ReadMeaningProbe(pid,c)
   lines[#lines+1]='本次档位：'..(t.percent~=nil and ('＋'..t.percent..'%') or '未完成')
   lines[#lines+1]=value~=nil and ('载体配置已确认：＋'..value..'%；实际收益请看巨作界面。') or '载体配置未确认；不要据此验收收益。'
   if t.error or reason then lines[#lines+1]='待处理：'..tostring(t.error or reason)..'；右键结束。'
   else lines[#lines+1]=t.percent==0 and '右键：替换为＋100%。' or t.percent==100 and '右键：替换为＋200%。' or '右键：结束并按当前事实恢复旧倍率。' end
  end
  lines[#lines+1]='仅测试巨作文化／旅游倍率；意义延展与HD建筑保持，需比较是否被误放大。'
  return table.concat(lines,'\n')
 end
 function d.Receive(pid,a)
  if not P.IsTestPlayer(pid) then return false end
  d.received[pid]={seq=a.Seq,generation=a.Generation,stage='RECEIVED'}
  if a.Generation~=d.generation then d.errors[pid]='DIALOGUE_GENERATION_MISMATCH';d.received[pid].stage='REJECTED_GENERATION';return false end
  if type(a.Seq)~='number' or a.Seq%1~=0 or a.Seq<=(d.seq[pid] or 0) then return false end
  -- ACK receipt even if initialization fails: failure must not create a resend storm.
  d.seq[pid]=a.Seq
  local initialized,initError=pcall(d.Init)
  if not initialized then
   d.samples[pid]=nil;d.errors[pid]='DIALOGUE_INIT_FAILED: '..tostring(initError);d.received[pid].stage='INIT_FAILED';return false
  end
  d.received[pid].stage='INITIALIZED'
  local ok,res=pcall(function()
   assert(a.Valid==1 and a.Turn==Game.GetCurrentGameTurn() and type(a.Data)=='string' and #a.Data<=100000,'DIALOGUE_SAMPLE_INVALID')
   local cities,seen={},{};local count=0
   for line in a.Data:gmatch('[^;]+') do
    local cid,wid,typ=line:match('^(%d+),(%-?%d+),([A-Z0-9_]+)$');cid=tonumber(cid);wid=tonumber(wid)
    local c=cid and Players[pid]:GetCities():FindID(cid);assert(c and c:GetOwner()==pid,'DIALOGUE_OWNER')
    if wid==-1 then assert(not cities[cid] and typ=='EMPTY','DIALOGUE_CITY_DUPLICATE');cities[cid]={}
    else assert(cities[cid] and wid and wid>=0 and not seen[wid],'DIALOGUE_DUPLICATE_WORK');seen[wid]=true
     assert(P.Info('GreatWorks',typ),'DIALOGUE_WORK_TYPE');cities[cid][#cities[cid]+1]={id=wid,type=typ}
    end
    count=count+1
   end
   assert(count==a.Count,'DIALOGUE_COUNT')
   for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan'); assert(cities[c:GetID()],'DIALOGUE_CITY_MISSING') end
   return {turn=a.Turn,cities=cities,seq=a.Seq,generation=a.Generation,factsEpoch=a.FactsEpoch,factsInput=a.FactsInput}
  end)
  d.samples[pid]=ok and res or nil;d.errors[pid]=not ok and tostring(res) or nil;d.received[pid].stage=ok and 'ACCEPTED' or 'REJECTED_SAMPLE';d.Audit(pid)
  if shared.GreatWorkAdjacency then shared.GreatWorkAdjacency.Receive(pid,a) end
  return ok -- Accepted collection, independent of legacy projection success.
 end
 function d.Describe(pid,c)
  local p=d.last[pid] and d.last[pid][c:GetID()]
  if not p then
   local r=d.received[pid]
   local incoming=shared.RequestIngress or {};local packet=shared.DialogueIngress
   return '时代对话：后台收藏尚未初始化\nGame ready='..tostring(d.ready)..' ACK='..tostring(d.seq[pid] or 0)
    ..' | received='..tostring(r and r.seq or 'NONE')..' | '..tostring(r and r.stage or 'NO_PACKET')
    ..'\n入口 count='..tostring(incoming.count or 0)..' last='..tostring(incoming.action)..' player='..tostring(incoming.player)
    ..' | 收藏入口='..tostring(packet and packet.seq or 'NONE')..' bytes='..tostring(packet and packet.dataBytes or 0)
    ..'\nGeneration expected='..d.generation..' received='..tostring(r and r.generation or 'NONE')
    ..'\n'..tostring(d.errors[pid] or '等待后台当前收藏；不要用配置缺失状态验算收益。')
  end
  local rows={'B059 时代对话 | city='..c:GetID()..(d.off[pid] and ' | TEST OFF' or ' | AUTO')}
  if p.error then rows[#rows+1]='未完成：'..p.error;return table.concat(rows,'\n') end
  rows[#rows+1]=string.format('%s ACTIVE=%s | 合格%d件 / 排除%d件 / 创作者时代D=%d',p.specialization,tostring(p.active),p.count,p.excluded,p.d)
  rows[#rows+1]=string.format('理论+%d%% Culture/Tourism | 已配置%s%%',p.percent,tostring(p.applied))
  if p.test then rows[#rows+1]='临时本城实验：+'..p.test..'%（替换AUTO，不叠加；读档恢复AUTO）' end
  local eras={};for era in pairs(p.eras) do eras[#eras+1]=era end;table.sort(eras)
  rows[#rows+1]=table.concat(eras,', ')
  for i=1,math.min(3,#p.rows) do local w=p.rows[i];rows[#rows+1]=Locale.Lookup(w.name)..' → '..w.era..(w.artifact and '（文物历史时代）' or '') end
  rows[#rows+1]='配置≠实测；请比较下方作品实际产出，theming按原生行为。'
  return table.concat(rows,'\n')
 end
 local function auditAll() for pid in pairs(Players) do
  d.Audit(pid);if shared.GreatWorkAdjacency then shared.GreatWorkAdjacency.Audit(pid) end
 end end
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged'}) do
  local e=P.Field(Events,name);if e and e.Add then e.Add(function(pid)
   if type(pid)=='number' and pid>=0 then
    if not P.IsTestPlayer(pid) then return end
    d.Audit(pid);if shared.GreatWorkAdjacency then shared.GreatWorkAdjacency.Audit(pid) end
   else auditAll() end -- unknown signature retains prior conservative scope
  end) end
 end
 local e=P.Field(Events,'CityTransfered');if e and e.Add then e.Add(function() if d.carrierTest then d.carrierTest=nil;d.meaningOverride=nil;d.meaningQualification=nil end;d.ready=false;d.samples={};d.paired={};d.last={};d.Init();auditAll() end) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('Dialogue',function(c,loss)
   local ids={};for n=2,#levels do local id='BUILDING_SPC_B059_D'..n;if P.Info('Buildings',id)then ids[#ids+1]=id end end;for _,n in ipairs({25,50,100,200})do ids[#ids+1]='BUILDING_SPC_B059_TEST'..n end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
   local t=d.carrierTest
   if t and t.owner==loss.origin.owner then
    -- Exit has already proved its exact target. Drop only the matching hold.
    local h=d.meaningOverride
    if h and h.reference==t.reference and h.city==loss.origin.cityID then
     d.carrierTest=nil;d.meaningOverride=nil;d.meaningQualification=nil
    end
   end
 end)end

 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('Dialogue',function(pid)d.generation=d.generation+1;d.samples={};d.paired={};d.seq={};d.last={};d.test={} end)end

end
