-- Pure bounded derived recovery framing. Decoding is never source, qualification,
-- carrier-commit or transaction proof. The future Store/caller must prove those.
-- No native surfaces or use of the permanent record's bounded Copy budget.
SPCNetworkRecoveryModel={MaxSources=512,MaxBytes=1048576}
local M=SPCNetworkRecoveryModel
local domains={'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_HOLY_SITE','DISTRICT_HARBOR'}
local domainSet={};for _,key in ipairs(domains)do domainSet[key]=true end
local kinds={NONE=true,RESEARCH=true,CULTURE=true,COMMERCE=true,INDUSTRY=true}
local statuses={CONFIRMED=true,RETAINED=true,UNKNOWN=true}
local function integer(n,limit)return type(n)=='number'and n==n and n>=0 and n<(limit or 9007199254740991)and n%1==0 end
local function fields(t,allowed)
 assert(type(t)=='table'and getmetatable(t)==nil,'NREC_STRUCTURE_INVALID')
 for k in pairs(t)do assert(allowed[k],'NREC_FIELD_UNKNOWN')end
end
local function text(t,limit)return type(t)=='string'and #t>0 and #t<=limit end
local referenceFields={reference=true,stamp=true}
local function witness(v)
 fields(v,referenceFields);assert(text(v.reference,512)and text(v.stamp,512),'NREC_REFERENCE_INVALID')
end
local function number(n)
 assert(type(n)=='number'and n==n and n>=0 and n<math.huge,'NREC_VALUE_INVALID')
 if n==0 then return '0'end
 local s=string.format('%.17g',n);assert(tonumber(s)==n,'NREC_VALUE_ROUNDTRIP');return s
end
local function civ(s)return text(s,128)and s:match('^CIVILIZATION_[A-Z0-9_]+$')end
local rootFields={version=true,family=true,sequence=true,receiver=true,shape=true,sources=true}
local sourceFields={reference=true,stamp=true,status=true,domains=true,eligible=true,civilizations=true}
function M.Validate(v)
 fields(v,rootFields);assert(v.version==1 and(v.family=='COMMERCE'or v.family=='CULTURE')and integer(v.sequence)and v.sequence>0,'NREC_ENVELOPE_INVALID')
 witness(v.receiver)
 if v.family=='COMMERCE'then
  fields(v.shape,{gold=true,access=true});assert(integer(v.shape.gold,2147483648)and type(v.shape.access)=='boolean','NREC_SHAPE_INVALID')
 else
  fields(v.shape,{kind=true,plot=true,count=true});assert(kinds[v.shape.kind]and integer(v.shape.count,256),'NREC_SHAPE_INVALID')
  if v.shape.kind=='NONE'then assert(v.shape.plot==nil and v.shape.count==0,'NREC_SHAPE_INVALID')
  else assert(integer(v.shape.plot,1000000000),'NREC_SHAPE_INVALID')end
 end
 assert(type(v.sources)=='table'and getmetatable(v.sources)==nil,'NREC_STRUCTURE_INVALID')
 local count,all=0,{}
 for id,s in pairs(v.sources)do
  count=count+1;assert(integer(id,1000000000),'NREC_SOURCE_ID_INVALID');assert(count<=M.MaxSources,'NREC_SOURCE_LIMIT');fields(s,sourceFields);assert(statuses[s.status],'NREC_PROVENANCE_INVALID')
  if s.status=='UNKNOWN'then
   assert(s.domains==nil and s.eligible==nil and s.civilizations==nil,'NREC_UNKNOWN_HAS_FACTS')
   assert(s.reference==nil or text(s.reference,512),'NREC_REFERENCE_INVALID');assert(s.stamp==nil or text(s.stamp,512),'NREC_REFERENCE_INVALID')
  else
   witness({reference=s.reference,stamp=s.stamp})
   if v.family=='COMMERCE'then
    assert(s.eligible==nil and s.civilizations==nil,'NREC_FAMILY_INVALID');fields(s.domains,domainSet)
    for _,d in pairs(s.domains)do
     fields(d,{eligible=true,X=true});assert(type(d.eligible)=='boolean','NREC_ELIGIBILITY_INVALID')
     if d.eligible then number(d.X)else assert(d.X==nil,'NREC_INELIGIBLE_HAS_VALUE')end
    end
   else
    assert(s.domains==nil and type(s.eligible)=='boolean','NREC_FAMILY_INVALID');assert(type(s.civilizations)=='table'and getmetatable(s.civilizations)==nil,'NREC_STRUCTURE_INVALID')
    local n=0;for c,yes in pairs(s.civilizations)do assert(civ(c)and yes==true,'NREC_CIV_INVALID');n=n+1;assert(n<=64,'NREC_CIV_SOURCE_LIMIT');all[c]=true end
    assert(s.eligible or n==0,'NREC_INELIGIBLE_HAS_VALUE')
   end
  end
 end
 local n=0;for _ in pairs(all)do n=n+1 end;assert(n<256,'NREC_CIV_DICTIONARY_LIMIT')
 return v
end
function M.Encode(v)
 M.Validate(v);local parts,bytes={},0
 local function put(s)
  assert(type(s)=='string','NREC_FRAME_INVALID');local frame=#s..':'..s;bytes=bytes+#frame;assert(bytes<=M.MaxBytes,'NREC_BYTE_LIMIT');parts[#parts+1]=frame
 end
 local function int(n)put(string.format('%.0f',n))end
 local function boolean(b)put(b and '1'or'0')end
 put('SPC_NETWORK_RECOVERY');put('1');put(v.family);int(v.sequence);put(v.receiver.reference);put(v.receiver.stamp)
 if v.family=='COMMERCE'then int(v.shape.gold);boolean(v.shape.access)
 else put(v.shape.kind);put(v.shape.plot==nil and ''or string.format('%.0f',v.shape.plot));int(v.shape.count)end
 local dictionary,index={},{}
 if v.family=='CULTURE'then
  for _,s in pairs(v.sources)do for c in pairs(s.civilizations or {})do index[c]=true end end
  for c in pairs(index)do dictionary[#dictionary+1]=c end;table.sort(dictionary)
  int(#dictionary);for i,c in ipairs(dictionary)do put(c);index[c]=i end
 end
 local ids={};for id in pairs(v.sources)do ids[#ids+1]=id end;table.sort(ids);int(#ids)
 for _,id in ipairs(ids)do
  local s=v.sources[id];int(id);put(s.status);put(s.reference or '');put(s.stamp or '')
  if s.status~='UNKNOWN'then
   if v.family=='COMMERCE'then
    local n=0;for _ in pairs(s.domains)do n=n+1 end;int(n)
    for i,key in ipairs(domains)do local d=s.domains[key];if d then int(i);boolean(d.eligible);if d.eligible then put(number(d.X))end end end
   else
    boolean(s.eligible);local values={};for c in pairs(s.civilizations)do values[#values+1]=index[c]end;table.sort(values);int(#values);for _,i in ipairs(values)do int(i)end
   end
  end
 end
 return table.concat(parts)
end
function M.Decode(wire)
 assert(type(wire)=='string'and #wire<=M.MaxBytes,'NREC_WIRE_INVALID');local at=1
 local function get()
  local colon=wire:find(':',at,true);assert(colon and colon-at>=1 and colon-at<=7,'NREC_FRAME_INVALID')
  local size=wire:sub(at,colon-1);assert(size=='0'or size:match('^[1-9]%d*$'),'NREC_FRAME_INVALID')
  local n=tonumber(size);assert(n<=M.MaxBytes and colon+n<=#wire,'NREC_FRAME_INVALID')
  local s=wire:sub(colon+1,colon+n);at=colon+n+1;return s
 end
 local function int(limit)
  local s=get();assert(s=='0'or s:match('^[1-9]%d*$'),'NREC_INTEGER_INVALID');local n=tonumber(s)
  assert(integer(n,limit)and string.format('%.0f',n)==s,'NREC_INTEGER_INVALID');return n
 end
 local function boolean()local s=get();assert(s=='0'or s=='1','NREC_BOOLEAN_INVALID');return s=='1'end
 assert(get()=='SPC_NETWORK_RECOVERY'and get()=='1','NREC_VERSION_UNSUPPORTED')
 local v={version=1,family=get(),sequence=int(),receiver={reference=get(),stamp=get()},shape={},sources={}}
 assert(v.family=='COMMERCE'or v.family=='CULTURE','NREC_FAMILY_INVALID')
 if v.family=='COMMERCE'then v.shape.gold=int(2147483648);v.shape.access=boolean()
 else v.shape.kind=get();local s=get();if s~=''then assert(s:match('^%d+$'),'NREC_INTEGER_INVALID');v.shape.plot=tonumber(s)end;v.shape.count=int(256)end
 local dictionary={}
 if v.family=='CULTURE'then
  local n=int(256);local seen={};for i=1,n do local s=get();assert(civ(s)and not seen[s],'NREC_CIV_INVALID');seen[s]=true;dictionary[i]=s end
 end
 local n=int(M.MaxSources+1)
 for _=1,n do
  local id=int(1000000000);assert(v.sources[id]==nil,'NREC_DUPLICATE_SOURCE')
  local s={status=get()};local reference,stamp=get(),get();s.reference=reference~=''and reference or nil;s.stamp=stamp~=''and stamp or nil
  assert(statuses[s.status],'NREC_PROVENANCE_INVALID');v.sources[id]=s
  if s.status~='UNKNOWN'then
   if v.family=='COMMERCE'then
    s.domains={};local count=int(6)
    for _=1,count do
     local key=domains[int(6)];assert(key and not s.domains[key],'NREC_DOMAIN_INVALID')
     local d={eligible=boolean()};s.domains[key]=d
     if d.eligible then local encoded=get();local value=tonumber(encoded);assert(value and number(value)==encoded,'NREC_VALUE_INVALID');d.X=value end
    end
   else
    s.eligible=boolean();s.civilizations={};local count=int(65)
    for _=1,count do local c=dictionary[int(256)];assert(c and not s.civilizations[c],'NREC_CIV_INVALID');s.civilizations[c]=true end
   end
  end
 end
 assert(at==#wire+1,'NREC_TRAILING_BYTES');M.Validate(v);assert(M.Encode(v)==wire,'NREC_NOT_CANONICAL');return v
end
