-- B072: bounded turn summaries; no Gameplay calls, listeners, or per-event work here.
SPCRuntimeAudit={}
local M=SPCRuntimeAudit
M.Schema=1
M.MaxBytes=4*1024*1024
M.Slots=8
local function cell(v) return tostring(v==nil and 'NA' or v):gsub('[\t\r\n]',' '):sub(1,160) end
-- Restricted stdio capability. Only these nine prefixed files may be touched.
-- No print fallback, shell, directory creation, database, or save Property sink.
function M.FileSink(lib,dir)
 assert(type(lib)=='table' and type(lib.open)=='function','FILE_API_UNAVAILABLE')
 assert(type(dir)=='string' and #dir<1024 and dir:sub(1,1)=='/','LOG_DIRECTORY_UNAVAILABLE')
 local s={serial=0,bytes=0,path='',writes=0}
 local index=dir..'/SpecializationRuntimeAudit.index'
 local f=lib.open(index,'rb')
 if f then local v=f:read(32);f:close();assert(v and v:match('^%d+\n?$'),'INVALID_LOG_INDEX');s.serial=assert(tonumber(v));assert(s.serial<1e12,'LOG_INDEX_LIMIT') end
 function s.Rotate(header)
  s.serial=s.serial+1
  local n=(s.serial-1)%M.Slots+1
  -- Advance index before replacing a bounded slot; a failed session is never retried.
  local i=assert(lib.open(index,'wb'),'INDEX_OPEN_FAILED')
  local ok=i:write(tostring(s.serial)..'\n');local closed=i:close();assert(ok and closed,'INDEX_WRITE_FAILED')
  s.path=dir..'/SpecializationRuntimeAudit-'..string.format('%02d',n)..'.tsv'
  local h=header(s.serial)
  local out=assert(lib.open(s.path,'wb'),'LOG_OPEN_FAILED')
  local wrote=out:write(h);local done=out:close();assert(wrote and done,'LOG_HEADER_FAILED')
  s.bytes=#h;s.writes=s.writes+1
 end
 function s.Append(text,header)
  assert(#text<16384,'SUMMARY_TOO_LARGE')
  if s.bytes+#text>M.MaxBytes then s.Rotate(header) end
  local out=assert(lib.open(s.path,'ab'),'LOG_APPEND_FAILED')
  local ok=out:write(text);local done=out:close();assert(ok and done,'LOG_WRITE_FAILED')
  s.bytes=s.bytes+#text;s.writes=s.writes+1
 end
 return s
end
local meta={'session','build','modinfo','turn','interval_from_turn','partial','elapsed_seconds','player','cities','routes','input_revision','derived_revision','network_validity','inflight','session_peak_inflight','network_players_proxy','network_inputs_proxy','diagnostic_entries_proxy','anomalies'}
function M.New(counters,sink,options)
 local s={state='STARTING',reason='',previous={},names={},lastTurn=nil,startTurn=options.turn,session=nil,rows=0,anomalies=0,peak={},sink=sink}
 for k,e in pairs(counters.entries) do
  assert(#s.names<64 and type(e.total)=='number','COUNTER_SCHEMA_UNSUPPORTED')
  s.names[#s.names+1]=k;s.previous[k]=0;s.peak[k]=0
 end
 table.sort(s.names)
 local function header(serial)
  if not s.session then s.session=tostring(serial)..'-'..cell(options.start or 'clock-unavailable') end
  local cols={};for _,k in ipairs(meta) do cols[#cols+1]=k end
  for _,k in ipairs(s.names) do cols[#cols+1]=k..'_interval';cols[#cols+1]=k..'_total';cols[#cols+1]=k..'_peak_interval' end
  return '# SPC_RUNTIME_AUDIT schema=1 session='..s.session..' build='..options.build..' modinfo='..options.modinfo..' source_base='..cell(options.sourceBase)..' start='..cell(options.start)..' start_turn='..cell(options.turn)..' segment='..serial..'\n'..table.concat(cols,'\t')..'\n'
 end
 function s.Fail(reason) s.state='DISABLED';s.reason=cell(reason) end
 local ok,err=pcall(sink.Rotate,header)
 if not ok then s.Fail(err) else s.state='ACTIVE' end
 function s.EndTurn(turn,c,info)
  if s.state~='ACTIVE' or s.lastTurn==turn then return false end
  if s.lastTurn and turn<s.lastTurn then s.Fail('TURN_REWIND_NEW_SESSION_REQUIRED');return false end
  -- The interval is between local-player end-turn boundaries, including intervening AI work.
  -- Cumulative differences avoid losing AI work when engine turn counters roll over.
  local delta={};local flags={}
  for _,k in ipairs(s.names) do
   local e=c.entries[k];if not e or e.total<s.previous[k] then s.Fail('COUNTER_RESET_NEW_SESSION_REQUIRED');return false end
   delta[k]=e.total-s.previous[k]
  end
  local function flag(k,n) flags[#flags+1]=k..':'..tostring(n) end
  if (delta.derive_executed or 0)>128 then flag('DERIVE_HIGH',delta.derive_executed) end
  if (delta.derive_executed or 0)>32 and (delta.derived_cache_hit or 0)==0 then flag('NO_CACHE_HITS',delta.derive_executed) end
  local writes=(delta.building_create or 0)+(delta.building_remove or 0)
  if writes>256 then flag('BUILDING_WRITES_HIGH',writes) end
  if (c.inflight or 0)>1 then flag('INFLIGHT_HIGH',c.inflight) end
  if (delta.send_timeout or 0)>3 then flag('SEND_TIMEOUT_HIGH',delta.send_timeout) end
  if (delta.withdrawal or 0)>0 then flag('CONFIRMED_WITHDRAWAL_REVIEW',delta.withdrawal) end
  if (delta.route_failure or 0)>3 then flag('ROUTE_FAILURE_HIGH',delta.route_failure) end
  local vals={s.session,options.build,options.modinfo,turn,s.lastTurn or s.startTurn,s.lastTurn and 0 or 1,
   info.elapsed,info.player,info.cities,info.routes,info.inputRevision,info.derivedRevision,info.validity,
   c.inflight,c.peakInflight,info.networkPlayers,info.networkInputs,info.diagnosticEntries,table.concat(flags,',')}
  -- Explicit array indices: unknown metrics use 'NA', not holes that truncate ipairs.
  local row={};for i=1,#meta do row[i]=cell(vals[i]) end
  for _,k in ipairs(s.names) do
   s.peak[k]=math.max(s.peak[k],delta[k]);row[#row+1]=cell(delta[k]);row[#row+1]=cell(c.entries[k].total);row[#row+1]=cell(s.peak[k])
  end
  local text=table.concat(row,'\t')..'\n'
  local good,why=pcall(sink.Append,text,header)
  if not good then s.Fail(why);return false end
  for _,k in ipairs(s.names) do s.previous[k]=c.entries[k].total end
  s.lastTurn=turn;s.rows=s.rows+1;s.anomalies=s.anomalies+#flags
  return true
 end
 return s
end
