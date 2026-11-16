"""R19 presentation roles: native queued icon, candidate preview, current timer."""
from pathlib import Path
import unittest
from refactor_harness import ROOT,Context,measure
from test_refactor_s7d2 import ui_actual


def display(kind='Dialogue'):
 v=ui_actual(kind);v.globals().include('TimedProjectDisplay');return v


class Roles(unittest.TestCase):
 def test_localized_project_help_and_timer_are_read_only(self):
  for kind,key in (('Claim','CLAIM'),('Dialogue','DIALOGUE'),('Engineering','STUDY')):
   with self.subTest(kind=kind):
    display(kind).execute("""
    local kind=...
    local w=T.writes()
    projectTranslations['LOC_SPC_TIMED_PROJECT_'..kind..'_PREVIEW']='Localized preview'
    projectTranslations.LOC_SPC_TIMED_PROJECT_TIMER_ACTIVE='Timer started: one turn'
    projectTranslations.LOC_SPC_TIMED_PROJECT_TIMER_STATUS='Timer: {1}'
    local cityKey='0:'..c:GetID()
    local rows=shared[backendKey].views
    rows[cityKey]=nil
    local item={Type=project,IsCurrentProduction=false,ToolTip='Original'}
    SPCTimedProjectDisplay.Items({Owner=0,City=c,ProjectItems={item}})
    assert(item.TurnsLeft=='1'and item.Progress==0 and item.ToolTip=='Localized preview[NEWLINE]Original')
    local function control()return {
     SetText=function(self,text)self.text=text end,SetPercent=function()end,
     SetShadowPercent=function()end,SetToolTipString=function(self,note)self.note=note end
    }end
    local parent={CurrentProductionCost=control(),CurrentProductionProgressString=control(),
     CurrentProductionProgress=control(),ProductionIcon=control()}
    q.target=project
    rows[cityKey]={stage='ACTIVE',project=project,reason='Authoritative'}
    SPCTimedProjectDisplay.Current(parent,0,c:GetID())
    assert(parent.CurrentProductionProgressString.text=='Timer started: one turn')
    rows[cityKey]={stage='CALLING',project=project,reason='Authoritative'}
    SPCTimedProjectDisplay.Current(parent,0,c:GetID())
    assert(parent.CurrentProductionProgressString.text=='Timer: '..(kind=='CLAIM'and '已暂停'or '待确认'))
    assert(T.writes()==w and uiBegins==0)
    """,key)

 def test_noncurrent_candidate_never_borrows_running_or_held_timer_state(self):
  v=display();v.execute("""
  local views=shared.DialogueProjects.views;local key='0:'..c:GetID();local writes=T.writes()
  for _,stage in ipairs({'ACTIVE','CALLING','HELD'})do
   views[key]={stage=stage,reason='CURRENT_TIMER_ONLY'}
   local old=c.GetBuildQueue;c.GetBuildQueue=function()error('NONCURRENT_MUST_NOT_READ_QUEUE')end
   local item={Type=project,IsCurrentProduction=false,TurnsLeft=999,Progress=2,ToolTip='Original'}
   SPCTimedProjectDisplay.Items({Owner=0,City=c,ProjectItems={item}})
   assert(item.TurnsLeft=='1'and item.Progress==0 and item.ToolTip:find('Original',1,true)and not item.ToolTip:find('CURRENT_TIMER_ONLY',1,true))
   c.GetBuildQueue=old
  end
  assert(T.writes()==writes and uiBegins==0)
  """)
 def test_current_without_timer_is_explicitly_not_yet_timed(self):
  v=display();v.execute("q.target=project;shared.DialogueProjects.views['0:'..c:GetID()]=nil;local text,note=SPCDialogueProjectUI.Text(0,c:GetID());assert(text=='待计时'and note:find('独占生产队列',1,true)and note:find('未确认时不会完成',1,true));assert(not pending()and uiBegins==0)")
 def test_current_active_calling_held_labels_and_reasons_remain_exact(self):
  v=display();v.execute("q.target=project;for stage,label in pairs({ACTIVE='1',CALLING='待确认',HELD='已暂停'})do shared.DialogueProjects.views['0:'..c:GetID()]={stage=stage,reason='Authoritative'};local text,note=SPCDialogueProjectUI.Text(0,c:GetID());assert(text==label and note=='Authoritative')end")
 def test_real_queued_selection_cannot_start_or_rearm_from_display(self):
  v=display();v.execute("q.target='NORMAL';uiQueueSize=2;assert(not ui.Before(c,{Type=project},true));local w=T.writes();for i=1,100 do SPCTimedProjectDisplay.Items({Owner=0,City=c,ProjectItems={{Type=project,IsCurrentProduction=false}}});pumpUI()end;assert(uiBegins==0 and uiReads==0 and T.writes()==w)")
 def test_current_multiple_queue_wait_is_text_only_not_automatic_start(self):
  v=display();v.execute("q.target=project;uiQueueSize=2;assert(selectUI());pumpUI();assert(uiBegins==0);local text,note=SPCDialogueProjectUI.Text(0,c:GetID());assert(text=='待计时'and note:find('独占生产队列',1,true));uiQueueSize=1;idleUI(1000);assert(uiBegins==0)")
 def test_unrelated_item_and_current_flag_unknown_keep_existing_roles(self):
  v=display();v.execute("shared.DialogueProjects.views['0:'..c:GetID()]={stage='HELD',reason='HeldCurrent'};local item={Type=project,ToolTip='Original'};local other={Type='NORMAL',TurnsLeft=7,Progress=8,ToolTip='Other'};SPCTimedProjectDisplay.Items({Owner=0,City=c,ProjectItems={item,other}});assert(item.TurnsLeft=='已暂停'and item.ToolTip:find('HeldCurrent',1,true));assert(other.TurnsLeft==7 and other.Progress==8 and other.ToolTip=='Other')")
 def test_original_queue_cell_wrapper_preserves_native_args_returns_and_icon_only(self):
  v=Context('UI');v.execute("calls=0;LuaEvents={SPC_ClaimIconDecorate=function(icon,name)decorated=icon;texture=name end};instance={ProductionIcon={},iconTexture='ICON_PROJECT_SPC_ERA_DIALOGUE'};function CreateQueueInstance(...)calls=calls+1;args={...};return instance end")
  v.execute(v.fragment('Mod/UI/CrewProjectOrder.lua','local baseQueueInstance=CreateQueueInstance','local claimSelection,'))
  v.execute("local entry={Directive=7,ProjectType=12};assert(CreateQueueInstance('Manager','Parent',0,9,2,entry)==instance and calls==1 and #args==6 and args[6]==entry);assert(decorated==instance.ProductionIcon and texture=='ICON_PROJECT_SPC_ERA_DIALOGUE'and instance.TurnsLeft==nil)")
  measure('S9e10_presentation_roles',{'known_noncurrent_queue_reads':0,'automatic_begin_or_completion_added':False,'native_queue_cell':'existing icon-only wrapper unchanged','current_status_without_timer':'待计时','original_reported_location':'USER_GAME_TEST_REQUIRED'})

if __name__=='__main__':unittest.main()
