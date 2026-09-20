-- P0-E1: bounded, read-only evidence. Never issues a cityKey or authorizes migration.
SPCCityIdentityRead={}
local M=SPCCityIdentityRead
M.Keys={TOKEN='SPC_DEV_BINDING_B013_TOKEN',JOURNAL='SPC_DEV_CITY_JOURNAL_B015',FLOW='SPC_DEV_CITY_FLOW_B020',INVEST='SPC_DEV_INVESTMENT_LEDGER_V1',TEMPLATES='SPC_STANDARDIZATION_LEDGER_V1'}
local order={'TOKEN','JOURNAL','FLOW','INVEST','TEMPLATES'}
local function int(x) return type(x)=='number' and x>=0 and x<1000000000 and x%1==0 end
-- Shared budget across the whole snapshot; rejects cycles and oversized/corrupt saves.
function M.Copy(value)
 local nodes,bytes,seen=0,0,{}
 local function cp(v,depth)
  nodes=nodes+1;assert(nodes<=8192 and depth<=12,'EVIDENCE_LIMIT')
  local t=type(v)
  if t=='table' then
   assert(not seen[v],'EVIDENCE_CYCLE');seen[v]=true;local out={}
   for k,x in pairs(v) do assert(type(k)=='string' or type(k)=='number','EVIDENCE_KEY');out[cp(k,depth+1)]=cp(x,depth+1) end
   seen[v]=nil;return out
  end
  assert(t=='nil' or t=='string' or t=='number' or t=='boolean','EVIDENCE_TYPE')
  if t=='string' then bytes=bytes+#v;assert(bytes<=65536,'EVIDENCE_LIMIT') end
  if t=='number' then assert(v==v and v~=math.huge and v~=-math.huge,'EVIDENCE_NUMBER') end
  return v
 end
 return cp(value,0)
end
local function same(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~='table' then return a==b end
 for k,v in pairs(a) do if not same(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
local function anchor(v,r,token)
 return type(v)=='table' and v.owner==r.owner and v.cityID==r.cityID and v.token==token and v.x==r.x and v.y==r.y
end
local reasons={NO_TOKEN='缺少旧绑定凭据，不能认领历史',NO_LEDGER='原Owner绑定总账缺失',BAD_LEDGER='绑定总账格式或计数冲突',DUPLICATE_TOKEN='绑定凭据不唯一',POSITION_CHANGED='旧锚点与当前位置冲突',PARTIAL_BINDING='绑定尚未确认',JOURNAL='专业历史缺失或冲突',FLOW='专业提交未完成或与历史不一致',INVEST='投资凭据不完整或冲突',TEMPLATES='模板记录格式或锚点冲突',CROSS_OWNER='原锚点记录仍在，但跨Owner/引用连续性尚未通过原生验证',LOCAL_MATCH='原验证范围内记录一致；仅可作后续迁移候选',READ_FAILED='读取失败或记录过大；未替换上次观察',NO_CITY='原位置无城市，不能推断其历史终止或新城身份'}
function M.Preview(input)
 local ok,s=pcall(M.Copy,input)
 if not ok then return {state='HELD',reason='READ_FAILED',message=reasons.READ_FAILED,migrationAllowed=false} end
 local out={state='HELD',migrationAllowed=false,cityKey=nil,generation='UNKNOWN',history='UNKNOWN',catalog='NOT_VALIDATED',checks={}}
 local function stop(code,state) out.state=state or 'HELD';out.reason=code;out.message=reasons[code];return out end
 if type(s)~='table' or type(s.ref)~='table' then return stop('NO_CITY','UNKNOWN') end
 local v=s.values or {};if type(v)~='table' then return stop('BAD_LEDGER') end;local token=v.TOKEN
 if token==nil then return stop('NO_TOKEN','UNKNOWN') end
 if type(token)~='string' then return stop('BAD_LEDGER') end
 local owner=tonumber(token:match('^DEV%-B013%-P(%d+)%-[1-9]%d*$'))
 if not owner then return stop('BAD_LEDGER') end
 local l=s.ledger;if l==nil then return stop('NO_LEDGER') end
 if type(l)~='table' or l.schema~=1 or l.owner~=owner or not int(l.counter) or l.counter>32 or type(l.records)~='table' then return stop('BAD_LEDGER') end
 local n,matches,record,seen=0,0,nil,{}
 for k,r in pairs(l.records) do
  if type(r)~='table' or not int(r.cityID) or k~=tostring(r.cityID) or r.owner~=owner or not int(r.x) or not int(r.y) or not int(r.serial) or r.serial<1 or r.serial>l.counter or seen[r.serial] or r.uid~='DEV-B013-P'..owner..'-'..r.serial or (r.state~='RESERVED' and r.state~='CONFIRMED') then return stop('BAD_LEDGER') end
  seen[r.serial]=true;n=n+1
  if r.uid==token then matches=matches+1;record=r end
 end
 if n~=l.counter then return stop('BAD_LEDGER') end
 if matches~=1 then return stop('DUPLICATE_TOKEN') end
 out.origin={owner=record.owner,cityID=record.cityID,x=record.x,y=record.y};out.candidateToken=token
 if record.state~='CONFIRMED' then return stop('PARTIAL_BINDING') end
 if record.x~=s.ref.x or record.y~=s.ref.y then return stop('POSITION_CHANGED') end
 out.checks.binding='MATCH'
 local j=v.JOURNAL
 if not anchor(j,record,token) or j.schema~=1 or j.kind~='DEV_FOUNDATION_JOURNAL' or j.health~='TRACKING' or not int(j.foundationTurn) or not int(j.revision) then return stop('JOURNAL') end
 if j.specialization=='NONE' then
  if j.potential~=0 or j.first~=nil then return stop('JOURNAL') end
 elseif not ({RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true})[j.specialization] or j.potential~=1 or type(j.first)~='table' or not int(j.first.districtID) or not int(j.first.turn) or j.first.turn<j.foundationTurn or type(j.first.type)~='string' then return stop('JOURNAL') end
 out.checks.journal='STRUCTURE_MATCH'
 local f=v.FLOW
 if not anchor(f,record,token) or f.schema~=1 or not int(f.revision) or f.revision<1 or f.stage~='DONE' or not same(f.facts,f.target) or not same(f.target,j) then return stop('FLOW') end
 out.checks.flow='DONE_MATCH'
 local inv=v.INVEST
 if inv~=nil then
  local a=type(inv)=='table' and inv.anchor
  if type(inv)~='table' or inv.schema~=1 or type(a)~='table' or a.owner~=record.owner or a.cityID~=record.cityID or a.token~=token or a.specialization~=j.specialization or not same(a.first,j.first) or inv.pending~=nil or type(inv.investments)~='table' then return stop('INVEST') end
  local count,uids=0,{}
  for receipt,uid in pairs(inv.investments) do
   if type(receipt)~='string' or receipt=='' or type(uid)~='string' or uid=='' or uids[uid] then return stop('INVEST') end
   uids[uid]=true;count=count+1
  end
  if count>3 or inv.revision~=count+1 then return stop('INVEST') end
  out.checks.investment='STRUCTURE_MATCH'
 else out.checks.investment='ABSENT_NOT_SYNTHESIZED' end
 local t=v.TEMPLATES
 if t~=nil then
  if type(t)~='table' or t.schema~=1 or t.initialized~=true or t.uid~='STD:'..token or t.foundation~=token or t.x~=record.x or t.y~=record.y or type(t.learned)~='table' then return stop('TEMPLATES') end
  local count=0
  for id,row in pairs(t.learned) do
   if type(id)~='string' or type(row)~='table' or type(row.district)~='string' or not int(row.tier) or row.tier<1 or not int(row.turn) or type(row.evidence)~='string' then return stop('TEMPLATES') end
   count=count+1
  end
  if t.revision~=count+1 then return stop('TEMPLATES') end
  out.checks.templates='STRUCTURE_ONLY_CATALOG_REVIEW_REQUIRED'
 else out.checks.templates='ABSENT_NOT_SYNTHESIZED' end
 -- Shape consistency is not current catalog validation, migration authorization, or generation proof.
 if s.ref.owner~=record.owner or s.ref.cityID~=record.cityID then return stop('CROSS_OWNER') end
 return stop('LOCAL_MATCH','LOCAL_CANDIDATE')
end
function M.Compare(before,after)
 if not before then return 'NO_SESSION_BASELINE' end
 if not after then return 'LOCATION_EMPTY' end
 local a,b=before.values.TOKEN,after.values.TOKEN
 if a and b and a~=b then return 'DIFFERENT_TOKEN_DO_NOT_MERGE' end
 if not a or not b then return 'UNKNOWN_TOKEN_MISSING' end
 if before.ref.x~=after.ref.x or before.ref.y~=after.ref.y then return 'CONFLICT_POSITION' end
 if before.ref.owner~=after.ref.owner or before.ref.cityID~=after.ref.cityID then return 'TOKEN_RETAINED_CONTINUITY_UNPROVEN' end
 return 'SAME_REFERENCE_CONTINUITY_UNPROVEN'
end
function M.Start(P,shared)
 if shared.CityIdentityRead then return end
 local d={events={},eventCount=0,eventNext=1,epoch=1,reads=0,hooks={}}
 shared.CityIdentityRead=d
 local watch
 local function capture(c)
  if not c then return nil end
  local s={ref={owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()},values={}}
  for _,name in ipairs(order) do s.values[name]=c:GetProperty(M.Keys[name]) end
  local token=s.values.TOKEN;local owner=type(token)=='string' and tonumber(token:match('^DEV%-B013%-P(%d+)%-[1-9]%d*$'))
  if owner then s.ledger=Game:GetProperty('SPC_DEV_BINDING_B013_P'..owner) end
  d.reads=d.reads+1;return M.Copy(s)
 end
 local function ref(r) return tostring(r.owner)..'/'..tostring(r.cityID)..' @ '..tostring(r.x)..','..tostring(r.y) end
 function d.Describe(pid,detail)
  assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED')
  if not watch or watch.pid~=pid then return '城市身份：尚无本次加载的观察记录。\n请选择己方专业城，点击“记录城市身份”。读档后需重新记录。' end
  local ok,s=pcall(function() return capture(CityManager.GetCityAt(watch.before.ref.x,watch.before.ref.y)) end)
  if not ok then return '城市身份：读取失败或记录超限。保留原观察；未执行迁移。' end
  local result=M.Preview(s)
  local names={LOCAL_CANDIDATE='原范围记录一致（迁移候选）',HELD='暂缓迁移',UNKNOWN='无充分证据'}
  local lines={P.VERSION..' | 城市身份只读核对',names[result.state],result.message,
   '当前引用：'..(s and ref(s.ref) or '原位置无城市'),
   '跨易主／读档永久身份：尚未通过原生验证；未写入任何记录。'}
  if detail then
   lines[#lines+1]='原引用：'..ref(watch.before.ref)..' | 对照：'..M.Compare(watch.before,s)
   lines[#lines+1]='绑定凭据：'..tostring(watch.before.values.TOKEN)..' → '..tostring(s and s.values.TOKEN)
   if result.origin then lines[#lines+1]='旧账本锚点：'..ref(result.origin) end
   for _,name in ipairs(order) do
    local a,b=watch.before.values[name],s and s.values[name]
    lines[#lines+1]=name..'：'..(a==nil and '原无' or '原有')..' → '..(b==nil and '现无' or '现有')..'；'..(same(a,b) and '一致' or '不同')
   end
   lines[#lines+1]='模板目录/历史最大值/新cityKey均未认定。事件仅作证据，不授权继承。'
   local count=math.min(d.eventCount,8)
   for i=count,1,-1 do local idx=(d.eventNext-i-1)%32+1;local e=d.events[idx];lines[#lines+1]=e.name..' T'..e.turn..' ['..table.concat(e.args,',')..']' end
  end
  return table.concat(lines,'\n')
 end
 function d.Record(pid,c)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'SELECT_OWN_CITY')
  local s=capture(c) -- a failed read must not replace the previous baseline
  watch={pid=pid,before=s};d.events={};d.eventCount=0;d.eventNext=1
  return d.Describe(pid,false)
 end
 local function listen(ns,name,fn)
  local e=P.Field(ns,name)
  d.hooks[name]=e and type(e.Add)=='function' and pcall(e.Add,fn) or false
 end
 local function observe(name,...)
  if not watch then return end
  local args={}
  for i=1,math.min(select('#',...),8) do
   local v=select(i,...);local t=type(v)
   args[i]=(t=='number' or t=='boolean' or t=='string') and tostring(v):sub(1,64) or '<non-scalar>'
  end
  d.events[d.eventNext]={name=name,args=args,turn=tostring(Game.GetCurrentGameTurn())}
  d.eventNext=d.eventNext%32+1;d.eventCount=math.min(32,d.eventCount+1)
 end
 for _,name in ipairs({'CityTransfered','CityAddedToMap','CityRemovedFromMap','CityInitialized'}) do local n=name;listen(Events,n,function(...) observe(n,...) end) end
 for _,name in ipairs({'CityBuilt','CityConquered'}) do local n=name;listen(GameEvents,n,function(...) observe(n,...) end) end
 listen(Events,'LoadScreenClose',function() watch=nil;d.events={};d.eventCount=0;d.eventNext=1;d.epoch=d.epoch+1 end)
end
