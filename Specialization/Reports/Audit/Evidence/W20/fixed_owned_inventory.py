from pathlib import Path
import re,sqlite3,xml.etree.ElementTree as ET,json,collections
root=Path('Mod'); xml=ET.parse(root/'SpecializationP0.modinfo')
files=[x.text for a in xml.findall('./InGameActions/UpdateDatabase') for x in a.findall('File')]
rows=[]; dynamic=[]; columns=collections.defaultdict(set)
for file in files:
    raw=(root/file).read_text()
    raw=re.sub(r'--[^\n]*','',raw)
    for m in re.finditer(r'INSERT\s+(?:OR\s+\w+\s+)?INTO\s+(Types|Buildings)\s*\(([^)]*)\)\s*(.*?);',raw,re.S|re.I):
        table=m.group(1); col=[c.strip() for c in m.group(2).split(',')]; rest=m.group(3).strip()
        line=(root/file).read_text()[:(root/file).read_text().find(m.group(0).split('(',1)[0])].count('\n')+1
        if rest.upper().startswith('VALUES'):
            columns[table].update(col); rows.append((file,table,m.group(0)))
        else: dynamic.append((file,table))
db=sqlite3.connect(':memory:')
for t,cs in columns.items(): db.execute('CREATE TABLE '+t+'('+','.join('"'+c+'"' for c in sorted(cs))+', _file)')
for f,t,s in rows:
    before=db.execute('SELECT COUNT(*) FROM '+t).fetchone()[0]
    db.execute(s)
    db.execute('UPDATE '+t+' SET _file=? WHERE _file IS NULL',(f,))
def q(s): return db.execute(s).fetchall()
F={}
def add(k,seq):F[k]=set(seq)
def bits(p,n):return [p+str(i) for i in range(n)]
add('Support',['BUILDING_SPC_DEV_'+k+'_SUPPORT' for k in ['RESEARCH','CULTURE','COMMERCE']])
add('Lv2Housing',bits('BUILDING_SPC_DEV_LV2_HOUSING_',9))
add('Lv2GPP',[f'BUILDING_SPC_DEV_GPP_{k}_{i}' for k in ['RESEARCH','CULTURE','INDUSTRY','COMMERCE'] for i in range(8)])
add('Lv3SupportRetired',[f'BUILDING_SPC_DEV_LV3_{k}' for k in ['RESEARCH','CULTURE','COMMERCE','INDUSTRY']]+bits('BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_',8))
add('Lv3Effects',bits('BUILDING_SPC_DEV_LV3_POP_CULTURE_',8)+[f'BUILDING_SPC_DEV_LV3_COM_{k}' for k in ['RESEARCH','CULTURE','INDUSTRY']])
add('Lv4PercentRetired',bits('BUILDING_SPC_LV4_PERCENT_CULTURE_',8))
add('IndustrySupport',[f'BUILDING_SPC_DEV_INDUSTRY_LV1_{i}' for i in range(-1,8)])
add('CrewProjects',['BUILDING_SPC_CREW_PROJECT_ACCESS'])
add('ResearchInfrastructure',bits('BUILDING_SPC_RESEARCH_INFRA_',4)+bits('BUILDING_SPC_LV4_PERCENT_RESEARCH_',8)+[f'BUILDING_SPC_B051_SCIENCE_{m}_{i}' for m in ['POS','NEG','POP'] for i in range(8 if m=='POP' else 16)])
add('ResearchCross',[f'BUILDING_SPC_RESEARCH_CROSS_{s}_{i}' for s in ['POS','NEG'] for i in range(16)]+bits('BUILDING_SPC_DEV_LV3_POP_RESEARCH_',8)+[f'BUILDING_SPC_B082_DISTRICT_{s}' for s in ['03','05','1']])
add('Apply',[f'BUILDING_SPC_RESEARCH_APPLY_{y}_{i}' for y in ['FOOD','PRODUCTION','GOLD','CULTURE','FAITH'] for i in range(5)])
add('Tradition',[f'BUILDING_SPC_RESEARCH_TRADITION_{n}' for n in [5,10,15,20,25]])
add('Copy',[f'BUILDING_SPC_B051_PRODUCTION_{m}_{i}' for m in ['POS','NEG','POP'] for i in range(8 if m=='POP' else 16)])
add('Half',[f'BUILDING_SPC_B050_{y}_{m}_{i}' for y in ['SCIENCE','PRODUCTION'] for m in ['POP','SUB'] for i in range(8)])
boosts=re.findall(r"building='([^']+)'",(root/'BoostConfig.lua').read_text())
ints=re.findall(r"='(BUILDING_SPC_B058_[^']+)'",(root/'BoostIntegerConfig.lua').read_text())
add('Boost',boosts+ints+[f'BUILDING_SPC_B057_{k}_{a}' for k in ['RESEARCH','CULTURE'] for a in [2,4]])
add('DialogueTests',[f'BUILDING_SPC_B059_TEST{n}' for n in [25,50,100]])
add('GreatWorkProbe',['BUILDING_SPC_B055_GW_CITY','BUILDING_SPC_B055_GW_OBJECT'])
add('PurchaseProbe',['BUILDING_SPC_B053_FIXTURE','BUILDING_SPC_B053_DISCOUNT'])
add('GWARetired',[f'BUILDING_SPC_B060_{y}_{s}{i}' for y in ['FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'] for s in ['P','N'] for i in range(13)])
lim={'SCIENCE':5,'PRODUCTION':10,'GOLD':30,'FOOD':5,'FAITH':5,'CULTURE':10}; pb={'SCIENCE':4,'GOLD':6,'CULTURE':4,'PRODUCTION':4,'FOOD':3,'FAITH':3}
add('Meaning',[f'BUILDING_SPC_MEANING_PROBE_{y}_{i}' for y,n in pb.items() for i in range(n)]+['BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3','BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3_SCALE100','BUILDING_SPC_MEANING_PROBE_PRODUCTION_SINGLE3']+[f'BUILDING_SPC_MEANING_PROBE_{y}_VALUE_{a}' for y,n in lim.items() for a in range(1,n+1)])
add('Aesthetic',['BUILDING_SPC_CULTURE_AESTHETIC'])
add('Inspiration',[f'BUILDING_SPC_INSPIRE_PROBE_{v}' for v in [1,3,6,10]])
add('Claim',[f'BUILDING_SPC_CLAIM_{k}' for k in ['RESEARCH','CULTURE','INDUSTRY','COMMERCE']])
add('Convergence',[f'BUILDING_SPC_B061_{y}_{i}' for y in ['SCIENCE','CULTURE','PRODUCTION'] for i in range(16)])
expected=set().union(*F.values()); ty={x[0]:x[1:] for x in q('SELECT Type,Kind,_file FROM Types')}; bu={x[0]:x[1:] for x in q('SELECT BuildingType,InternalOnly,_file FROM Buildings')}
wrong=[(n,ty.get(n),bu.get(n)) for n in sorted(expected) if n not in ty or n not in bu or ty[n][0]!='KIND_BUILDING' or bu[n][0]!=1]
dup_type=q('SELECT Type,COUNT(*),GROUP_CONCAT(_file) FROM Types GROUP BY Type HAVING COUNT(*)>1');dup_build=q('SELECT BuildingType,COUNT(*),GROUP_CONCAT(_file) FROM Buildings GROUP BY BuildingType HAVING COUNT(*)>1')
ov=[]
for a in F:
 for b in F:
  if a<b and F[a]&F[b]:ov.append((a,b,sorted(F[a]&F[b])))
left=q('SELECT BuildingType,InternalOnly,_file FROM Buildings WHERE BuildingType NOT IN ('+','.join('?' for _ in expected)+')') if False else [(n,*v) for n,v in sorted(bu.items()) if n not in expected]
print(json.dumps({'registered_database_files':len(files),'literal_types':len(ty),'literal_buildings':len(bu),'families':{k:len(v) for k,v in F.items()},'expected_fixed_unique':len(expected),'bad_or_missing':wrong,'duplicates_types':dup_type,'duplicates_buildings':dup_build,'fixed_family_overlaps':ov,'dynamic_type_building_statements':dynamic,'literal_buildings_outside_fixed_set':left},ensure_ascii=False,indent=2))
