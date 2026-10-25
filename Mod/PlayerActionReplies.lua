-- Fixed, bounded session transport. Not transaction authority or replay control.
SPCPlayerActionReplies={CAPACITY=8}
function SPCPlayerActionReplies.New(epoch,version,scope)
 local function integer(n)return type(n)=='number' and n>=0 and n<9007199254740992 and n%1==0 end
 local function text(s,max)return type(s)=='string' and #s>0 and #s<=max end
 assert(integer(epoch) and epoch>0 and text(version,128),'PLAYER_REPLY_SESSION')
 if scope==nil then scope='UNIT_ACTION'end;assert(scope=='UNIT_ACTION'or scope=='UNIT_VIEW'or scope=='UNIT_TARGETS'or scope=='CITY_PRESENTATION','PLAYER_REPLY_SCOPE')
 local d={epoch=epoch,version=version,scope=scope}
 local slots,index={},{};local cursor,count=0,0;local closed=false
 local actions=scope=='UNIT_ACTION'and {UNIT_ACTION_PREPARE=true,UNIT_ACTION_CONFIRM=true}or(scope=='UNIT_VIEW'and {UNIT_ACTION_VIEW=true}or(scope=='UNIT_TARGETS'and {UNIT_TARGETS_READ=true}or {CITY_PRESENTATION_READ=true}))
 local function key(pid,token)
  if not integer(pid) or not text(token,256)then return nil end
  return tostring(pid)..':'..token
 end
 function d.Accepts(pid,p)
  return not closed and type(p)=='table' and getmetatable(p)==nil
   and key(pid,p.Token)~=nil and p.ReplyChannel==scope and p.ReplyEpoch==epoch
   and actions[p.Action]==true and((scope=='CITY_PRESENTATION'and integer(p.CityID))or(scope~='CITY_PRESENTATION'and integer(p.UnitID)))or false
 end
 local function erase(i)
  local row=slots[i]
  if row then index[key(row.owner,row.token)]=nil;slots[i]=nil;count=count-1 end
  return row
 end
 local function put(pid,p,payload)
  local k=key(pid,p.Token)
  if index[k]then return false,'ALREADY_RETAINED'end
  local row={owner=pid,token=p.Token,action=p.Action,unitID=scope~='CITY_PRESENTATION'and p.UnitID or nil,
   cityID=scope=='CITY_PRESENTATION'and p.CityID or nil,
   epoch=epoch,version=version}
  for k,v in pairs(payload)do row[k]=v end
  cursor=cursor%8+1;erase(cursor);slots[cursor]=row;index[k]=cursor;count=count+1
  return true
 end
 function d.Publish(pid,p,value,outcome)
  if scope~='UNIT_ACTION'then return false,'INVALID_SCOPE'end
  if not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if type(value)~='string' or #value>200000 then return false,'INVALID_TEXT'end
  local result
  if outcome~=nil then
   if type(outcome)~='table' or getmetatable(outcome)~=nil then return false,'INVALID_OUTCOME'end
   result={}
   for _,field in ipairs({'status','kind','phase'})do
    local v=outcome[field]
    if v~=nil and not text(v,128)then return false,'INVALID_OUTCOME'end
    result[field]=v
   end
  end
  return put(pid,p,{text=value,outcome=result})
 end
 function d.PublishView(pid,p,view)
  if scope~='UNIT_VIEW'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if type(view)~='table'or getmetatable(view)~=nil or view.owner~=pid
   or view.unitID~=p.UnitID or view.token~=p.Token
   or type(view.legal)~='boolean'or type(view.prepared)~='boolean'then return false,'INVALID_VIEW'end
  local out={legal=view.legal,prepared=view.prepared}
  for _,field in ipairs({'owner','unitID','turn','x','y','amount','progress','cost','baseInput','baseUnused','potential','nextPotential'})do
   local v=view[field]
   if v~=nil and(type(v)~='number'or v~=v or v<=-math.huge or v>=math.huge)then return false,'INVALID_VIEW_NUMBER'end
   out[field]=v -- preserve original precision/range; this is no business policy
  end
  for field,limit in pairs({token=256,planToken=256,reason=200000,specialization=128})do
   local v=view[field]
   if v~=nil and(type(v)~='string'or #v>limit)then return false,'INVALID_VIEW_TEXT'end
   out[field]=v
  end
  local name=view.targetName
  if name~=nil and not(type(name)=='string'and #name<=20000)
   and not(type(name)=='number'and name==name and name>-math.huge and name<math.huge)then return false,'INVALID_VIEW_NAME'end
  out.targetName=name
  return put(pid,p,{view=out})
 end
 function d.FailView(pid,p)
  if scope~='UNIT_VIEW'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  return put(pid,p,{error='VIEW_UNAVAILABLE'}) -- explicit negative delivery, never a zero/success view
 end
 -- Transport budgets only; target discovery keeps its original native scope.
 function d.PublishTargets(pid,p,s)
  if scope~='UNIT_TARGETS'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if type(s)~='table'or getmetatable(s)~=nil or s.owner~=pid or s.unitID~=p.UnitID
   or s.token~=p.Token or s.version~=version then return false,'INVALID_TARGETS'end
  local out={owner=pid,unitID=p.UnitID,token=p.Token,version=version,plots={},unknown={}}
  for _,field in ipairs({'turn','x','y'})do
   local v=s[field];if v~=nil and not integer(v)then return false,'INVALID_TARGET_STAMP'end;out[field]=v
  end
  local budget=0;local rows=0
  local function stringValue(v,limit)
   if type(v)~='string'or #v>limit then return false end
   budget=budget+#v;return budget<=262144
  end
  if s.error~=nil then
   if not stringValue(s.error,20000)then return false,'INVALID_TARGET_ERROR'end;out.error=s.error
  end
  if s.mode~=nil then
   if not stringValue(s.mode,128)then return false,'INVALID_TARGET_MODE'end;out.mode=s.mode
  elseif s.error==nil then return false,'MISSING_TARGET_MODE'end
  for _,field in ipairs({'plots','unknown'})do
   local src=s[field]
   if type(src)~='table'or getmetatable(src)~=nil or #src>4096 then return false,'INVALID_TARGET_ROWS'end
   local n=0
   for k in pairs(src)do
    if not integer(k)or k<1 or k>#src then return false,'INVALID_TARGET_ARRAY'end;n=n+1
   end
   rows=rows+n;if n~=#src or rows>4096 then return false,'TARGET_ROWS_LIMIT'end
   for i=1,n do
    local row=src[i]
    if type(row)~='table'or getmetatable(row)~=nil then return false,'INVALID_TARGET_ROW'end
    if field=='plots'then
     if not integer(row.plot)then return false,'INVALID_TARGET_PLOT'end
     out.plots[i]={plot=row.plot}
    else
     if not integer(row.cityID)or not stringValue(row.reason,20000)then return false,'INVALID_TARGET_UNKNOWN'end
     out.unknown[i]={cityID=row.cityID,reason=row.reason}
    end
   end
  end
  return put(pid,p,{targets=out})
 end
 function d.FailTargets(pid,p)
  if scope~='UNIT_TARGETS'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  return put(pid,p,{error='TARGETS_UNAVAILABLE'}) -- never a successful empty/partial map
 end
 function d.PublishPresentation(pid,p,s)
  if scope~='CITY_PRESENTATION'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if type(s)~='table'or getmetatable(s)~=nil or s.owner~=pid or s.cityID~=p.CityID
   or s.token~=p.Token then return false,'INVALID_PRESENTATION'end
  local ok,out=pcall(function()
   local budget=0
   local function copy(src,numbers,booleans,strings)
    assert(type(src)=='table'and getmetatable(src)==nil,'PRESENTATION_TABLE')
    local out={}
    for _,k in ipairs(numbers or {})do
     local v=src[k];assert(v==nil or(type(v)=='number'and v==v and v>-math.huge and v<math.huge),'PRESENTATION_NUMBER');out[k]=v
    end
    for _,k in ipairs(booleans or {})do
     local v=src[k];assert(v==nil or type(v)=='boolean','PRESENTATION_BOOLEAN');out[k]=v
    end
    for k,limit in pairs(strings or {})do
     local v=src[k]
     if v~=nil then assert(type(v)=='string'and #v<=limit,'PRESENTATION_TEXT');budget=budget+#v;assert(budget<=32768,'PRESENTATION_TEXT_BUDGET');out[k]=v end
    end
    return out
   end
   local out=copy(s,{'owner','cityID','potential','investments','active','x','y'},nil,
    {token=256,specialization=128,progression=128,activeStatus=128,error=20000})
   if s.institutionArchive~=nil then out.institutionArchive=copy(s.institutionArchive,{'RESEARCH','CULTURE','COMMERCE','INDUSTRY'})end
   local sum=s.institutionSummary
   if sum~=nil then
    local v=copy(sum,{'revision','dialogue','engineering','insights','buildingTemplates','districtTemplates'},
     {'known','reputationKnown','traditionKnown','dialogueKnown','engineeringKnown','insightsKnown','templatesKnown'},{token=256})
    if sum.reference~=nil then v.reference=copy(sum.reference,{'owner','cityID','x','y'})end
    for _,k in ipairs({'tradition','reputation'})do
     local t=sum[k]
     if t==false then v[k]=false
     elseif t~=nil then
      v[k]=copy(t,k=='tradition'and {'age','cursor','percent','nextAge'}or {'age'},nil,{state=128})
     end
    end
    out.institutionSummary=v
   end
   return out
  end)
  if not ok then return false,'INVALID_PRESENTATION_FIELDS'end
  return put(pid,p,{presentation=out})
 end
 function d.FailPresentation(pid,p)
  if scope~='CITY_PRESENTATION'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  return put(pid,p,{error='PRESENTATION_UNAVAILABLE'})
 end
 function d.Has(pid,token)return not closed and index[key(pid,token)]~=nil or false end
 function d.Take(pid,token)
  if closed then return nil end
  local i=index[key(pid,token)];return i and erase(i)or nil
 end
 function d.Discard(pid,token)
  if closed then return false end
  local i=index[key(pid,token)];if i then erase(i);return true end;return false
 end
 function d.Count()return count end
 function d.Shutdown()closed=true;slots={};index={};count=0 end
 return d
end
-- One explicit Gameplay producer service. Session metadata only, not a save.
function SPCPlayerActionReplies.Start(P,shared)
 local previous=ExposedMembers.SPC_PlayerActionReplyEpoch or 0
 assert(type(previous)=='number' and previous>=0 and previous<9007199254740991
  and previous%1==0,'PLAYER_REPLY_EPOCH')
 local d=SPCPlayerActionReplies.New(previous+1,P.VERSION)
 local views=SPCPlayerActionReplies.New(previous+1,P.VERSION,'UNIT_VIEW')
 local targets=SPCPlayerActionReplies.New(previous+1,P.VERSION,'UNIT_TARGETS')
 local presentations=SPCPlayerActionReplies.New(previous+1,P.VERSION,'CITY_PRESENTATION')
 d.Views=views;d.Targets=targets;d.Presentations=presentations -- independent fixed-role spaces
 local shutdown=d.Shutdown
 d.Shutdown=function()presentations.Shutdown();targets.Shutdown();views.Shutdown();shutdown()end
 local old=shared.PlayerActionReplies
 if old and type(old.Shutdown)=='function'then old.Shutdown()end
 ExposedMembers.SPC_PlayerActionReplyEpoch=previous+1
 shared.PlayerActionReplies=d
 return d
end
