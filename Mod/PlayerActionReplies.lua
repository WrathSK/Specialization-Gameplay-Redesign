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
 -- Payloads come from our own Gameplay producers in the same package. Only the
 -- request identity and the transport budgets are checked here (Owner 2026-11-25:
 -- no format re-validation; a malformed payload is a producer bug and may throw).
 function d.Publish(pid,p,value,outcome)
  if scope~='UNIT_ACTION'then return false,'INVALID_SCOPE'end
  if not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if #value>200000 then return false,'TEXT_BUDGET'end
  local result
  if outcome~=nil then result={status=outcome.status,kind=outcome.kind,phase=outcome.phase}end
  return put(pid,p,{text=value,outcome=result})
 end
 function d.PublishView(pid,p,view)
  if scope~='UNIT_VIEW'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if view.owner~=pid or view.unitID~=p.UnitID or view.token~=p.Token then return false,'VIEW_IDENTITY_CHANGED'end
  local out={legal=view.legal,prepared=view.prepared,targetName=view.targetName}
  for _,field in ipairs({'owner','unitID','turn','x','y','amount','progress','cost','baseInput','baseUnused','potential','nextPotential'})do
   out[field]=view[field] -- preserve original precision/range; this is no business policy
  end
  for field,limit in pairs({token=256,planToken=256,reason=200000,specialization=128})do
   local v=view[field]
   if v~=nil and #v>limit then return false,'VIEW_TEXT_BUDGET'end
   out[field]=v
  end
  if type(view.targetName)=='string'and #view.targetName>20000 then return false,'VIEW_TEXT_BUDGET'end
  return put(pid,p,{view=out})
 end
 function d.FailView(pid,p)
  if scope~='UNIT_VIEW'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  return put(pid,p,{error='VIEW_UNAVAILABLE'}) -- explicit negative delivery, never a zero/success view
 end
 -- Transport budgets only; target discovery keeps its original native scope.
 function d.PublishTargets(pid,p,s)
  if scope~='UNIT_TARGETS'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if s.owner~=pid or s.unitID~=p.UnitID or s.token~=p.Token or s.version~=version then return false,'TARGETS_IDENTITY_CHANGED'end
  local out={owner=pid,unitID=p.UnitID,token=p.Token,version=version,turn=s.turn,x=s.x,y=s.y,
   error=s.error,mode=s.mode,plots={},unknown={}}
  local budget=#(s.error or '')+#(s.mode or '')
  if #(s.error or '')>20000 or #(s.mode or '')>128 then return false,'TARGET_TEXT_BUDGET'end
  if #s.plots+#s.unknown>4096 then return false,'TARGET_ROWS_LIMIT'end
  for i,row in ipairs(s.plots)do out.plots[i]={plot=row.plot}end
  for i,row in ipairs(s.unknown)do
   if #row.reason>20000 then return false,'TARGET_TEXT_BUDGET'end
   budget=budget+#row.reason
   out.unknown[i]={cityID=row.cityID,reason=row.reason}
  end
  if budget>262144 then return false,'TARGET_TEXT_BUDGET'end
  return put(pid,p,{targets=out})
 end
 function d.FailTargets(pid,p)
  if scope~='UNIT_TARGETS'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  return put(pid,p,{error='TARGETS_UNAVAILABLE'}) -- never a successful empty/partial map
 end
 function d.PublishPresentation(pid,p,s)
  if scope~='CITY_PRESENTATION'or not d.Accepts(pid,p)then return false,'STALE_OR_INVALID_REQUEST'end
  if s.owner~=pid or s.cityID~=p.CityID or s.token~=p.Token then return false,'PRESENTATION_IDENTITY_CHANGED'end
  local budget,over=0,false
  local function copy(src,fields,strings)
   local out={}
   for _,k in ipairs(fields)do out[k]=src[k]end
   for k,limit in pairs(strings or {})do
    local v=src[k]
    if v~=nil then
     budget=budget+#v
     if #v>limit then over=true end
     out[k]=v
    end
   end
   return out
  end
  local out=copy(s,{'owner','cityID','potential','investments','active','x','y'},
   {token=256,specialization=128,progression=128,activeStatus=128,error=20000})
  if s.institutionArchive~=nil then out.institutionArchive=copy(s.institutionArchive,{'RESEARCH','CULTURE','COMMERCE','INDUSTRY'})end
  local sum=s.institutionSummary
  if sum~=nil then
   local v=copy(sum,{'revision','dialogue','engineering','insights','buildingTemplates','districtTemplates',
    'known','reputationKnown','traditionKnown','dialogueKnown','engineeringKnown','insightsKnown','templatesKnown'},{token=256})
   if sum.reference~=nil then v.reference=copy(sum.reference,{'owner','cityID','x','y'})end
   for _,k in ipairs({'tradition','reputation'})do
    local t=sum[k]
    if t==false then v[k]=false
    elseif t~=nil then
     v[k]=copy(t,k=='tradition'and {'age','cursor','percent','nextAge'}or {'age'},{state=128})
    end
   end
   out.institutionSummary=v
  end
  if over or budget>32768 then return false,'PRESENTATION_TEXT_BUDGET'end
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
