-- P0-F1: Research-only age model/readout. No yield, carrier or global GC writer.
SPCResearchTradition={}
local M=SPCResearchTradition
local function integer(v)return type(v)=='number' and v>=0 and v<1000000000 and v%1==0 end
local states={COUNTING=true,PAUSED_IDENTITY=true,OWNER_POLICY_UNRESOLVED=true,UNKNOWN_INTERVAL=true}
function M.Validate(t,r)
 assert(type(t)=='table' and t.version==1 and integer(t.start) and integer(t.age)
  and integer(t.cursor) and t.cursor>=t.start and t.age<=t.cursor-t.start
  and states[t.state] and type(t.receipt)=='string' and #t.receipt>0,'TRADITION_RECORD_INVALID')
 if r then
  assert(r.investment and r.investment.investments[t.receipt] and r.base.first
   and t.start>=r.base.first.turn,'TRADITION_ORIGIN_RECEIPT_MISSING')
  local count=0;for _ in pairs(r.investment.investments)do count=count+1 end
  assert(count==3,'TRADITION_P4_RECEIPTS_REQUIRED')
 end
end
function M.Begin(turn,receipt)
 local t={version=1,start=turn,age=0,cursor=turn,state='COUNTING',receipt=receipt}
 M.Validate(t);return t
end
-- A caller must provide ordered, reliable identity transitions. No ACTIVE input.
-- Unknown/missed intervals fail closed; do not infer an identity history on load.
function M.Advance(t,turn,identity)
 M.Validate(t);assert(integer(turn) and turn>=t.cursor,'TRADITION_TURN_INVALID')
 assert(type(identity)=='string','TRADITION_IDENTITY_UNKNOWN')
 local n={version=1,start=t.start,age=t.age,cursor=t.cursor,state=t.state,receipt=t.receipt}
 if t.state=='OWNER_POLICY_UNRESOLVED' or t.state=='UNKNOWN_INTERVAL' then return n end
 local delta=turn-t.cursor
 if delta>1 then n.state='UNKNOWN_INTERVAL';return n end
 if t.state=='COUNTING' then n.age=n.age+delta end
 n.cursor=turn;n.state=identity=='RESEARCH' and 'COUNTING' or 'PAUSED_IDENTITY'
 return n
end
function M.Shadow(age,multiplier)
 assert(integer(age) and type(multiplier)=='number' and multiplier>0 and multiplier<math.huge,'TRADITION_SPEED_UNKNOWN')
 local tier=0;local nextAge
 for j=1,4 do local threshold=math.floor(10*j*multiplier)
  if age>=threshold then tier=j elseif not nextAge then nextAge=threshold end
 end
 return 5*(1+tier),nextAge
end
function M.Start(P,shared)
 local data={};shared.ResearchTradition=data
 local store=assert(shared.CityProgressionStore)
 function data.Describe(pid,c)
  local ok,text=pcall(function()
   local t=store.ReadTradition(pid,c)
   local f=shared.EffectiveFacts.Read(pid,c)
   if not t then return '学术传统｜影子计算（未施加科技收益）\n'..
    (f.specialization=='RESEARCH' and f.potential==4 and '首次P4起点不可确认；不猜测补龄。测试需从P3投资开始。' or '尚未在本版本首次达到科研潜力4。') end
   local speed=GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()]
   local bonus,nextAge=M.Shadow(t.age,assert(speed and speed.CostMultiplier,'TRADITION_SPEED_UNKNOWN')/100)
   local reason={COUNTING='累计中',PAUSED_IDENTITY='转出科研，暂停',OWNER_POLICY_UNRESOLVED='跨Owner归属待定，保留但暂停',UNKNOWN_INTERVAL='计龄区间不可确认，保留但暂停'}
   local gate=f.activeStatus=='KNOWN' and f.specialization=='RESEARCH' and f.active>=4
   return table.concat({'学术传统｜影子计算（未施加科技收益）',
    '首次P4：T'..t.start..'｜已累计 '..t.age..' 回合｜'..reason[t.state],
    '当前潜力 '..f.potential..' / ACTIVE '..tostring(f.active),
    '按年龄预期：+'..bonus..'% 科技｜'..(gate and '当前满足四级门槛' or '当前未满足四级门槛或资格未知'),
    nextAge and ('下一阶段：累计 '..nextAge..' 回合（还需 '..(nextAge-t.age)..'）') or '已达25%上限',
    '仅报告；实际收益尚未接入。'..(t.cursor~=Game.GetCurrentGameTurn() and ' 最近可靠结算T'..t.cursor..'。' or '')},'\n')
  end)
  if ok then return text end
  return '学术传统：当前事实暂不可确认；未补算、未发放收益。\n'..(tostring(text):match('[A-Z][A-Z_]+') or 'UNKNOWN')
 end
end
