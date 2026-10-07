"""W02 audit evidence: bounded cache reproduction using unchanged actual Lua.
Run with Python + lupa.lua55 available (see DevelopmentTests/README.md).
No game, DB, deployment, repository writes or top-level historical test suite.
Archived from the existing temporary reproduction; only root routing and the
unused optional DB-classification tail changed. Core reproduction is unchanged.
"""
from pathlib import Path
import ast, json, sqlite3, sys
from collections import Counter
R=Path(__file__).resolve().parents[5]  # repository root; no personal machine path
p=R/'DevelopmentTests/test_p0_a.py'
tree=ast.parse(p.read_text())
kept=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id in {'R','M','NEW','FIX'} for t in n.targets)]
ns={'__file__':str(p)}
exec(compile(ast.Module(body=kept,type_ignores=[]),str(p),'exec'),ns)
out={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION; mocked native getters; no native timing', 'source':'actual current Mod/DistrictCompleteness.lua', 'fixture':'AST extracted test_p0_a runtime only; no top-level tests executed', 'same_input':{'turn':1,'owner':0,'districts_per_city':1,'building':'BUILDING_LIBRARY','D':1,'dirty_events_between_sweeps':0}, 'sweeps':[]}
for n in (8,9,20,40):
    lua=ns['runtime']()
    result=lua.execute('''
      local total=...;local hasCalls=0;local reports={}
      for i=1,total do
        local city=newCity(i);local district=addDistrict(city,20+i,'DISTRICT_CAMPUS');setBuildings(district,{'BUILDING_LIBRARY'})
        local getter=city.GetBuildings
        city.GetBuildings=function(self)
          local buildings=getter(self);local has=buildings.HasBuilding
          buildings.HasBuilding=function(b,index)hasCalls=hasCalls+1;return has(b,index)end
          return buildings
        end
      end
      counters={};reads=0
      for sweep=1,3 do
        for i=1,total do
          local city=cities[i];local view=svc.Read(0,city,city.token)
          assert(view.validity=='VERIFIED' and view.availability=='READY' and view.value.domains.DISTRICT_CAMPUS.value==1)
        end
        assert(writes==0 and turn==1 and svc.CacheSize()<=8)
        reports[sweep]={sweep=sweep,cities=total,definitions=#brows,captures=counters.dc_capture or 0,cacheHits=counters.dc_hit or 0,districtScans=counters.district_scan or 0,buildingChecks=counters.building_check or 0,hasBuildingCalls=hasCalls,mockNativeReads=reads,cacheSize=svc.CacheSize(),writes=writes}
      end
      return reports
    ''',n)
    rows=[dict(result[i].items()) for i in range(1,4)]
    for row in rows:
        previous=rows[row['sweep']-2] if row['sweep']>1 else {}
        row['captureDelta']=row['captures']-previous.get('captures',0)
        row['hasBuildingDelta']=row['hasBuildingCalls']-previous.get('hasBuildingCalls',0)
        row['cloneCount']='NOT_AVAILABLE: local recursive Clone is not instrumented'
        assert row['hasBuildingCalls']==row['buildingChecks']
        assert row['captures']==(n if n==8 else n*row['sweep'])
    out['sweeps'].extend(rows)

print(json.dumps(out,ensure_ascii=False,indent=2))
