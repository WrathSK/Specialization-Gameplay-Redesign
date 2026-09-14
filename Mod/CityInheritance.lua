-- B066 existing-identity transfers only; no Claim or missing-history invention.
SPCCityInheritance={KEY='SPC_CITY_INHERITANCE_V1'}
function SPCCityInheritance.Start(P,shared)
 local KEY=SPCCityInheritance.KEY
 local TOKEN='SPC_DEV_BINDING_B013_TOKEN'
 local fields={TOKEN=TOKEN,JOURNAL='SPC_DEV_CITY_JOURNAL_B015',FLOW='SPC_DEV_CITY_FLOW_B020',INVEST='SPC_DEV_INVESTMENT_LEDGER_V1',TEMPLATES='SPC_STANDARDIZATION_LEDGER_V1'}
 local d={errors={},applying=false,changes=0,ready=false};shared.CityInheritance=d
 local function cp(v) if type(v)~='table' then return v end;local r={};for k,x in pairs(v) do r[k]=cp(x) end;return r end
 local function eq(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a) do if not eq(v,b[k]) then return false end end;for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function read()
  local v=Game:GetProperty(KEY);if v==nil then return {schema=1,records={}} end
  assert(type(v)=='table' and v.schema==1 and type(v.records)=='table','INHERIT_BAD_LEDGER');return cp(v)
 end
 local function save(v) Game:SetProperty(KEY,cp(v));assert(eq(read(),v),'INHERIT_WRITE_FAILED') end
 local function shadow() return Game:GetProperty('SPC_INHERITANCE_SHADOW_V1') or {records={}} end
 local function valid(s)
  local a=s.values;assert(type(a)=='table' and a.TOKEN==s.uid,'INHERIT_TOKEN')
  local j=a.JOURNAL;local f=a.FLOW
  assert(j and j.health=='TRACKING' and j.specialization~='NONE' and j.specialization~='NON_V01' and j.potential==1 and j.first,'INHERIT_EXISTING_IDENTITY_REQUIRED')
  assert(f and f.stage=='DONE' and eq(f.facts,j) and eq(f.target,j),'INHERIT_FLOW_PENDING')
  assert(j.owner==s.owner and j.cityID==s.cityID and j.token==s.uid,'INHERIT_SOURCE_ANCHOR')
  local inv=a.INVEST
  if inv then assert(inv.pending==nil,'INHERIT_PENDING_INVESTMENT');assert(inv.anchor and inv.anchor.token==s.uid and inv.anchor.owner==s.owner and inv.anchor.cityID==s.cityID,'INHERIT_INVEST_ANCHOR') end
 end
 local function find(v,pid,cid)
  local found
  for _,r in pairs(v.records) do if not r.retired and r.owner==pid and r.cityID==cid then assert(not found,'INHERIT_DUPLICATE_ENDPOINT');found=r end end
  return found
 end
 function d.Resolve(pid,c)
  local r=find(read(),pid,c:GetID())
  if r and r.x==c:GetX() and r.y==c:GetY() and c:GetProperty(TOKEN)==r.uid and (r.status=='APPLIED' or d.applying) then return r.uid,'BOUND_MATCH' end
 end
 function d.AllowsShadow(uid,c)
  local r=find(read(),c:GetOwner(),c:GetID());return r and r.uid==uid and r.x==c:GetX() and r.y==c:GetY() and r.status=='APPLIED'
 end
 local function projection(r)
  local a=cp(r.source.values)
  local function anchor(t) if t then t.owner=r.owner;t.cityID=r.cityID end end
  anchor(a.JOURNAL);anchor(a.FLOW)
  for _,k in ipairs({'facts','target','before'}) do anchor(a.FLOW[k]) end
  if a.INVEST then anchor(a.INVEST.anchor) end
  return a
 end
 local function restore(uid)
  local v=read();local r=assert(v.records[uid],'INHERIT_RECORD_MISSING')
  if r.retired or not P.IsTestPlayer(r.owner) then return end
  local c=CityManager.GetCity(r.owner,r.cityID)
  assert(c and c:GetX()==r.x and c:GetY()==r.y,'INHERIT_ENDPOINT_CHANGED')
  if r.status=='APPLIED' then return end
  valid(r.source);local a=projection(r)
  -- Validate all fields before the first write. Resume only our exact partial projection.
  for k,key in pairs(fields) do local now=c:GetProperty(key);assert(now==nil or eq(now,a[k]),'INHERIT_CITY_CONFLICT') end
  r.status='PROJECTING';save(v)
  d.applying=true
  local ok,e=pcall(function()
   for _,k in ipairs({'JOURNAL','FLOW','INVEST','TEMPLATES','TOKEN'}) do
    if a[k]~=nil and not eq(c:GetProperty(fields[k]),a[k]) then c:SetProperty(fields[k],cp(a[k]));assert(eq(c:GetProperty(fields[k]),a[k]),'INHERIT_CITY_WRITE_FAILED') end
   end
   shared.CityFlowProbe.ResumeInherited(r.owner,c)
   shared.EffectiveFacts.Read(r.owner,c)
  end)
  d.applying=false;assert(ok,e)
  v=read();r=v.records[uid];r.status='APPLIED';save(v);d.changes=d.changes+1
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'INHERIT_APPLIED') end
  -- Reuse existing absolute reconciliation, never copy old ACTIVE or route sets.
  for _,name in ipairs({'ResearchSupport','Lv3Support','IndustrySupport','Lv2Housing','Lv2GPP','Lv3Effects','Lv4Percent','CopyYields','StandardizationDiscount','CommerceConvergence'}) do
   local m=shared[name];if m and type(m.Audit)=='function' then pcall(m.Audit) end
  end
 end
 local function transfer(newpid,newcid,oldpid,x,y,kind)
  if not d.ready then return end
  local c=CityManager.GetCity(newpid,newcid)
  assert(c and c:GetX()==x and c:GetY()==y,'INHERIT_TRANSFER_ENDPOINT')
  local v=read();local selected
  for uid,s in pairs(shadow().records) do
   local r=v.records[uid];local owner=r and r.owner or s.owner;local id=r and r.cityID or s.cityID
   if s.x==x and s.y==y and not (r and r.retired) and owner~=newpid and (oldpid==nil or oldpid==owner) then
    assert(not selected,'INHERIT_AMBIGUOUS_PLOT');selected={uid=uid,s=s,r=r,owner=owner,id=id}
   end
  end
  if not selected then
   local r=find(v,newpid,newcid);if r then restore(r.uid) end;return
  end
  local p=selected;local s=p.r and p.r.source or p.s
  -- Prefer a newer snapshot only if it was written by the currently registered owner.
  if p.s.owner==p.owner and p.s.cityID==p.id and (not p.r or p.s.revision>p.r.source.revision) then s=p.s end
  valid(s)
  local existing=c:GetProperty(TOKEN);assert(existing==nil or existing==p.uid,'INHERIT_DEST_TOKEN_CONFLICT')
  local r=p.r or {uid=p.uid,x=x,y=y,revision=0}
  r.previousOwner=p.owner;r.previousCityID=p.id;r.owner=newpid;r.cityID=newcid;r.source=cp(s)
  r.revision=r.revision+1;r.event=kind;r.turn=Game.GetCurrentGameTurn();r.status=P.IsTestPlayer(newpid) and 'PENDING' or 'DORMANT'
  v.records[p.uid]=r;save(v);restore(p.uid)
 end
 local function safe(fn,...)
  local ok,e=pcall(fn,...);if not ok then local code=tostring(e):match('INHERIT_[A-Z_]+') or 'INHERIT_ERROR';d.errors.last=code;print('[SPC][B066] '..tostring(e)) end
 end
 local function hook(ns,n,fn) local e=ns and ns[n];if e and type(e.Add)=='function' then e.Add(function(...) safe(fn,...) end) end end
 hook(GameEvents,'CityConquered',function(newpid,oldpid,cid,x,y) transfer(newpid,cid,oldpid,x,y,'CityConquered') end)
 hook(Events,'CityTransfered',function(pid,cid)
  if type(pid)~='number' or type(cid)~='number' then return end
  local c=CityManager.GetCity(pid,cid);if c then transfer(pid,cid,nil,c:GetX(),c:GetY(),'CityTransfered') end
 end)
 hook(GameEvents,'CityBuilt',function(pid,cid,x,y)
  if not d.ready then return end
  local v=read();local changed=false
  for uid,s in pairs(shadow().records) do
   if s.x==x and s.y==y then local r=v.records[uid]
    if (r and (r.owner~=pid or r.cityID~=cid)) or (not r and (s.owner~=pid or s.cityID~=cid)) then
     r=r or {uid=uid,x=x,y=y,source=cp(s),owner=s.owner,cityID=s.cityID,revision=0}
     r.retired=true;r.status='RETIRED_NEW_FOUNDATION';v.records[uid]=r;changed=true
    end
   end
  end
  if changed then save(v) end
 end)
 hook(Events,'LoadScreenClose',function()
  d.ready=true
  -- Only resume a transfer already durably confirmed; never infer a transfer from coordinates on load.
  for uid,r in pairs(read().records) do if not r.retired and r.status~='APPLIED' then safe(restore,uid) end end
 end)
 function d.Describe(pid)
  assert(P.IsTestPlayer(pid),'INHERIT_PLAYER_REQUIRED');local uid=shadow().watch[tostring(pid)];local r=uid and read().records[uid]
  if not r then return '尚无该城市的已确认转移记录；不会按位置自动恢复。\n错误='..tostring(d.errors.last or '无') end
  return 'B066 既有专业继承\nUID='..r.uid..' | 状态='..r.status..' | 转移次数='..r.revision..'\nOwner/CityID='..r.owner..'/'..r.cityID..' | 来源事件='..tostring(r.event)..'\n错误='..tostring(d.errors.last or '无')..'\n'..shared.InheritanceShadow.Describe(pid)
 end
end
