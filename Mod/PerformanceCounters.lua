-- B069: fixed schema, scalar counters only. No automatic disk/print sink.
SPCPerformance={}
local M=SPCPerformance
local names={'unit_cb','unit_ignored','revalidate','route_scan','publication','same_snapshot','derive','facts','city_scan','district_scan','building_check','building_create','building_remove','property_write','net_send','net_receive','audit_lv3','audit_boost','audit_standard','audit_commerce','audit_copy','busy_skip','send_duplicate','send_inflight','send_timeout','route_failure','confirmed_invalid','manual_snapshot','fact_change','input_duplicate','input_publication','withdrawal','revalidate_same','stale_input','derive_requested','derive_executed','derived_cache_hit','derived_cache_miss','input_version_change','derived_invalidation','discount_attempt','discount_send','discount_pending','discount_ack','discount_retry','discount_timeout','discount_receive','discount_duplicate','discount_stale','discount_apply','discount_withdraw','discount_dirty_mark','discount_direct_refresh','discount_reconcile','discount_skipped_clean','discount_fact_capture','discount_city_processed','discount_ui_scan'}
for _,k in ipairs({'copy','industry'}) do
 for _,n in ipairs({'attempt','send','receive','pending','retry','stale','apply','withdraw','duplicate','timeout'}) do names[#names+1]=k..'_'..n end
end
function M.New()
 local s={schema=1,turn=Game.GetCurrentGameTurn(),startTurn=Game.GetCurrentGameTurn(),entries={},inflight=0,peakInflight=0,revision=0,routes=0,enabled=true}
 for _,n in ipairs(names) do s.entries[n]={current=0,total=0,previous=0,peak=0} end
 return s
end
function M.Count(n,amount)
 local s=ExposedMembers and ExposedMembers.SPC_Performance
 if not s or not s.enabled then return end
 local e=s.entries[n];if not e then return end
 local t=Game.GetCurrentGameTurn()
 if t~=s.turn then
  for _,v in pairs(s.entries) do v.previous=v.current;v.peak=math.max(v.peak,v.current);v.current=0 end
  s.turn=t
 end
 amount=amount or 1;e.current=e.current+amount;e.total=e.total+amount
end
function M.Flight(n)
 local s=ExposedMembers and ExposedMembers.SPC_Performance
 if s then s.inflight=n;s.peakInflight=math.max(s.peakInflight,n) end
end
function M.Describe(detailed)
 M.Count('manual_snapshot',0)
 local s=ExposedMembers and ExposedMembers.SPC_Performance
 if not s then return 'Performance counters not initialized' end
 local lines={'B069 performance | turn='..s.turn..' | start='..s.startTurn,
  'Current / Total (direct Lua engine calls; native Modifier Property writes not observable)',
  'revision='..s.revision..' routes='..s.routes..' inflight='..s.inflight..' peak='..s.peakInflight}
 local groups={{'unit_cb','unit_ignored'},{'revalidate','route_scan'},{'publication','same_snapshot'},
 {'derive','facts'},{'city_scan','district_scan'},{'building_check','building_create','building_remove'},
 {'property_write','net_send','net_receive'},{'audit_lv3','audit_boost','audit_standard'},
 {'audit_commerce','audit_copy'},{'busy_skip','send_duplicate','send_inflight','send_timeout'},
 {'route_failure','confirmed_invalid'},{'fact_change','input_duplicate','input_publication'},{'withdrawal','revalidate_same','stale_input'},{'derive_requested','derive_executed'},{'derived_cache_hit','derived_cache_miss'},{'input_version_change','derived_invalidation'},{'discount_attempt','discount_send','discount_pending'},{'discount_ack','discount_retry','discount_timeout'},{'discount_receive','discount_duplicate','discount_stale'},{'discount_apply','discount_withdraw'},{'discount_dirty_mark','discount_direct_refresh','discount_reconcile'},{'discount_skipped_clean','discount_fact_capture','discount_city_processed','discount_ui_scan'}}
 for _,k in ipairs({'copy','industry'}) do
  groups[#groups+1]={k..'_attempt',k..'_send',k..'_receive',k..'_pending'}
  groups[#groups+1]={k..'_retry',k..'_stale',k..'_apply',k..'_withdraw',k..'_duplicate',k..'_timeout'}
 end
 for _,g in ipairs(groups) do local a={};for _,n in ipairs(g) do local e=s.entries[n];a[#a+1]=n..'='..e.current..'/'..e.total end;lines[#lines+1]=table.concat(a,'  ') end
 local audit=ExposedMembers.SPC_RuntimeAudit
 lines[#lines+1]='Runtime audit='..(audit and audit.state or 'NOT_INITIALIZED')..' | '..(audit and audit.reason or '')
 if audit and audit.sink then lines[#lines+1]='Audit file='..audit.sink.path..' | rows='..tostring(audit.rows) end
 if detailed then
  lines[#lines+1]='schema=1; auto_log='..(audit and audit.state=='ACTIVE' and 'ACTIVE' or 'DISABLED')..'; format=TSV; retention=8 x 4MiB'
  for _,n in ipairs(names) do local e=s.entries[n];lines[#lines+1]=n..' previous='..e.previous..' peak='..math.max(e.peak,e.current) end
 end
 return table.concat(lines,'\n')
end
