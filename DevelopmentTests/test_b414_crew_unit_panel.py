"""B414: check the actual SPC UnitPanel wrapper with native-shaped action rows."""

from pathlib import Path
import unittest

from lupa.lua51 import LuaRuntime


ROOT = Path(__file__).resolve().parents[1]
PANEL = (ROOT / 'Mod/UI/ExpeditionSpyUnitPanel.lua').read_text()
FIXTURE = r"""
GameInfo={Units={},UnitCommands={},UnitOperations={}}
UnitOperationTypes={TYPE=1}
UnitCommandTypes={TYPE=2}
local crewIds={250,420,750,1000,1360}
function unit(index,kind)
 GameInfo.Units[index]={UnitType=kind}
 return {GetUnitType=function()return index end}
end
crews={}
for _,id in ipairs(crewIds)do crews[#crews+1]=unit(id,'UNIT_SPC_CREW_'..id)end
builder=unit(1,'UNIT_BUILDER')
settler=unit(2,'UNIT_SETTLER')
selected=crews[1]
UI={GetHeadSelectedUnit=function()return selected end}
SPCExpeditionSpyUI={IsTeam=function()return false end}
SPCRestructuringUI={IsTeam=function()return false end,BlockDelete=function()return false end}
include=function()end
local event={Add=function()end,Remove=function()end}
Events={}
LuaEvents={SPC_ExpeditionActivityChanged=event}
ContextPtr={SetShutdown=function()end}
local rows={}
local function native(id,category,hash,hotkey)
 local command=id:match('^UNITCOMMAND_')~=nil
 local row={CategoryInUI=category,HotkeyId=hotkey}
 local list=command and GameInfo.UnitCommands or GameInfo.UnitOperations
 row[command and 'CommandType' or 'OperationType']=id
 list[hash]=row
 rows[#rows+1]={row,hash,command and UnitCommandTypes.TYPE or UnitOperationTypes.TYPE}
end
native('UNITOPERATION_MOVE_TO','MOVE',11,'MoveTo')
native('UNITOPERATION_SWAP_UNITS','SPECIFIC',12)
native('UNITOPERATION_SLEEP','INPLACE',13,'Sleep')
native('UNITCOMMAND_WAKE','INPLACE',14)
native('UNITCOMMAND_ENTER_FORMATION','SPECIFIC',15)
native('UNITCOMMAND_NAME_UNIT','SPECIFIC',16)
native('UNITCOMMAND_DELETE','SECONDARY',17)
native('UNITOPERATION_HARVEST_RESOURCE','SPECIFIC',21)
native('UNITOPERATION_REPAIR','SPECIFIC',22)
native('UNITOPERATION_REMOVE_FEATURE','BUILD',23)
native('UNITCOMMAND_HARVEST_WONDER','SPECIFIC',24)
native('UNITOPERATION_FOUND_CITY','SPECIFIC',25,'FoundCity')

clicks={}
function OnUnitActionClicked(kind,hash)clicks[#clicks+1]=hash end
function OnUnitActionClicked_BuildImprovement(hash)clicks[#clicks+1]=hash end
function AddActionToTable(actions,row,disabled,tip,hash,callback,kind)
 actions[row.CategoryInUI][hash]=callback
 if row.HotkeyId and not disabled then actions.hotkeys[row.HotkeyId]=callback end
end
function GetUnitActionsTable(u)
 if onBuild then onBuild(u)end
 local actions={MOVE={},INPLACE={},SPECIFIC={},SECONDARY={},BUILD={},hotkeys={}}
 for _,entry in ipairs(rows)do
  local row,hash,kind=unpack(entry)
  AddActionToTable(actions,row,false,'',hash,function()OnUnitActionClicked(kind,hash)end,kind)
 end
 AddActionToTable(actions,{CategoryInUI='BUILD'},false,'',26,
  function()OnUnitActionClicked_BuildImprovement(26)end)
 AddActionToTable(actions,{CategoryInUI='SPECIFIC'},false,'',27,function()end)
 return actions
end
"""


def panel():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute("io=nil;os=nil;debug=nil;package=nil;require=nil;dofile=nil;loadfile=nil")
    lua.execute(FIXTURE)
    lua.execute(PANEL)
    return lua


class CrewActionPolicy(unittest.TestCase):
    def test_all_crew_tiers_keep_common_controls_and_omit_abilities(self):
        panel().execute("""
            for _,crew in ipairs(crews)do
                selected=crew
                local a=GetUnitActionsTable(crew)
                assert(a.MOVE[11] and a.SPECIFIC[12] and a.INPLACE[13] and a.INPLACE[14])
                assert(a.SPECIFIC[15] and a.SPECIFIC[16] and a.SECONDARY[17])
                assert(not a.SPECIFIC[21],'HARVEST_BUTTON_LEAK')
                assert(not a.SPECIFIC[22] and not a.SPECIFIC[24] and not a.SPECIFIC[25])
                assert(not a.SPECIFIC[27] and next(a.BUILD)==nil)
                assert(a.hotkeys.MoveTo and a.hotkeys.Sleep and not a.hotkeys.FoundCity)
            end
        """)

    def test_builder_and_settler_keep_native_action_registration(self):
        panel().execute("""
            selected=crews[1]
            local ordinary=GetUnitActionsTable(builder)
            assert(ordinary.SPECIFIC[21] and ordinary.BUILD[26])
            local settlerActions=GetUnitActionsTable(settler)
            assert(settlerActions.SPECIFIC[25] and settlerActions.hotkeys.FoundCity)
            selected=builder
            ordinary.SPECIFIC[21]()
            assert(#clicks==1 and clicks[1]==21)
        """)

    def test_stale_native_ability_callbacks_cannot_use_selected_crew(self):
        panel().execute("""
            local ordinary=GetUnitActionsTable(builder)
            selected=crews[1]
            ordinary.SPECIFIC[21]()
            ordinary.SPECIFIC[24]()
            ordinary.BUILD[26]()
            assert(#clicks==0,'CREW_NATIVE_ABILITY_DISPATCH')
            ordinary.MOVE[11]()
            ordinary.SPECIFIC[12]()
            assert(#clicks==2 and clicks[1]==11 and clicks[2]==12)
        """)

    def test_native_builder_exception_and_reentry_restore_scope(self):
        panel().execute("""
            onBuild=function(u)
                if u==crews[1] then
                    local nested=GetUnitActionsTable(builder)
                    assert(nested.SPECIFIC[21] and nested.BUILD[26])
                end
            end
            local crewActions=GetUnitActionsTable(crews[1])
            assert(not crewActions.SPECIFIC[21])
            onBuild=function()error('NATIVE_ACTION_BUILD_FAILED')end
            local ok,err=pcall(GetUnitActionsTable,crews[1])
            assert(not ok and err:find('NATIVE_ACTION_BUILD_FAILED'))
            onBuild=nil
            local outside={SPECIFIC={},hotkeys={}}
            AddActionToTable(outside,GameInfo.UnitOperations[21],false,'',21,function()end)
            assert(outside.SPECIFIC[21])
        """)


if __name__ == '__main__':
    unittest.main()
