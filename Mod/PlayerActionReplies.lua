-- Fixed, bounded session transport. Not transaction authority or replay control.
SPCPlayerActionReplies={CAPACITY=8}
function SPCPlayerActionReplies.New(epoch,version)
 local function integer(n)return type(n)=='number' and n>=0 and n<9007199254740992 and n%1==0 end
 local function text(s,max)return type(s)=='string' and #s>0 and #s<=max end
 assert(integer(epoch) and epoch>0 and text(version,128),'PLAYER_REPLY_SESSION')
 local d={epoch=epoch,version=version,scope='UNIT_ACTION'}
 local slots,index={},{};local cursor,count=0,0;local closed=false
 local actions={UNIT_ACTION_PREPARE=true,UNIT_ACTION_CONFIRM=true}
 local function key(pid,token)
  if not integer(pid) or not text(token,256)then return nil end
  return tostring(pid)..':'..token
 end
 function d.Accepts(pid,p)
  return not closed and type(p)=='table' and getmetatable(p)==nil
   and key(pid,p.Token)~=nil and p.ReplyChannel=='UNIT_ACTION' and p.ReplyEpoch==epoch
   and actions[p.Action]==true and integer(p.UnitID)or false
 end
 local function erase(i)
  local row=slots[i]
  if row then index[key(row.owner,row.token)]=nil;slots[i]=nil;count=count-1 end
  return row
 end
 function d.Publish(pid,p,value,outcome)
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
  local k=key(pid,p.Token)
  if index[k]then return false,'ALREADY_RETAINED'end -- first retained terminal evidence wins
  local row={owner=pid,token=p.Token,action=p.Action,unitID=p.UnitID,
   epoch=epoch,version=version,text=value,outcome=result}
  cursor=cursor%8+1;erase(cursor);slots[cursor]=row;index[k]=cursor;count=count+1
  return true
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
 local old=shared.PlayerActionReplies
 if old and type(old.Shutdown)=='function'then old.Shutdown()end
 ExposedMembers.SPC_PlayerActionReplyEpoch=previous+1
 shared.PlayerActionReplies=d
 return d
end
