-- Isolated diagnostic probe (Owner policy 2026-11-25). It only reads the error
-- log that production fills through SPCSafeCallbacks.Record and prints new
-- entries for the FireTuner collector. Nothing in production refers to this
-- context; removing its modinfo entry and these two files changes no behaviour.
local PREFIX='[SPC][ERR] '
local lastLog,seen=nil,0
local function scan()
 local shared=ExposedMembers.SPC_P0
 local log=shared and shared.ErrorLog
 if log==nil then return end
 if log~=lastLog then lastLog=log;seen=0 end -- a new game or load starts a new log
 if log.seq==seen then return end
 for _,e in ipairs(log.entries)do
  if e.seq>seen then print(PREFIX..'seq='..e.seq..' label='..e.label..' '..e.text)end
 end
 seen=log.seq
end
Events.LocalPlayerTurnBegin.Add(scan)
Events.LocalPlayerTurnEnd.Add(scan)
Events.GameCoreEventPublishComplete.Add(scan)
