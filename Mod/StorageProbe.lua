-- B012 synthetic Game Property only. No city identity or specialization writes.
SPCStorageProbe={}
function SPCStorageProbe.Start(P,shared)
 local data={version=P.VERSION,players={}};shared.StorageProbe=data
 local function expected(pid)
  return {schema=1,owner=pid,revision=1,counter=2,records={
   ["sample:alpha"]={uid="DEV-1",number=17,enabled=true,nested={value=0.5}},
   ["sample:beta"]={uid="DEV-2",number=0,enabled=false,nested={value=42}}}}
 end
 local function equal(a,b,depth)
  if depth>8 or type(a)~=type(b) then return false end
  if type(a)~="table" then return a==b end
  for k,v in pairs(b) do if not equal(a[k],v,depth+1) then return false end end
  for k in pairs(a) do if b[k]==nil then return false end end
  return true
 end
 function data.Run(pid,write)
  if not P.IsTestPlayer(pid) then return "OUTSIDE_TEST_CIV" end
  local b=data.players[pid] or {attempts=0};data.players[pid]=b
  local key="SPC_DEV_STORAGE_B012_P"..tostring(pid)
  local want=expected(pid)
  local ok,value=pcall(function() return Game:GetProperty(key) end)
  local state="READ_ERROR"
  if ok then
   if value==nil then state="EMPTY"
   elseif equal(value,want,0) then state="MATCH"
   else state="MISMATCH_NO_OVERWRITE" end
  end
  if write and state=="EMPTY" then
   b.attempts=b.attempts+1
   local ack=pcall(function() Game:SetProperty(key,want) end)
   local readOK,after=pcall(function() return Game:GetProperty(key) end)
   state=readOK and (equal(after,expected(pid),0) and "MATCH" or "WRITE_UNCONFIRMED") or "READBACK_ERROR"
   b.ack=ack and "RETURNED" or "THREW_CHECK_READBACK"
  elseif write and state=="MATCH" then state="MATCH_NO_WRITE" end
  b.state=state
  b.text=table.concat({P.VERSION.." | DEV表存储 "..state,
   "本次加载实际写入尝试="..b.attempts.." | writeCall="..tostring(b.ack or "NONE"),
   "期望/完整核对：revision=1 counter=2 records=2",
   "DEV-1: 17 / true / nested=0.5",
   "DEV-2: 0 / false / nested=42",
   "MATCH表示所有键和值一致；不等于实机验收已通过。",
   "仅专用Game Property；没有城市专业/Potential写入。"},"\n")
  print("[SPC][B012][STORAGE] "..b.text)
  return b.text
 end
end
