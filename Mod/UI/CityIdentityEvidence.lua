-- On-demand UI evidence only. Never sends requests, saves properties or authorizes identity.
SPCCityIdentityEvidence={}
function SPCCityIdentityEvidence.New(P)
 local watch,events=nil,{};local full=false
 local function scalar(v)
  local t=type(v)
  if t=='number' or t=='boolean' or t=='nil' then return tostring(v)end
  if t=='string' then return v:sub(1,48):gsub('[\r\n]',' ')end
  return '<'..t..'>'
 end
 local function field(c,name)
  local ok,f=pcall(function()return c[name]end)
  if not ok then return name..': LOOKUP_ERROR' end
  if type(f)~='function' then return name..': ABSENT ('..type(f)..')' end
  local good,v=pcall(f,c)
  if not good then return name..': CALL_ERROR' end
  return name..': '..scalar(v)..' ['..type(v)..']'
 end
 local function observe(name,pid,cid,...)
  if not watch then return end
  local c=CityManager.GetCityAt(watch.x,watch.y)
  if not ((pid==watch.owner and cid==watch.cityID) or (c and pid==c:GetOwner() and cid==c:GetID())) then return end
  local a={scalar(pid),scalar(cid)}
  for i=1,math.min(select('#',...),6)do a[#a+1]=scalar(select(i,...))end
  local line=name..' T'..Game.GetCurrentGameTurn()..' ('..table.concat(a,',')..')'
  for _,old in ipairs(events)do if old==line then return end end
  if #events>=8 then full=true;return end;events[#events+1]=line
 end
 for _,name in ipairs({'CityTransfered','CulturalIdentityCityConverted','CityLiberated'})do
  local n=name;local e=P.Field(Events,n)
  if e and type(e.Add)=='function' then e.Add(function(...)local ok=pcall(observe,n,...);if not ok then full=true end end)end
 end
 return {Read=function(pid)
  local ok,out=pcall(function()
   if not P.IsTestPlayer(pid) then return 'UI证据：不在测试范围。' end
   local v=Game:GetProperty('SPC_E1_IDENTITY_EXPERIMENT_V1')
   if type(v)~='table' or v.schema~=1 or v.requester~=pid or type(v.origin)~='table' or type(v.token)~='string' then return '请先右键“记录城市身份”建立实验，再读取UI证据。'end
   local o=v.origin
   for _,k in ipairs({'owner','cityID','x','y'})do assert(type(o[k])=='number' and o[k]>=0 and o[k]%1==0,'BAD_REFERENCE')end
   if not watch or watch.token~=v.token or watch.x~=o.x or watch.y~=o.y then
    watch={owner=o.owner,cityID=o.cityID,x=o.x,y=o.y,token=v.token};events={};full=false
   end
   local c=CityManager.GetCityAt(o.x,o.y)
   local lines={P.VERSION..' | UI侧易主证据（只读）','实验：'..v.token,
    '原引用：'..o.owner..'/'..o.cityID,'当前引用：'..(c and c:GetOwner()..'/'..c:GetID() or '无城市'),
    '只作佐证，不迁移、不改变HELD。'}
   if c then for _,n in ipairs({'GetOriginalOwner','GetOwnerBeforeOccupation','GetJustConqueredFrom','GetLastTransferType'})do lines[#lines+1]=field(c,n)end end
   lines[#lines+1]='本次UI观察事件：'..#events..(full and '（已满或观察失败）' or '')
   for _,e in ipairs(events)do lines[#lines+1]=e end
   if #events==0 then lines[#lines+1]='本次加载首次读取后才观察；未捕获不代表事件不存在。'end
   return table.concat(lines,'\n')
  end)
  return ok and out or 'UI证据读取失败；未写入或迁移。'
 end}
end
