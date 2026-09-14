include('DialogueModel')
SPCDialogue={}
function SPCDialogue.Start(P,shared)
 local d={ready=false,busy=false,seq={},samples={},off={},test={},last={},errors={},changes=0,received={},generation=1};shared.Dialogue=d
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
  for _,p in pairs(Players) do local cities=p:GetCities();if cities then for _,c in cities:Members() do P.Count('city_scan');
   for n=2,#levels do local id='BUILDING_SPC_B059_D'..n;if P.Info('Buildings',id) then set(c,id,false) end end
   for _,v in ipairs({25,50,100}) do local id='BUILDING_SPC_B059_TEST'..v;if P.Info('Buildings',id) then set(c,id,false) end end
   for _,m in ipairs({'CITY','OBJECT'}) do local id='BUILDING_SPC_B055_GW_'..m;if P.Info('Buildings',id) then set(c,id,false) end end
  end end end
  d.ready=true
 end
 function d.Audit(pid)
  if not d.ready or d.busy or not P.IsTestPlayer(pid) then return end;d.busy=true
  local s=d.samples[pid];local output={};d.last[pid]=output
  for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan');
   local id=c:GetID();local ok,p=pcall(function()
    local f=shared.EffectiveFacts.Read(pid,c)
    local works=s and s.turn==Game.GetCurrentGameTurn() and s.cities[id]
    assert(works,'DIALOGUE_COLLECTION_PENDING')
    local plan=SPCDialogueModel.Plan(P,works);plan.active=f.active;plan.specialization=f.specialization
    plan.applied=(not d.off[pid] and f.specialization=='CULTURE' and f.active==4) and plan.percent or 0
    local t=d.test[pid];plan.test=t and t.city==id and t.percent or nil
    if plan.test and not d.off[pid] and f.specialization=='CULTURE' and f.active==4 then plan.applied=plan.test end
    plan.carrier=plan.applied>0 and ('BUILDING_SPC_B059_'..(plan.test and 'TEST'..plan.test or 'D'..plan.d)) or nil
    return plan
   end)
   if not ok then p={applied=0,error=tostring(p)} end
   local written,why=pcall(function()
    -- Remove old level first, then add at most one current level.
    for n=2,#levels do if p.carrier~='BUILDING_SPC_B059_D'..n then
     local key='BUILDING_SPC_B059_D'..n;if P.Info('Buildings',key) then set(c,key,false) end
    end end
    for _,v in ipairs({25,50,100}) do local key='BUILDING_SPC_B059_TEST'..v;if key~=p.carrier and P.Info('Buildings',key) then set(c,key,false) end end
    if p.applied>0 then assert(p.d<=#levels,'DIALOGUE_ERA_DIRECTORY');set(c,p.carrier,true) end
   end)
   if not written then p.error=tostring(why);p.applied=nil end
   output[id]=p
  end
  d.busy=false
  if shared.GreatWorkAdjacency then shared.GreatWorkAdjacency.Audit(pid) end
 end
 function d.Receive(pid,a)
  if not P.IsTestPlayer(pid) then return end
  d.received[pid]={seq=a.Seq,generation=a.Generation,stage='RECEIVED'}
  if a.Generation~=d.generation then d.errors[pid]='DIALOGUE_GENERATION_MISMATCH';d.received[pid].stage='REJECTED_GENERATION';return end
  if type(a.Seq)~='number' or a.Seq%1~=0 or a.Seq<=(d.seq[pid] or 0) then return end
  -- ACK receipt even if initialization fails: failure must not create a resend storm.
  d.seq[pid]=a.Seq
  local initialized,initError=pcall(d.Init)
  if not initialized then
   d.samples[pid]=nil;d.errors[pid]='DIALOGUE_INIT_FAILED: '..tostring(initError);d.received[pid].stage='INIT_FAILED';return
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
   return {turn=a.Turn,cities=cities}
  end)
  d.samples[pid]=ok and res or nil;d.errors[pid]=not ok and tostring(res) or nil;d.received[pid].stage=ok and 'ACCEPTED' or 'REJECTED_SAMPLE';d.Audit(pid)
  if shared.GreatWorkAdjacency then shared.GreatWorkAdjacency.Receive(pid,a) end
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
 local function auditAll() for pid in pairs(Players) do d.Audit(pid) end end
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','PlayerTurnActivated','PlayerTurnDeactivated'}) do
  local e=P.Field(Events,name);if e and e.Add then e.Add(auditAll) end
 end
 local e=P.Field(Events,'CityTransfered');if e and e.Add then e.Add(function() d.ready=false;d.samples={};d.last={};d.Init();auditAll() end) end
end
