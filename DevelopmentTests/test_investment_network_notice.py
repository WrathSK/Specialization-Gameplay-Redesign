"""A blocked investment may explain a known cause without changing admission."""
from contextlib import closing
from pathlib import Path
import sqlite3
import unittest
from unittest.mock import patch

from lupa.lua51 import LuaRuntime
import test_b252_sidebar as development_panel
import test_b262_capital_sidebar as capital_panel
from test_network_city_registration import registration
from test_refactor_s6f import development


MOD = Path(__file__).resolve().parents[1] / 'Mod'


class NetworkNotice(unittest.TestCase):
    def test_scoped_city_current_proof_and_transport_limit(self):
        lua = registration()
        lua.execute("""
        assert(not net.InvestmentNotice(0));prove();checkGate(true)
        local lookups=0
        incoming.GetName=function()lookups=lookups+1;return 'LOC_CITY_TRANSFER' end
        mapTransfer(incoming,0,902);checkUnresolved()
        local before=T.encode(T.props())
        local notice=assert(net.InvestmentNotice(0))
        assert(notice.tag=='LOC_SPC_INVESTMENT_NETWORK_CITY' and notice.city=='LOC_CITY_TRANSFER')
        local observed=lookups
        notice.city='other'
        assert(net.InvestmentNotice(0).city=='LOC_CITY_TRANSFER' and not net.InvestmentNotice(9))
        assert(lookups==observed and T.encode(T.props())==before)
        shared.RouteSignalRevision=shared.RouteSignalRevision+1
        assert(not net.InvestmentNotice(0) and not net.TransactionCurrent(0))
        incoming.GetName=function()error('display name unavailable')end
        checkUnresolved();assert(net.InvestmentNotice(0).city=='#902')
        final(incoming,CityTransferTypes.BY_GIFT);checkRegistered()
        assert(not net.InvestmentNotice(0))
        for _,limit in ipairs({'NETWORK_ROUTE_LIMIT','NETWORK_PAYLOAD_LIMIT'})do
         seq=seq+1
         net.Receive(0,{Epoch=net.epoch,Seq=seq,Turn=Game.GetCurrentGameTurn(),
          Signal=shared.RouteSignalRevision,Valid=0,Failure=limit})
         assert(net.InvestmentNotice(0).tag=='LOC_SPC_INVESTMENT_NETWORK_LIMIT')
         assert(not net.TransactionCurrent(0))
         checkRegistered();assert(not net.InvestmentNotice(0))
        end
        """)

    def test_contract_services_keep_their_guards_and_clear_the_notice(self):
        lua = development()
        lua.execute("""
        local bridge=shared.NetworkBridge
        bridge.InvestmentNotice=function()return {tag='LOC_SPC_INVESTMENT_NETWORK_CITY',city='Boston'}end
        networkFail=true
        local capView=cap.Refresh(0,source:GetID(),true)
        assert(capView.domains[1].reason=='CAPITAL_NETWORK_PENDING' and capView.domains[1].networkNotice.city=='Boston')
        shared.Commerce.TransactionCurrent=function()return false end
        capView=cap.Refresh(0,source:GetID(),true)
        assert(capView.stage=='HELD' and capView.reason=='CAPITAL_COMMERCE_PENDING' and capView.networkNotice.city=='Boston')
        open()
        assert(view().reason=='DEVELOPMENT_OUTGOING_PENDING' and view().networkNotice.city=='Boston')
        assert(not sign() and not C.confirm() and moneyCalls==0)
        bridge.InvestmentNotice=function()return nil end
        assert(not cap.Refresh(0,source:GetID(),true).networkNotice)
        shared.Commerce.TransactionCurrent=function()return true end
        networkFail=false;open()
        assert(not view().networkNotice and view().options[1].canSign)
        capView=cap.Refresh(0,source:GetID(),true)
        assert(not capView.networkNotice and not capView.domains[1].networkNotice)
        """)

    def test_both_panels_show_localized_cause_and_keep_confirmation_disabled(self):
        with closing(sqlite3.connect(':memory:')) as db:
            db.execute('CREATE TABLE LocalizedText(Language, Tag, Text, PRIMARY KEY(Language,Tag))')
            db.executescript((MOD/'Text/Commerce.sql').read_text())
            for lang in ('zh_Hans_CN', 'en_US'):
                texts = dict(db.execute("SELECT Tag, Text FROM LocalizedText WHERE Language=? "
                                        "AND Tag GLOB 'LOC_SPC_INVESTMENT_NETWORK_*'", (lang,)))
                self.assertEqual(len(texts), 2)
                for panel, view, control in ((capital_panel, 'capitalView', 'Current'),
                                             (development_panel, 'developmentView', 'Error')):
                    with self.subTest(lang=lang, panel=view), patch.object(development_panel, 'LuaRuntime', LuaRuntime):
                        lua = panel.ui()
                        lua.globals().noticeText = lua.table_from(texts)
                        lua.execute("""
                        local lookup=Locale.Lookup
                        Locale.Lookup=function(key,...)
                         if key=='LOC_TEST_CITY' then return 'Boston' end
                         if noticeText[key] then return (noticeText[key]:gsub('{1}',(...) or '')) end
                         return lookup(key,...)
                        end
                        """)
                        if view == 'developmentView':
                            lua.execute('LuaEvents.SPC_DevelopmentOpen(0,9);ack()')
                        lua.execute(f"v={view};v.canSign=false;v.stage='HELD';"
                                    "v.reason='" + ('CAPITAL_COMMERCE_PENDING' if view == 'capitalView'
                                                    else 'DEVELOPMENT_OUTGOING_PENDING') + "'")
                        for tag, value in texts.items():
                            lua.globals().tag = tag
                            lua.execute("v.networkNotice={tag=tag,city='LOC_TEST_CITY'};notify()")
                            self.assertIn(value.replace('{1}', 'Boston'), lua.eval(f'Controls.{control}.text'))
                            self.assertTrue(lua.eval('Controls.Confirm.disabled'))
