from pathlib import Path
p=Path(__file__).with_name('test_unit_site_probe.py')
t=p.read_text().replace("ContextPtr={SetUpdate=function(_,fn) update=fn end}","Events={LoadScreenClose={Add=function(fn) load=fn end,Remove=function() end}}\nContextPtr={SetUpdate=function(_,fn) update=fn end,SetInitHandler=function(_,fn) init=fn end,SetShutdown=function() end,SetHide=function(_,v) hidden=v end}")
t=t.replace("assert(not Controls.ReadButton.hidden);Controls.ReadButton.click()", "init();load();assert(hidden==false);assert(not Controls.ReadButton.hidden);Controls.ReadButton.click()")
t=t.replace("assert(Controls.ReadButton.hidden)","assert(not Controls.ReadButton.hidden);Controls.ReadButton.click();assert(Controls.Report.text:find('Select an owned'))")
t=t.replace("=='51'","=='52'").replace('manifest51','manifest52')
exec(compile(t,str(p),'exec'),{'__file__':str(p.resolve())})
