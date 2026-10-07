include('NetworkInput')
SPCInspirationReadout={}
local baseline,diagnosticCache
local expected={SPC_INSPIRE_PROBE_1=0.1,SPC_INSPIRE_PROBE_3=0.3,SPC_INSPIRE_PROBE_6=0.6,SPC_INSPIRE_PROBE_10=1}
local SCIENTIST='GREAT_PERSON_CLASS_SCIENTIST'
local function tr(k,...)return Locale.Lookup('LOC_SPC_INSPIRE_'..k,...)end
local function finite(v)return type(v)=='number' and v==v and math.abs(v)~=math.huge end
local function scalar(v)
 if type(v)~='string' and not finite(v) and type(v)~='boolean' then return 'UNKNOWN' end
 return tostring(v):gsub('[\r\n]',' '):gsub('%[NEWLINE%]',' '):sub(1,192)
end
local function api(name,...)
 local fn=GameEffects and GameEffects[name]
 if type(fn)~='function' then return false,nil end
 return pcall(fn,...)
end
local function array(t,limit)
 if type(t)~='table' then return nil end
 local n,seen=0,{}
 for k,v in pairs(t)do
  n=n+1
  if n>limit or not finite(k) or k%1~=0 or k<1 or k>limit then return nil end
  if not finite(v) and type(v)~='string' then return nil end
  local key=type(v)..':'..tostring(v);if seen[key] then return nil end;seen[key]=true
 end
 for i=1,n do if t[i]==nil then return nil end end
 return n
end
local function diagnose(P,view)
 local lines={tr('DIAG_TITLE')};local probes,percent={},{};local complete=true
 local localCount,unknown,omitted=0,0,0
 local function object(id)
  local pk,p=api('GetObjectsPlayerId',id);local tk,t=api('GetObjectType',id);local sk,s=api('GetObjectString',id)
  -- Object IDs are opaque; the raw type/string is evidence, not a CityID mapping.
  return {player=pk and finite(p) and p%1==0 and p or nil,kind=tk and scalar(t) or 'UNKNOWN',raw=sk and scalar(s) or 'UNKNOWN',
   available=pk and finite(p) and p%1==0 and tk and type(t)=='string' and sk and type(s)=='string'}
 end
 local ok,ids=api('GetModifiers');local n=ok and array(ids,32768) or nil
 if not n then return tr('DIAG_TITLE')..'\n'..tr('DIAG_UNKNOWN','MODIFIER_ENUMERATION_UNAVAILABLE_OR_INVALID')..'\n'..tr('DIAG_MULTIPLIER')end
 for i=1,n do
  local id=ids[i];local good,def=api('GetModifierDefinition',id)
  if not good or type(def)~='table' or type(def.Id)~='string' then complete=false
  else
   local args=type(def.Arguments)=='table' and def.Arguments or nil
   local isProbe=expected[def.Id]~=nil;local isPercent=false
   if not isProbe and args then
    local m=P.Info('Modifiers',def.Id);local dm=m and P.Info('DynamicModifiers',m.ModifierType)
    isPercent=dm and dm.EffectType=='EFFECT_ADJUST_GREAT_PERSON_POINTS_PERCENT'
      and (args.GreatPersonClassType==nil or args.GreatPersonClassType==SCIENTIST)
   end
   if isProbe or isPercent then
    local ownerOK,ownerID=api('GetModifierOwner',id);local owner=ownerOK and object(ownerID) or {kind='UNKNOWN',raw='UNKNOWN'}
    if not owner.available then complete=false end
    -- Percent sources may affect a player via Subjects despite a foreign Owner.
    local sk,subjects=api('GetModifierSubjects',id);local sn=sk and array(subjects,64) or nil
    if isPercent and not sn then complete=false end
    local subjectRows,affects={},false
    if sn then
     for j=1,sn do
      local o=object(subjects[j]);if not o.available then complete=false end;if o.player==view.owner then affects=true end
      if j<=2 then subjectRows[#subjectRows+1]=tr('DIAG_SUBJECT',j,scalar(o.player),o.kind,o.raw)end
     end
    end
    local relevant=isProbe and (owner.player==view.owner or owner.player==nil)
     or isPercent and (owner.player==view.owner or affects or owner.player==nil or not sn)
    if relevant then
     local ak,active=api('GetModifierActive',id)
     if not ak or type(active)~='boolean' or not args or not sn then complete=false end
     if isProbe then
      if not args or not finite(tonumber(args.Amount)) or args.GreatPersonClassType~=SCIENTIST then complete=false end
      if owner.player==view.owner then localCount=localCount+1 else unknown=unknown+1 end
     end
     local activeValue='UNKNOWN';if ak and type(active)=='boolean' then activeValue=tostring(active)end
     local rows=isProbe and probes or percent
     if #rows>=8 then omitted=omitted+1
     else
      local first=isProbe and tr('DIAG_PROBE',scalar(id),activeValue,scalar(args and args.Amount),expected[def.Id],scalar(args and args.GreatPersonClassType))
       or tr('DIAG_PERCENT',scalar(def.Id),activeValue,scalar(args and args.Amount),scalar(args and args.GreatPersonClassType))
      rows[#rows+1]={first,tr('DIAG_OWNER',scalar(owner.player),owner.kind,owner.raw),tr('DIAG_SUBJECTS',sn and tostring(sn) or 'UNKNOWN'),table.concat(subjectRows,'\n')}
     end
    end
   end
  end
 end
 ids=nil -- No history, object cache, or native handles retained across requests.
 lines[#lines+1]=tr('DIAG_SCAN',complete and 'COMPLETE' or 'INCOMPLETE',localCount,unknown)
 if #probes==0 and complete then lines[#lines+1]=tr('DIAG_NONE')end
 if not complete then lines[#lines+1]=tr('DIAG_UNKNOWN','INCOMPLETE_FIELDS_OR_DEFINITIONS')end
 for _,row in ipairs(probes)do for _,line in ipairs(row)do if line~='' then lines[#lines+1]=line end end end
 lines[#lines+1]=tr('DIAG_MULTIPLIER')
 for _,row in ipairs(percent)do for _,line in ipairs(row)do if line~='' then lines[#lines+1]=line end end end
 if omitted>0 then lines[#lines+1]=tr('DIAG_LIMIT',omitted)end
 return table.concat(lines,'\n')
end
function SPCInspirationReadout.Render(P,view,token,action)
 if not view or view.token~=token or view.owner~=Game.GetLocalPlayer()then baseline=nil;diagnosticCache=nil;return tr('READ_UNKNOWN')end
 local c=Players[view.owner]:GetCities():FindID(view.city)
 if not c or SPCNetworkInput.Reference(c)~=view.reference then baseline=nil;diagnosticCache=nil;return tr('READ_UNKNOWN')end
 local ok,rate=pcall(function()return Players[view.owner]:GetGreatPeoplePoints():GetPointsPerTurn(P.Info('GreatPersonClasses',SCIENTIST).Index)end)
 local turn=Game.GetCurrentGameTurn();local text=tr('TURN',turn)
 if ok and finite(rate)then
  if view.stage==0 then baseline={rate=rate,turn=turn,reference=view.reference,session=view.session}end
  text=text..'\n'..tr('NATIVE',string.format('%.3f',rate))
  if baseline and baseline.turn==turn and baseline.reference==view.reference and (baseline.session==view.session or action=='INSPIRE_END' or view.stage<0)then
   text=text..'\n'..tr('DELTA',string.format('%.3f',rate-baseline.rate))
  else text=text..'\n'..tr('NO_BASELINE')end
 else text=text..'\n'..tr('READ_UNKNOWN')end
 if action=='INSPIRE_READ' or action=='INSPIRE_END' or view.stage<0 then
  if not diagnosticCache or diagnosticCache.token~=token or diagnosticCache.reference~=view.reference or diagnosticCache.turn~=turn then
   local good,out=pcall(diagnose,P,view)
   diagnosticCache={token=token,reference=view.reference,turn=turn,text=good and out or tr('DIAG_UNKNOWN','DIAGNOSTIC_READ_FAILED')}
  end
  text=text..'\n'..diagnosticCache.text
 end
 if view.stage<0 then baseline=nil end
 return text..'\n'..tr('SCOPE')
end
