"""B236 UI adapter: native request ordering, real queue reader and event publication."""
import unittest
from pathlib import Path
from lupa import LuaRuntime
R=Path(__file__).resolve().parents[1]
M=R/'Mod'
SETUP=r'''
include=function()end
P={VERSION='B236',IsTestPlayer=function(pid)return pid==0 end}
Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return turn end};turn=1
GameConfiguration={GetGameSpeedType=function()return 'STANDARD'end}
GameInfo={GameSpeeds={STANDARD={CostMultiplier=100}},Projects={}}
local next=0
for tier in ipairs(SPCCrewModel.CAPACITY)do for _,ratio in ipairs(SPCCrewModel.RATIOS)do
 next=next+1;local id=SPCCrewModel.Project(tier,ratio);local r={Index=next,ProjectType=id,Cost=SPCCrewModel.Cost(tier,ratio,100)};GameInfo.Projects[id]=r;GameInfo.Projects[next]=r
end end
CityProductionDirectives={PROJECT=7,TRAIN=8};PlayerOperations={EXECUTE_SCRIPT=5}
queue={};completed={};q={GetSize=function()return #queue end,GetAt=function(_,i)return queue[i+1]end,GetProjectCost=function(_,id)return GameInfo.Projects[id].Cost end}
c={GetOwner=function()return owner end,GetID=function()return 9 end,GetX=function()return 10 end,GetY=function()return 11 end,GetBuildQueue=function()return q end};owner=0
Players={[0]={GetCities=function()return {FindID=function(_,id)if id==9 then return c end end}end,GetStats=function()return {GetNumProjectsAdvanced=function(_,id)return completed[id]or 0 end}end}}
selected=c;UI={GetHeadSelectedCity=function()return selected end}
Locale={Lookup=function(k,arg)return k..(arg or '')end}
ExposedMembers={SPC_P0={CrewProjects={revision=1,views={['0:9']={allowed={PROJECT_SPC_CREW_250=true}}},errors={}}}}
sent={};built=0;notified=0
api=SPCCrewProjectUI.New(P,function(pid,op,p)
 assert(pid==0 and op==5);sent[#sent+1]=p
 if nestedSend then nestedSend(p)end
end,function()notified=notified+1 end,function(city,item)
 built=built+1;assert(city==c and item.Type=='PROJECT_SPC_CREW_250')
 if buildNested then api.Publish()end
 if buildDenied then return false end
 if not delayed then queue[#queue+1]={Directive=7,ProjectType=GameInfo.Projects[item.Type].Index}end
end)
item={Type='PROJECT_SPC_CREW_250'}
function reply(extra)
 local p=sent[#sent];extra=extra or {};extra.token=p.Token;extra.owner=0;extra.city=9;ExposedMembers.SPC_CrewReply=extra
end
function reserve()
 assert(api.Before(c,item,false)==false);assert(#sent==1 and sent[1].Action=='RESERVE' and built==0)
 reply({reservation=1,before=0,base=0});api.Publish()
end
'''
def fixture():
    l=LuaRuntime(unpack_returned_tuples=True)
    l.execute('include=function()end')
    for f in ('CrewModel.lua','UI/CrewProjectUI.lua'):l.execute((M/f).read_text())
    l.execute(SETUP);return l
class CrewProductionUI(unittest.TestCase):
    def check(self,s):fixture().execute(s)
    def test_single_build_confirm_ack_and_actual_reader(self):
        self.check("reserve();assert(built==1 and #sent==2 and sent[2].Action=='CONFIRM');local q=ExposedMembers.SPC_CrewNativeRead(0,9);assert(q.projects[item.Type]==1 and q.costs[item.Type]==375 and q.completed[item.Type]==0);reply({confirmed=true});api.Publish();for i=1,10 do api.Publish()end;assert(built==1 and #sent==2 and not ExposedMembers.SPC_CrewUIError)")
    def test_delayed_native_queue_waits_for_event_not_return_or_reissued_build(self):
        self.check("delayed=true;reserve();assert(built==1 and #sent==1);for i=1,3 do api.Publish()end;assert(built==1 and #sent==1);queue[1]={Directive=7,ProjectType=GameInfo.Projects[item.Type].Index};api.Publish();assert(#sent==2 and sent[2].Action=='CONFIRM' and built==1)")
    def test_completed_during_native_operation_can_ack_without_queue(self):
        self.check("delayed=true;reserve();completed[GameInfo.Projects[item.Type].Index]=1;api.Publish();assert(sent[2].Action=='CONFIRM');reply({finished=true});api.Publish();assert(not ExposedMembers.SPC_CrewUIError and built==1)")
    def test_nested_publish_never_repeats_native_build(self):
        self.check("buildNested=true;reserve();assert(built==1 and #sent==2)")
    def test_reentrant_reserve_transmission_has_token_before_send(self):
        self.check("nestedSend=function(p)if p.Action=='RESERVE'then reply({reservation=1,before=0,base=0});api.Publish()end end;api.Before(c,item,false);assert(built==1 and #sent==2 and sent[2].Action=='CONFIRM')")
    def test_selection_change_cancels_before_build_and_error_is_readable(self):
        self.check("api.Before(c,item,false);selected=nil;reply({reservation=1,before=0,base=0});api.Publish();assert(built==0 and sent[2].Action=='CANCEL');reply({error='CREW_CANCEL_UNCONFIRMED'});api.Publish();local d={City=c,ProjectItems={{Type=item.Type,ToolTip='cost'}}};api.Items(d);assert(d.ProjectItems[1].ToolTip:find('CREW_CANCEL_UNCONFIRMED',1,true))")
    def test_native_reject_cancels_without_confirm(self):
        self.check("buildDenied=true;reserve();assert(sent[2].Action=='CANCEL' and built==1);reply({cancelled=true});api.Publish();assert(#sent==2)")
    def test_denied_silent_native_order_cancels_on_turn_change_without_retry(self):
        self.check("delayed=true;reserve();turn=2;api.Publish();assert(sent[2].Action=='CANCEL' and built==1)")
    def test_filter_exact_current_price_preserves_unrelated_projects_and_native_queue(self):
        self.check("local d={City=c,ProjectItems={{Type='OTHER',ToolTip='same'},{Type='PROJECT_SPC_CREW_250',ToolTip='cost'},{Type='PROJECT_SPC_CREW_250_P140'}}};api.Items(d);assert(#d.ProjectItems==2 and d.ProjectItems[1].ToolTip=='same');assert(api.Before(c,{Type='OTHER'},false));assert(not api.Before(c,item,true) and #sent==0);assert(not pcall(ExposedMembers.SPC_CrewNativeRead,1,9))")
if __name__=='__main__':unittest.main()
