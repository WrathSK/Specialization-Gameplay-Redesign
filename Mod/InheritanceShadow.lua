-- B064 shadow only: no city writes, no ownership adoption, no rewards.
SPCInheritanceShadow={KEY='SPC_INHERITANCE_SHADOW_V1'}
function SPCInheritanceShadow.Start(P,shared)
 local KEY=SPCInheritanceShadow.KEY
 local d={errors={},hooks={},writes=0,ready=false};shared.InheritanceShadow=d
 local fields={TOKEN='SPC_DEV_BINDING_B013_TOKEN',FLOW='SPC_DEV_CITY_FLOW_B020',JOURNAL='SPC_DEV_CITY_JOURNAL_B015',INVEST='SPC_DEV_INVESTMENT_LEDGER_V1',TEMPLATES='SPC_STANDARDIZATION_LEDGER_V1'}
 local function cp(v,n) n=n or 0;assert(n<20,'SHADOW_DEPTH');if type(v)~='table' then return v end;local r={};for k,x in pairs(v) do r[k]=cp(x,n+1) end;return r end
 local function eq(a,b,n) n=n or 0;if n>20 or type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end;for k,v in pairs(a) do if not eq(v,b[k],n+1) then return false end end;for k in pairs(b) do if a[k]==nil then return false end end;return true end
 local function count(t) local n=0;if type(t)=='table' then for _ in pairs(t) do n=n+1 end end;return n end
 local function read()
  local v=Game:GetProperty(KEY)
  if v==nil then return {schema=1,revision=0,records={},watch={},events={},sequence=0} end
  assert(type(v)=='table' and v.schema==1 and type(v.records)=='table' and type(v.watch)=='table' and type(v.events)=='table' and type(v.revision)=='number' and type(v.sequence)=='number','SHADOW_BAD_LEDGER')
  return cp(v)
 end
 local function save(old,v)
  if eq(old,v) then return end
  assert(eq(read(),old),'SHADOW_STALE');v.revision=old.revision+1
  Game:SetProperty(KEY,cp(v));assert(eq(read(),v),'SHADOW_WRITE_UNCONFIRMED');d.writes=d.writes+1
 end
 local function safe(fn,...)
  local ok,e=pcall(fn,...);if not ok then d.errors.last=tostring(e):match('SHADOW_[A-Z_]+') or 'SHADOW_CALLBACK_ERROR（详见Lua.log）';print('[SPC][B064] '..tostring(e)) end;return ok
 end
 function d.Capture(c,reason)
  if not c or not P.IsTestPlayer(c:GetOwner()) then return end
  local pid=c:GetOwner();local token,state=shared.BindingProbe.Resolve(pid,c)
  if not token or state~='BOUND_MATCH' then return end
  local old=read();local v=cp(old);local r=v.records[token]
  if r then assert((r.owner==pid and r.cityID==c:GetID() and r.x==c:GetX() and r.y==c:GetY()) or (shared.CityInheritance and shared.CityInheritance.AllowsShadow(token,c)),'SHADOW_ANCHOR_CONFLICT') end
  local values={};for k,key in pairs(fields) do values[k]=cp(c:GetProperty(key)) end
  if r and eq(r.values,values) then return end
  v.records[token]={uid=token,owner=pid,cityID=c:GetID(),x=c:GetX(),y=c:GetY(),values=values,revision=(r and r.revision or 0)+1,turn=Game.GetCurrentGameTurn(),reason=reason}
  save(old,v)
 end
 -- Called only after existing writes. A shadow failure is diagnostic, never a second unit charge.
 shared.OnPermanentCityWrite=function(c,reason) safe(function() d.Capture(c,reason) end) end
 function d.Select(pid,c)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'SHADOW_SELECT_OWN_CITY')
  d.Capture(c,'SELECT');local token,state=shared.BindingProbe.Resolve(pid,c);assert(token and state=='BOUND_MATCH','SHADOW_NO_VALID_BINDING')
  local old=read();assert(old.records[token],'SHADOW_RECORD_MISSING');local v=cp(old);v.watch[tostring(pid)]=token;save(old,v)
  return d.Describe(pid)
 end
 function d.Describe(pid)
  assert(P.IsTestPlayer(pid),'SHADOW_PLAYER_REQUIRED');local v=read();local uid=v.watch[tostring(pid)];assert(uid and v.records[uid],'请选择己方有有效记录的城市，点击Select shadow city')
  local r=v.records[uid];local a=r.values;local j=a.JOURNAL or {};local inv=a.INVEST or {};local std=a.TEMPLATES or {}
  local c=CityManager.GetCityAt(r.x,r.y)
  local lines={'永久备份对照（继承状态见上方）','Game账本rev='..v.revision..' | 城市备份rev='..r.revision..' | UID='..uid,
   '备份Owner/CityID='..r.owner..'/'..r.cityID..' | 原位置当前='..(c and c:GetOwner()..'/'..c:GetID() or '无城市'),
   '备份专业='..tostring(j.specialization)..' | 投资='..count(inv.investments)..' | 模板='..count(std.learned)..' | pending='..tostring(inv.pending and inv.pending.stage),
   '保存原因='..tostring(r.reason)..' | 本次加载写入='..d.writes}
  for _,k in ipairs({'TOKEN','FLOW','JOURNAL','INVEST','TEMPLATES'}) do local now=c and c:GetProperty(fields[k]);lines[#lines+1]=k..' 备份='..(a[k]~=nil and '有' or '无')..' 当前='..(now~=nil and '有' or '无')..' 一致='..tostring(eq(a[k],now)) end
  lines[#lines+1]='事件记录总序号='..v.sequence..'（保留最近24条，显示最后6条）'
  for i=math.max(1,#v.events-5),#v.events do local e=v.events[i];lines[#lines+1]=e.seq..' '..e.name..' '..e.args..' | 位置状态 '..e.at end
  lines[#lines+1]='Hook '..table.concat(d.hooks,',')
  lines[#lines+1]='错误='..tostring(d.errors.last or '无')..'；当前位置仅观察，不认定身份继承。'
  return table.concat(lines,'\n')
 end
 local function event(name,...)
  local args={...};local n=select('#',...);local old=read();if not next(old.records) then return end
  local relevant=false;local states={}
  for _,r in pairs(old.records) do
   local c=CityManager.GetCityAt(r.x,r.y)
   local endpoint=(args[1]==r.owner and args[2]==r.cityID) or (c and args[1]==c:GetOwner() and args[2]==c:GetID())
   local coords=(args[3]==r.x and args[4]==r.y) or (args[4]==r.x and args[5]==r.y)
   if endpoint or coords then relevant=true;states[#states+1]=r.uid..':'..(c and c:GetOwner()..'/'..c:GetID() or 'NONE') end
  end
  if not relevant then return end
  table.sort(states);  -- Convert each parameter explicitly, including nil holes; never retain engine objects.
  local text={};for i=1,math.min(n,8) do local x=args[i];text[#text+1]=(type(x)=='number' or type(x)=='boolean' or type(x)=='string' or x==nil) and tostring(x) or ('<'..type(x)..'>') end
  local v=cp(old);v.sequence=v.sequence+1;local e={seq=v.sequence,name=name,args=table.concat(text,','),at=table.concat(states,';'),turn=Game.GetCurrentGameTurn()};v.events[#v.events+1]=e
  if #v.events>24 then table.remove(v.events,1) end;save(old,v);print('[SPC][B064][EVENT] '..e.seq..' '..name..' '..e.args..' '..e.at)
 end
 local function hook(ns,name,fn,label)
  local e=ns and ns[name];local ok=e and type(e.Add)=='function' and pcall(e.Add,function(...) safe(fn,...) end)
  d.hooks[#d.hooks+1]=(label or name)..':'..(ok and 'ON' or 'ABSENT')
 end
 for _,name in ipairs({'CityTransfered','CityAddedToMap','CityRemovedFromMap','CityInitialized'}) do hook(Events,name,function(...) event(name,...) end) end
 for _,name in ipairs({'CityBuilt','CityConquered'}) do hook(GameEvents,name,function(...) event(name,...) end,'Game.'..name) end
 hook(Events,'LoadScreenClose',function()
  d.ready=true
  for pid,p in pairs(Players) do if P.IsTestPlayer(pid) then for _,c in p:GetCities():Members() do safe(function() d.Capture(c,'LOAD_VALIDATED') end) end end end
 end)
end
