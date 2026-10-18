"""Current Research/Culture institution UI, actual Lua with isolated controls.

Proves selected-city identity, cumulative rows and ACTIVE/UNKNOWN display logic;
native typography, truncation and layout still require visual acceptance.
"""
from pathlib import Path
import sqlite3
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime

ROOT=Path(__file__).resolve().parents[1]


def display():
    lua=LuaRuntime()
    db=sqlite3.connect(':memory:')
    db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))')
    db.executescript((ROOT/'Mod/Text/TestText.sql').read_text())
    lua.globals().loc=lua.table_from(dict(db.execute("select Tag,Text from LocalizedText where Language='zh_Hans_CN'")))
    db.close()
    lua.execute('''
      function include()end
      Locale={Lookup=function(k)return loc[k]or k end}
      local function event()local e={};function e.Add(f)e.f=f end;function e.Remove(f)if e.f==f then e.f=nil end end;return setmetatable(e,{__call=function(_,...)if e.f then return e.f(...)end end})end
      LuaEvents={SPC_InstitutionOverview=event(),SPC_PresentationChanged=event()}
      ExposedMembers={SPC_P0={}};Game={GetLocalPlayer=function()return 0 end}
      city={GetID=function()return 4 end,GetOwner=function()return 0 end,GetX=function()return 8 end,GetY=function()return 9 end}
      UI={GetHeadSelectedCity=function()return city end}
      local function control()local c={}
       function c:SetHide(v)self.hidden=v end;function c:IsHidden()return self.hidden or false end
       function c:SetText(v)self.text=v end;function c:SetAlpha(v)self.alpha=v end
       function c:SetToolTipString(v)self.tip=v end;function c:CalculateSize()sizes=sizes+1 end
       function c:ReprocessAnchoring()end;function c:ChangeParent()parents=parents+1 end
       function c:DestroyChild()end
       return c
      end
      sizes=0;parents=0;nativeRenders=0;resets=0
      Controls={InstitutionContainer=control(),InstitutionRows=control(),InstitutionHeader=control(),PanelBreakdown=control()}
      parent=control();parent.GetChildren=function()return {Controls.InstitutionContainer}end
      parent.SortChildren=function()error('already first; no re-sort')end
      ContextPtr={SetHide=function()end,LookUpControl=function()return parent end,
       SetInitHandler=function(self,f)init=f end,SetShutdown=function(self,f)shutdown=f end}
      InstanceManager={new=function()local m={items={}}
       function m:GetInstance()local row={Top=control(),Stage=control(),Name=control(),State=control()};self.items[#self.items+1]=row;return row end
       function m:ResetInstances()resets=resets+1;self.items={}end
       function m:DestroyInstances()self.items={}end
       rows=m;return m
      end}
      local buildings={{BuildingType='BUILDING_SPC_OWN',InternalOnly=true},{BuildingType='BUILDING_OTHER_MOD',InternalOnly=true}}
      GameInfo={Buildings=function()return ipairs(buildings)end}
      -- Match the game's single row iterator rather than ipairs' index/value pair.
      GameInfo.Buildings=function()local i=0;return function()i=i+1;return buildings[i]end end
      function ViewPanelBreakdown(d)nativeRenders=nativeRenders+1;rendered=d end
      data={Owner=0,City=city,BuildingsAndDistricts={{Buildings={{Type='BUILDING_SPC_OWN'},{Type='BUILDING_LIBRARY'},{Type='BUILDING_OTHER_MOD'}}}}}
      v={owner=0,cityID=4,x=8,y=9,specialization='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
      ExposedMembers.SPC_P0.CityPresentationView=v
    ''')
    for filename in ['InstitutionPresentation.lua','UI/InstitutionOverview.lua','UI/Institutions.lua']:
        lua.execute((ROOT/'Mod'/filename).read_text())
    lua.execute('init();ViewPanelBreakdown(data)')
    return lua


class CultureInstitutionDisplay(unittest.TestCase):
    def test_culture_names_cumulative_levels_and_current_row(self):
        lua=display()
        lua.execute('''
          local expected={'文艺同好会','赞助人行会','人文联合会','博雅总院'}
          local roman={'Ⅰ','Ⅱ','Ⅲ','Ⅳ'}
          assert(#rows.items==4 and not Controls.InstitutionContainer.hidden)
          for i,row in ipairs(rows.items)do
           assert(row.Name.text==expected[i] and row.Stage.text==roman[i])
           assert(row.State.text==(i==4 and '当前' or '启用'))
          end
          assert(rows.items[3].Top.tip:find('时代对话',1,true))
          assert(rows.items[4].Top.tip:find('巨作启迪',1,true))
          assert(rows.items[4].Top.tip:find('尚未实施',1,true))
          assert(#rendered.BuildingsAndDistricts[1].Buildings==2)
          assert(#data.BuildingsAndDistricts[1].Buildings==3)
          for potential=1,2 do v.potential=potential;v.active=potential;LuaEvents.SPC_PresentationChanged();assert(#rows.items==potential)end
        ''')

    def test_active_drop_keeps_established_rows_and_unknown_does_not_erase(self):
        lua=display()
        lua.execute('''
          v.active=2;LuaEvents.SPC_PresentationChanged()
          assert(#rows.items==4 and rows.items[2].State.text=='当前' and rows.items[4].State.text=='未激活')
          ExposedMembers.SPC_P0.CityPresentationView={owner=0,cityID=4,error='temporary'}
          LuaEvents.SPC_PresentationChanged()
          assert(#rows.items==4 and rows.items[4].Name.text=='博雅总院' and rows.items[4].State.text=='待确认')
          ExposedMembers.SPC_P0.CityPresentationView=v;v.active=4;LuaEvents.SPC_PresentationChanged()
          assert(rows.items[4].State.text=='当前')
        ''')

    def test_same_city_identity_change_refreshes_both_signatures(self):
        lua=display()
        lua.execute('''
          local before=nativeRenders;v.specialization='RESEARCH';LuaEvents.SPC_PresentationChanged()
          assert(nativeRenders==before+1 and rows.items[1].Name.text=='学者结社')
          assert(rows.items[4].Name.text=='学术总署')
          v.specialization='CULTURE';LuaEvents.SPC_PresentationChanged();assert(rows.items[1].Name.text=='文艺同好会')
          v.specialization='INDUSTRY';LuaEvents.SPC_PresentationChanged();assert(rows.items[1].Name.text=='匠作坊')
          v.specialization='COMMERCE';LuaEvents.SPC_PresentationChanged();assert(Controls.InstitutionContainer.hidden and #rows.items==0)
        ''')

    def test_selected_city_and_owner_guard_prevent_stale_presentation(self):
        lua=display()
        lua.execute('''
          local other={GetID=function()return 5 end,GetOwner=function()return 0 end,GetX=function()return 1 end,GetY=function()return 1 end}
          local d={Owner=0,City=other,BuildingsAndDistricts={}}
          ViewPanelBreakdown(d);assert(Controls.InstitutionContainer.hidden)
          ViewPanelBreakdown(data);assert(not Controls.InstitutionContainer.hidden)
          data.Owner=1;ViewPanelBreakdown(data);assert(Controls.InstitutionContainer.hidden)
        ''')

    def test_duplicate_notifications_do_not_rebuild_and_sibling_rows_supported(self):
        lua=display()
        lua.execute('''
          local s,r,n=sizes,resets,nativeRenders
          for i=1,1000 do LuaEvents.SPC_PresentationChanged();LuaEvents.SPC_InstitutionOverview(data,v)end
          assert(sizes==s and resets==r and nativeRenders==n and parents==1)
          local model=SPCInstitutionPresentation
          model.BySpecialization.CULTURE[5]={level=4,name='Sibling',text='Same level'}
          v.active=3;LuaEvents.SPC_PresentationChanged();assert(#rows.items==5 and rows.items[5].State.text=='未激活')
          v.active=4;LuaEvents.SPC_PresentationChanged();assert(rows.items[4].State.text=='当前' and rows.items[5].State.text=='当前')
        ''')

    def test_existing_layout_and_all_added_localizations_are_well_formed(self):
        root=ET.parse(ROOT/'Mod/UI/Institutions.xml').getroot()
        row=root.find("./Instance[@Name='InstitutionRowInstance']/Grid")
        self.assertEqual(row.get('Size'),'parent,32')
        name=next(x for x in row.iter() if x.get('ID')=='Name')
        self.assertEqual(name.get('TruncateWidth'),'parent')
        for file in ['InstitutionPresentation.lua','UI/InstitutionOverview.lua','UI/Institutions.lua']:
            source=(ROOT/'Mod'/file).read_text()
            for forbidden in ['RequestPlayerOperation','SetUpdate','SetProperty','CreateBuilding','RemoveBuilding']:
                self.assertNotIn(forbidden,source)


if __name__=='__main__':unittest.main()
