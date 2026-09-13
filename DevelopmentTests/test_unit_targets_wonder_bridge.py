from pathlib import Path
p=Path(__file__).with_name('test_unit_targets.py')
t=p.read_text().replace("Map.GetCityPlots=function() return {GetPurchasedPlots=function() return {10} end} end",
"Map.GetCityPlots=nil;ExposedMembers={DLHD={Utils={GetCityPlots=function(pid,cid) assert(pid==0 and cid==8);return {10,10} end}}}")
t=t.replace("mark=6;assert", "ExposedMembers.DLHD.Utils.GetCityPlots=nil;assert(read(true).unknown[1].reason:find('HD_CITY_PLOTS_HELPER_UNAVAILABLE'));ExposedMembers.DLHD.Utils.GetCityPlots=function() return {10} end;mark=6;assert")
t=t.replace("=='53'","=='54'").replace('manifest53','manifest54')
exec(compile(t,str(p),'exec'),{'__file__':str(p.resolve())})
