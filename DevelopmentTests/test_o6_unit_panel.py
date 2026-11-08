"""Exercise the selected UnitPanel entry, shared action policy and real REST dispatcher.

Native Lua is read locally. The fixture only executes named source fragments and
does not model native rendering or loading beyond the explicit manifest choice.
"""
from hashlib import sha256
import os
from pathlib import Path
import unittest

from refactor_harness import Context, PackageVFS, executed
from test_b414_crew_unit_panel import FIXTURE
from test_environment_assembly import manifest, matches_profile
from test_pu02_restructuring_ui import function, ui as restructuring_panel


def selected_entry(hd):
    root = manifest()
    criteria = {entry.get('id'): entry for entry in root.findall('./ActionCriteria/Criteria')}
    entries = [
        action.findtext('Properties/LuaReplace')
        for action in root.findall('./InGameActions/ReplaceUIScript')
        if action.findtext('Properties/LuaContext') == 'UnitPanel'
        and matches_profile(action, criteria, hd)
    ]
    if len(entries) > 1:
        raise AssertionError('MULTIPLE_UNIT_PANEL_ENTRIES')
    return entries[0] if entries else None


def panel(hd, expansion=None):
    context = Context(name='UnitPanel', vfs=PackageVFS())
    context.execute(FIXTURE)
    expected_base = 'DL_UnitPanel' if hd else 'UnitPanel_Expansion2'
    loaded_bases = []

    if expansion is not None:
        path = Path(expansion) / 'DLC/Expansion2/UI/Replacements/UnitPanel_Expansion2.lua'
        data = path.read_bytes()
        digest = sha256(data).hexdigest()
        assert digest == '2ff1396a299a4cafac3e7d4c217eb74ee5ebf2eb6f57e03e5ef41bb58547ff78'
        executed('external:UnitPanel_Expansion2.lua', digest, 'source_fragments_only')
        context.execute("""
            g_isOkayToProcess=true
            UnitOperationTypes.PARAM_IMPROVEMENT_TYPE=101
            UnitOperationTypes.PARAM_OPERATION_TYPE=102
            UnitOperationTypes.BUILD_IMPROVEMENT_ADJACENT=103
            InterfaceModeTypes={BUILD_IMPROVEMENT_ADJACENT=104}
            UI.SetInterfaceMode=function(mode,params) entered=mode; operation=params[102]end
            ContextPtr.RequestRefresh=function()end
        """)
        context.execute(function(data.decode(), 'function OnUnitActionClicked_BuildImprovementAdjacent('))

    def include(name):
        if name in ('DL_UnitPanel', 'UnitPanel_Expansion2'):
            assert name == expected_base and not loaded_bases
            loaded_bases.append(name)
        elif name == 'ExpeditionSpyUnitPanel':
            assert loaded_bases == [expected_base]
            context.load('UI/ExpeditionSpyUnitPanel', included=True)
        elif name not in ('ExpeditionSpyUI', 'RestructuringUI'):
            raise AssertionError(f'UNEXPECTED_UNIT_PANEL_INCLUDE {name}')
        # The Crew-only fixture doubles the two other action owners. The
        # restructuring case below runs its real UI, gameplay and Store.

    context.globals().include = include
    entry = selected_entry(hd)
    if entry:
        context.load(entry)
    return context


class UnitPanelProfiles(unittest.TestCase):
    def test_crew_whitelist_reaches_native_actions_in_both_profiles(self):
        for hd in (False, True):
            with self.subTest(hd=hd):
                panel(hd).execute("""
                    local a=GetUnitActionsTable(crews[1])
                    assert(a.MOVE[11] and a.SPECIFIC[12] and a.INPLACE[13])
                    assert(not a.SPECIFIC[21] and next(a.BUILD)==nil,'HARVEST_BUTTON_LEAK')
                    assert(a.hotkeys.MoveTo and a.hotkeys.Sleep and not a.hotkeys.FoundCity)
                    local ordinary=GetUnitActionsTable(builder)
                    assert(ordinary.SPECIFIC[21] and ordinary.BUILD[26])
                """)

    def test_gathering_storm_adjacent_callback_checks_selected_unit(self):
        panel(False, os.environ['SPC_OFFICIAL_ASSETS']).execute("""
            selected=crews[1]
            OnUnitActionClicked_BuildImprovementAdjacent(17)
            assert(not entered,'CREW_ADJACENT_IMPROVEMENT_LEAK')
            selected=builder
            OnUnitActionClicked_BuildImprovementAdjacent(17)
            assert(entered==104 and operation==103)
        """)

    def test_official_restructuring_confirmation_reaches_real_owner_once(self):
        entry = selected_entry(False)
        l = restructuring_panel(unit_panel_entry=entry.removesuffix('.lua') if entry else None)
        l.execute("""
            assert(tagged(-247),'OFFICIAL_PREPARE_MISSING')
            press(-247);draw()
            press(-247)
            assert(actionCount('REST_PREPARE')==1 and not Z.state())
            local confirm=assert(tagged(-248))[1]
            confirm();confirm()
            assert(actionCount('REST_CONFIRM')==1 and Z.state().phase=='REALLOCATING')
        """)
