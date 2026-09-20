include('SampleLifecycle')
include('ResearchCrossModel')
SPCResearchCrossSample={}
local S=SPCResearchCrossSample
local L=SPCSampleLifecycle
function S.Replacements(P)
 local t={};for _,r in ipairs(assert(P.Rows('DistrictReplaces'),'CROSS_CATALOG_UNKNOWN')) do t[r.CivUniqueDistrictType]=r.ReplacesDistrictType end;return t
end
function S.Receive(P,data,pid,p)
 P.Count('cross_receive')
 local issued=ExposedMembers.SPC_C2_cross_issued
 if not data.ready or not P.IsTestPlayer(pid) or type(p)~='table' or not issued
  or issued.pid~=pid or issued.epoch~=p.ClientEpoch or issued.seq~=p.Seq or issued.generation~=p.Generation
  or p.Generation~=data.generation or type(p.Seq)~='number' or p.Seq<1 or p.Seq%1~=0
  or p.Turn~=Game.GetCurrentGameTurn() then P.Count('cross_stale');return false end
 local ack=data.responses[pid]
 if ack and ack.epoch==p.ClientEpoch and p.Seq<=ack.seq then P.Count('cross_duplicate');return false end
 local function respond(status) data.responses[pid]={epoch=p.ClientEpoch,seq=p.Seq,generation=p.Generation,status=status} end
 if p.Valid~=1 then respond('UNAVAILABLE');return false end
 local ok,value=pcall(function()
  assert(type(p.Data)=='string' and #p.Data<=160000 and type(p.Count)=='number' and p.Count>=0 and p.Count<=512 and p.Count%1==0,'CROSS_PAYLOAD_SIZE')
  local live=L.Live(P,pid,false);local rows,canonical={},{};local n=0;local replaces=S.Replacements(P)
  for line in p.Data:gmatch('[^;]+') do
   local fields={};for x in (line..','):gmatch('(.-),') do fields[#fields+1]=x end
   assert(#fields==10,'CROSS_PAYLOAD_SHAPE')
   local cid,did=tonumber(fields[1]),tonumber(fields[2]);assert(cid and did and cid%1==0 and did%1==0,'CROSS_PAYLOAD_ID')
   local key=cid..':'..did;local r=live[key]
   assert(r and r.reference==fields[3] and not rows[key],'CROSS_REFERENCE_STALE')
   local pillaged=r.district:IsPillaged();assert(type(pillaged)=='boolean' and fields[4]==(pillaged and '1' or '0'),'CROSS_PILLAGE_STALE')
   local row={reference=r.reference,id=did,type=r.type,cityID=cid,domain=SPCResearchCrossModel.Domain(r.type,replaces),complete=true,pillaged=pillaged,yields={}}
   local v={key,r.reference,fields[4]}
   for i,y in ipairs(SPCResearchCrossModel.Yields) do
    local a=tonumber(fields[i+4]);assert(a and a==a and math.abs(a)<1e8,'CROSS_VALUE_UNKNOWN')
    row.yields[y]=a;v[#v+1]=string.format('%.17g',a)
   end
   rows[key]=row;n=n+1;canonical[#canonical+1]=table.concat(v,',')
  end
  assert(n==p.Count,'CROSS_PARTIAL_SAMPLE');for k in pairs(live) do assert(rows[k],'CROSS_PARTIAL_SAMPLE') end
  table.sort(canonical);return {rows=rows,signature=table.concat(canonical,';'),turn=p.Turn}
 end)
 data.receiveErrors=data.receiveErrors or {}
 if not ok then data.receiveErrors[pid]=tostring(value);respond('UNAVAILABLE');P.Count('cross_stale');return false end
 data.receiveErrors[pid]=nil;data.seq[pid]=p.Seq
 local old=data.samples[pid]
 if old and old.signature==value.signature then old.turn=p.Turn;respond('UNCHANGED');P.Count('cross_duplicate');return false end
 data.samples[pid]=value;respond('ACCEPTED');P.Count('cross_apply');return true
end
