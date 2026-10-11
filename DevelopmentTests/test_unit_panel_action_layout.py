"""B195 current UnitPanelActions layout with actual crew executor and mocked native UI.
No legacy runtime snapshot or external database dependency; pixels remain a native check.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'Mod'


def panel():
    l=LuaRuntime(unpack_returned_tuples=True)
    l.execute('include=function()end')
    l.execute((MOD/'PerformanceCounters.lua').read_text())
    l.execute((MOD/'Probe.lua').read_text())
    l.execute(r'''
      print=function()end;include=function()end;P=SPCP0
      P.IsTestPlayer=function(pid)return pid==0 end
      P.Info=function(t,k)
       if t=='Units'then return GameInfo.Units[k] end
       return {Name='目标建筑'}
      end
      GameConfiguration={GetGameSpeedType=function()return 0 end}
      GameInfo={GameSpeeds={[0]={CostMultiplier=100}},Units={
       [1]={UnitType='UNIT_SPC_CREW_250'},[2]={UnitType='UNIT_SETTLER'},[3]={UnitType='UNIT_WARRIOR'}}}
      turn=1;cost=1800;progress=1700;target='BUILDING_TEST';kills=0;grants=0;props={};requests={}
      function makeUnit(id,kind,owner)
       local u={id=id,kind=kind or 1,owner=owner or 0,x=10,y=0,props={}}
       function u:GetOwner()return self.owner end;function u:GetID()return self.id end
       function u:GetType()return self.kind end;function u:GetX()return self.x end;function u:GetY()return self.y end
       function u:GetBuildCharges()return 1 end;function u:GetProperty(k)return self.props[k]end
       function u:SetProperty(k,v)self.props[k]=v end
       return u
      end
      units={[1]=makeUnit(1),[2]=makeUnit(2),[3]=makeUnit(3,2),[4]=makeUnit(4,3),[5]=makeUnit(5,1,1)}
      selected=units[1]
      city={GetOwner=function()return 0 end,GetID=function()return 8 end,
       GetBuildQueue=function()return {AddProgress=function(_,n)grants=grants+1;progress=progress+n end}end}
      local district={GetCity=function()return city end,GetX=function()return 10 end,GetY=function()return 0 end}
      Players={[0]={GetUnits=function()return {
       FindID=function(_,id)return units[id]end,
       Destroy=function(_,u)kills=kills+1;units[u.id]=nil;if selected==u then selected=nil end end}end,
       GetCities=function()return {FindID=function(_,id)return id==8 and city or nil end}end,
       GetDistricts=function()return {Members=function()return pairs({district})end}end,
       GetProperty=function(_,k)return props[k]end,SetProperty=function(_,k,v)props[k]=v end}}
      Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return turn end}
      Map={GetPlot=function(x,y)return {GetIndex=function()return x end}end}
      shared={Version=P.VERSION,UnitTargetSnapshot={token='KEEP'},
       UnitTargets={Refresh=function()shared.UnitTargetSnapshot={plots={{plot=10,cityID=8}}}end},
       ConstructionProbe={ReadSnapshot=function()return {target=target,kind='Buildings',cost=cost,progress=progress}end}}
      -- Investment is an unchanged business dependency; this fixture exercises only
      -- its structured UI contract, while crew preparation/consumption runs actual code.
      local investment
      shared.InvestmentAction={
       ReadView=function(pid,c,id)return {legal=true,prepared=investment~=nil and investment.unitID==id,
        planToken=investment and investment.token,specialization='RESEARCH',potential=1,nextPotential=2}end,
       Prepare=function(pid,c,id,token)
        investment={owner=pid,unitID=id,token=token};shared.InvestmentPreview=investment;return 'prepared'
       end,
       Confirm=function(pid,c,token)assert(investment and investment.token==token);investment=nil;return 'confirmed' end,
       CancelPreview=function()investment=nil end}
      ExposedMembers={SPC_P0=shared}
      function event()local e={listeners={}};function e.Add(f)e.listeners[f]=true end;function e.Remove(f)e.listeners[f]=nil end
       return setmetatable(e,{__call=function(self,...)for f in pairs(self.listeners)do f(...)end end})end
      Events={CityProductionChanged=event(),InterfaceModeChanged=event(),UnitRemovedFromMap=event()}
      Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1};InterfaceModeTypes={SELECTION=1};mode=1
      Locale={Lookup=function(s)return s end}
      parent={CalculateSize=function()end,ReprocessAnchoring=function()end}
      Controls=setmetatable({},{__index=function(t,k)
       local c={SetHide=function(self,v)self.hide=v end,SetDisabled=function(self,v)self.disabled=v end,
        SetIcon=function(self,v)self.icon=v end,SetToolTipString=function(self,v)self.tip=v end,
        ChangeParent=function(self,p)self.parent=p end,SetSizeX=function(self,v)self.width=v end,
        SetOffsetX=function(self,v)self.offset=v end,RegisterCallback=function(self,_,f)self.click=f end}
       t[k]=c;return c
      end})
      ContextPtr={SetInitHandler=function(_,f)init=f end,SetUpdate=function(_,f)tick=f end,
       ClearUpdate=function()tick=nil end,SetHide=function()end,SetShutdown=function(_,f)shutdown=f end,
       LookUpControl=function(_,path)assert(path=='/InGame/UnitPanel/StandardActionsStack');return parent end}
      UI={GetHeadSelectedUnit=function()return selected end,GetInterfaceMode=function()return mode end,
       RequestPlayerOperation=function(pid,op,p)
        assert(pid==0 and op==1 and p.OnStart=='SPC_P0_Request');requests[#requests+1]=p
        if p.Action=='UNIT_ACTION_VIEW'then shared.UnitActions.ReadView(pid,p.UnitID,p.Token)
        else shared.Snapshot=shared.UnitActions.Run(pid,p);shared.LastToken=p.Token end
       end}
      function refresh()tick(.3);tick(.3)end
      function actions(kind)local n=0;for _,p in ipairs(requests)do if p.Action==kind then n=n+1 end end;return n end
      function prepare()Controls.PrepareButton.click();refresh()end
    ''')
    l.execute((MOD/'UnitActions.lua').read_text())
    l.execute('SPCUnitActions.Start(P,shared)')
    l.execute((MOD/'UI/UnitPanelActions.lua').read_text())
    l.execute('init();refresh()')
    return l


class UnitPanelActionLayout(unittest.TestCase):
    def test_idle_uses_one_slot_prepared_uses_two_without_moving_prepare(self):
        l=panel()
        l.execute('''
         assert(not Controls.ActionGroup.hide and Controls.ActionGroup.width==44 and Controls.ActionSlot.width==47)
         assert(Controls.PrepareButton.offset==0 and Controls.ConfirmButton.hide)
         assert(Controls.ActionGroup.parent==parent and shared.UnitTargetSnapshot.token=='KEEP')
         local right=1000;local before=right-Controls.ActionGroup.width+Controls.PrepareButton.offset
         prepare()
         assert(Controls.ActionGroup.width==90 and Controls.ActionSlot.width==93 and Controls.PrepareButton.offset==46 and Controls.ConfirmButton.offset==0)
         assert(not Controls.ConfirmButton.hide)
         local after=right-Controls.ActionGroup.width+Controls.PrepareButton.offset
         local confirm=right-Controls.ActionGroup.width+Controls.ConfirmButton.offset
         assert(before==after and confirm+44<after)
         assert(kills==0 and grants==0 and next(props)==nil)
        ''')

    def test_double_and_repeated_prepare_are_inert_until_exact_confirm(self):
        l=panel()
        l.execute('''
         Controls.PrepareButton.click();Controls.PrepareButton.click()
         assert(actions('UNIT_ACTION_PREPARE')==1 and kills==0 and grants==0)
         refresh();local plan=shared.UnitActionPreview.token
         Controls.PrepareButton.click();Controls.PrepareButton.click();refresh()
         assert(actions('UNIT_ACTION_PREPARE')==1 and shared.UnitActionPreview.token==plan and kills==0 and grants==0)
         Controls.ConfirmButton.click();Controls.ConfirmButton.click()
         assert(actions('UNIT_ACTION_CONFIRM')==1 and kills==1 and grants==1 and progress==1800)
         refresh();assert(Controls.ActionGroup.hide and units[2]~=nil)
        ''')

    def test_mismatched_plan_token_hides_confirmation_and_never_consumes(self):
        l=panel()
        l.execute('''
         prepare();shared.UnitActionPreview.token='different-plan';refresh()
         assert(Controls.ConfirmButton.hide and Controls.ActionGroup.width==44 and Controls.ActionSlot.width==47 and Controls.PrepareButton.offset==0)
         Controls.ConfirmButton.click()
         assert(actions('UNIT_ACTION_CONFIRM')==0 and kills==0 and grants==0)
        ''')

    def test_changed_target_invalidates_preview_and_collapses_without_business_effect(self):
        l=panel()
        l.execute('''
         prepare();target='BUILDING_OTHER';Events.CityProductionChanged();refresh()
         assert(Controls.ConfirmButton.hide and Controls.ActionGroup.width==44 and Controls.ActionSlot.width==47 and Controls.PrepareButton.offset==0)
         assert(shared.UnitActionPreview==nil);Controls.ConfirmButton.click()
         assert(actions('UNIT_ACTION_CONFIRM')==0 and kills==0 and grants==0 and next(props)==nil)
        ''')

    def test_changed_unit_selection_or_position_does_not_reuse_confirmation(self):
        for change in ['selected=units[2]', 'selected.x=11', 'turn=2']:
            with self.subTest(change=change):
                l=panel()
                l.execute('prepare();'+change+''';refresh()
                 assert(Controls.ConfirmButton.hide and Controls.ActionGroup.width==44 and Controls.ActionSlot.width==47 and Controls.PrepareButton.offset==0)
                 Controls.ConfirmButton.click();assert(actions('UNIT_ACTION_CONFIRM')==0 and kills==0 and grants==0)
                ''')

    def test_other_units_foreign_owner_no_selection_and_other_mode_hide_group(self):
        for change in ['selected=units[4]', 'selected=units[5]', 'selected=nil', 'mode=2']:
            with self.subTest(change=change):
                l=panel()
                l.execute('prepare();'+change+''';refresh();assert(Controls.ActionGroup.hide)
                 confirms=actions('UNIT_ACTION_CONFIRM')
                ''')
                if change!='mode=2':
                    l.execute("Controls.ConfirmButton.click();assert(actions('UNIT_ACTION_CONFIRM')==confirms and kills==0 and grants==0)")

    def test_settler_branch_uses_same_slot_geometry_and_native_found_city_icon(self):
        l=panel()
        l.execute('''
         selected=units[3];refresh()
         assert(Controls.ActionGroup.width==44 and Controls.PrepareButton.offset==0 and Controls.ConfirmButton.hide)
         assert(Controls.PrepareIcon.icon=='ICON_UNITOPERATION_FOUND_CITY')
         prepare();assert(Controls.ActionGroup.width==90 and Controls.PrepareButton.offset==46 and not Controls.ConfirmButton.hide)
         assert(Controls.PrepareButton.tip:find('投资预览',1,true) and Controls.ConfirmButton.tip:find('确认投资',1,true))
         assert(kills==0 and grants==0)
        ''')

    def test_crew_native_icon_and_localized_preview_remain_readable(self):
        l=panel()
        l.execute('''
         assert(Controls.PrepareIcon.icon=='ICON_UNITOPERATION_BUILD_IMPROVEMENT')
         assert(Controls.PrepareButton.tip:find('准备在当前建造项目上投入250',1,true))
         prepare();assert(Controls.PrepareButton.tip:find('当前目标：目标建筑',1,true))
         assert(Controls.PrepareButton.tip:find('浪费：150点生产力',1,true))
         assert(not Controls.ConfirmButton.tip:find('当前进度',1,true))
        ''')


class NativeSlotStructure(unittest.TestCase):
    def test_existing_native_backing_is_decorative_and_buttons_keep_44_pixel_hitboxes(self):
        group=ET.parse(MOD/'UI/UnitPanelActions.xml').getroot().find("Grid[@ID='ActionGroup']")
        self.assertEqual(group.get('Size'),'44,53')
        slot=group.find("Grid[@ID='ActionSlot']")
        self.assertIsNotNone(slot)
        self.assertIs(list(group)[0],slot)
        self.assertEqual(slot.get('Texture'),'UnitPanel_ActionGroupSlot')
        self.assertEqual(slot.get('Size'),'47,41')
        self.assertEqual(slot.get('Anchor'),'C,B')
        self.assertEqual(slot.get('Offset'),'1,2')
        self.assertEqual(slot.get('SliceCorner'),'5,19')
        self.assertEqual(slot.get('SliceSize'),'1,1')
        glow=slot.find("Image[@Texture='UnitPanel_ActionGroupGlow']")
        self.assertIsNotNone(glow)
        self.assertEqual(glow.get('Anchor'),'C,B')
        self.assertEqual(len(group.findall('.//Button')),2)
        prepare=group.find("Button[@ID='PrepareButton']")
        confirm=group.find("Button[@ID='ConfirmButton']")
        for button in [prepare,confirm]:
            self.assertEqual(button.get('Size'),'44,53')
            self.assertEqual(button.get('Texture'),'UnitPanel_ActionButton')
            self.assertEqual(button.get('Offset'),'0,0')
        self.assertEqual(confirm.get('Hidden'),'1')


if __name__=='__main__':
    unittest.main()
