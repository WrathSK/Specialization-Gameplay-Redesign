from pathlib import Path
import hashlib,xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
b=w/'DevelopmentBackups/Specialization-before-B045-crew-ux/RuntimeSnapshot'
# Prove protected mechanics remain byte-identical, including the complete executor function.
for n in ['Data/Crew.sql','Data/CrewProjects.sql','CrewProjects.lua','ConstructionProbe.lua','UnitTargets.lua','InvestmentAction.lua']:
 assert (r/n).read_bytes()==(b/n).read_bytes(),n
assert (r/'UnitActions.lua').read_text().split(' function data.Run(pid,p)',1)[1]==(b/'UnitActions.lua').read_text().split(' function data.Run(pid,p)',1)[1]
assert (r/'Probe.lua').read_text().replace('P0-B-045','P0-B-044')==(b/'Probe.lua').read_text()
# Previous numerical, SQL, consumption and investment tests, with new build fixture and UI suite replaced below.
p=w/'DevelopmentTests/test_crew_projects.py';t=p.read_text();start=t.index('# UI regression');end=t.index('# Actual catalog');t=t[:start]+t[end:];t=t.replace("=='57'","=='58'")
t=t.replace("m.executescript((r/'Data/CrewProjects.sql').read_text())", "\n".join([
 "m.execute(\"delete from Types where Type like 'PROJECT_SPC_CREW_%' or Type='BUILDING_SPC_CREW_PROJECT_ACCESS'\")",
 "m.execute(\"delete from Buildings where BuildingType='BUILDING_SPC_CREW_PROJECT_ACCESS'\")",
 "m.execute(\"delete from Projects where ProjectType like 'PROJECT_SPC_CREW_%'\")",
 "m.execute(\"delete from ProjectCompletionModifiers where ProjectType like 'PROJECT_SPC_CREW_%'\")",
 "m.execute(\"delete from Modifiers where ModifierId like 'SPC_PROJECT_GRANT_CREW_%'\")",
 "m.execute(\"delete from ModifierArguments where ModifierId like 'SPC_PROJECT_GRANT_CREW_%'\")",
 "m.executescript((r/'Data/CrewProjects.sql').read_text())"]))
exec(compile(t,str(p),'exec'),{'__file__':str(p)})
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((r/'Probe.lua').read_text())
l.execute('''
P=SPCP0;P.IsTestPlayer=function() return true end
P.Info=function(t,k) if t=='Units' then return {UnitType='UNIT_SPC_CREW_250'} else return {Name='目标建筑'} end end
GameConfiguration={GetGameSpeedType=function() return 0 end}
GameInfo={GameSpeeds={[0]={CostMultiplier=100}},Units={[1]={UnitType='UNIT_SPC_CREW_250'}}}
turn=1;cost=1800;progress=1700;current='BUILDING_TEST';kills=0;grants=0;props={};uProps={};x=10
u={GetOwner=function() return 0 end,GetID=function() return 1 end,GetType=function() return 1 end,
 GetX=function() return x end,GetY=function() return 0 end,GetBuildCharges=function() return 1 end,
 GetProperty=function(_,k) return uProps[k] end,SetProperty=function(_,k,v) uProps[k]=v end}
c={GetOwner=function() return 0 end,GetID=function() return 8 end,GetBuildQueue=function() return {AddProgress=function(_,n) grants=grants+1;progress=progress+n end} end}
Players={[0]={GetUnits=function() return {FindID=function() return u end,Destroy=function() kills=kills+1;u=nil end} end,
 GetCities=function() return {FindID=function() return c end} end,GetProperty=function(_,k) return props[k] end,SetProperty=function(_,k,v) props[k]=v end}}
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return turn end}
Map={GetPlot=function(a,b) return {GetIndex=function() return a end} end}
shared={Version=P.VERSION,UnitTargetSnapshot={token='KEEP'},UnitTargets={Refresh=function() shared.UnitTargetSnapshot={plots={{plot=10,cityID=8}}} end},
ConstructionProbe={ReadSnapshot=function() return {target=current,kind='Buildings',cost=cost,progress=progress} end}}
ExposedMembers={SPC_P0=shared};Events={};include=function() end
Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1};InterfaceModeTypes={SELECTION=1};Locale={Lookup=function(n) return n end}
parent={CalculateSize=function() end,ReprocessAnchoring=function() end}
Controls=setmetatable({},{__index=function(t,k) local c={SetHide=function(self,v) self.hide=v end,
 SetDisabled=function(self,v) self.disabled=v end,SetIcon=function(self,v) self.icon=v end,
 SetToolTipString=function(self,v) self.tip=v end,ChangeParent=function(self,p) self.parent=p end,
 SetSizeX=function(self,v) self.width=v end,SetOffsetX=function(self,v) self.offset=v end,
 RegisterCallback=function(self,_,f) self.click=f end};t[k]=c;return c end})
ContextPtr={SetInitHandler=function(_,f) init=f end,SetUpdate=function(_,f) tick=f end,
 SetHide=function() end,SetShutdown=function() end,LookUpControl=function() return parent end}
requests=0;actionRequests=0
UI={GetHeadSelectedUnit=function() return u end,GetInterfaceMode=function() return 1 end,
RequestPlayerOperation=function(pid,_,p)
 requests=requests+1
 if p.Action=='UNIT_ACTION_VIEW' then shared.UnitActions.ReadView(pid,p.UnitID,p.Token)
 else actionRequests=actionRequests+1;shared.Snapshot=shared.UnitActions.Run(pid,p);shared.LastToken=p.Token end
end}
''')
l.execute((r/'UnitActions.lua').read_text());l.execute('SPCUnitActions.Start(P,shared)')
l.execute((r/'UI/UnitPanelActions.lua').read_text())
l.execute('''
init();tick(0.3);tick(0.3)
assert(shared.UnitTargetSnapshot.token=='KEEP')
assert(Controls.PrepareButton.tip:find('准备在当前建造项目上投入250',1,true))
local right=1000;local before=right-Controls.ActionGroup.width+Controls.PrepareButton.offset
Controls.PrepareButton.click();Controls.PrepareButton.click();assert(actionRequests==1 and kills==0 and grants==0)
tick(0.3);tick(0.3)
assert(not Controls.ConfirmButton.hide)
local after=right-Controls.ActionGroup.width+Controls.PrepareButton.offset
local confirm=right-Controls.ActionGroup.width+Controls.ConfirmButton.offset
assert(before==after and confirm+44<after)
local tip=Controls.PrepareButton.tip
assert(tip:find('施工预览',1,true) and tip:find('当前目标：目标建筑',1,true))
assert(tip:find('本次投入：250点生产力',1,true) and tip:find('施工后：1800 / 1800',1,true) and tip:find('浪费：150点生产力',1,true))
assert(not tip:find('已准备',1,true));assert(not Controls.ConfirmButton.tip:find('当前进度',1,true))
local count=actionRequests;Controls.PrepareButton.click();Controls.PrepareButton.click();assert(actionRequests==count and grants==0)
-- New target invalidates the old preparation using unchanged existing fresh checks.
current='BUILDING_OTHER';tick(0.6);tick(0.3);assert(Controls.ConfirmButton.hide and shared.UnitActionPreview==nil)
Controls.ConfirmButton.click();assert(actionRequests==count)
Controls.PrepareButton.click();tick(0.3);tick(0.3);assert(not Controls.ConfirmButton.hide)
x=11;tick(0.6);tick(0.3);assert(Controls.ConfirmButton.hide)
assert(Controls.PrepareButton.tip:find('将施工队移动',1,true));Controls.PrepareButton.click();assert(kills==0 and grants==0)
x=10;tick(0.6);tick(0.3);Controls.PrepareButton.click();tick(0.3);tick(0.3)
progress=cost;tick(0.6);tick(0.3);assert(Controls.ConfirmButton.hide and not shared.UnitActionView.legal)
assert(kills==0 and grants==0 and next(props)==nil and next(uProps)==nil)
-- Current valid plan still executes the unchanged capped settlement.
progress=1700;tick(0.6);tick(0.3);Controls.PrepareButton.click();tick(0.3);tick(0.3)
Controls.ConfirmButton.click();assert(kills==1 and grants==1 and progress==1800)
''')
x=E.parse(r/'UI/UnitPanelActions.xml').getroot().find('Grid');assert x.get('Size')=='90,53'
assert x.find("Button[@ID='PrepareButton']").get('Offset')=='46,0'
assert x.find("Button[@ID='ConfirmButton']").get('Offset')=='0,0'
print('LOCAL_SIMULATION_PASS B045: protected mechanics byte-identical; fixed slots/no overlap; quick double click and repeated preview inert; target/move/completion invalidation; short Chinese tooltips; actual unchanged capped executor. Actual native panel pixels require user check.')

# Verify effective localized names/descriptions after executing all repeated historical text rows.
import sqlite3
db=sqlite3.connect(':memory:');db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))')
db.executescript((r/'Text/TestText.sql').read_text())
for level,amount in zip('一二三四五',[250,420,750,1000,1360]):
 for lang in ['zh_Hans_CN','en_US']:
  def value(tag): return db.execute('select Text from LocalizedText where Language=? and Tag=?',(lang,tag)).fetchone()[0]
  assert value(f'LOC_UNIT_SPC_CREW_{amount}_NAME')==level+'级施工队'
  assert value(f'LOC_PROJECT_SPC_CREW_{amount}_NAME')=='组建'+level+'级施工队'
  desc=value(f'LOC_UNIT_SPC_CREW_{amount}_DESCRIPTION')
  assert desc==f'施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• {level}级施工队可提供{amount}点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。'
print('LOCAL_SIMULATION_PASS B045 localization: all five names and exact unit descriptions in both registered languages.')
