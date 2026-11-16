# Reproduction Method and Evidence Limits

Investigation / Non-authoritative / No design decision implied

Status: Stable

Maintainer: Primary. Source baseline: `3d0ac4b4c2b1c3d71cb46beb7d1093d191ade795`.

## Scope of executed validation

Executed with Python's standard library, no third-party dependency: parse the current manifest; lex all65 Mod SQL sources; split multi-value INSERT tuples outside strings/comments/parentheses; count literal primary keys and composite argument/attachment keys; check the literal declaration graph; mechanically construct the three catalog-independent ranges and check their matching ID graph. SQL SELECT statements are disclosed separately, not incorrectly counted as one row or ignored. No generator, source SQL or gameplay simulation was executed.

Observed output:44 gameplay UpdateDatabase actions /49 unique SQL;4,181 literal unique Modifiers /1,790 Buildings /1,836 Types;4,420 /2,013 /2,059 after fixed-range expansions. Literal graph checks and fixed ID graph checks pass; no source primary/composite duplicates. This is **STATIC_CONFIRMED** source evidence, not LOCAL_SIMULATION_PASS for gameplay or a native/DB load PASS.

The source set and manifest fingerprints match [Definition_Inventory](Definition_Inventory.md#inventory-fingerprint). Git/source versions are baseline-specific; future source changes require rerunning, not copying these totals. Temporary working output is not a permanent backup. This Markdown preserves the executable procedure and concise results, not a full generated Closure snapshot.

## Reproduce the source-only result

Save the code block to a temporary file **outside the repository**, then run it with Python3.10+ from the repository root. It opens repository sources read-only and writes only to stdout. No current database is required. The lexer deliberately fails on unsupported literal expressions rather than guessing. The three fixed expansions are explicit, source-bound derivations; all other INSERT SELECT populations remain symbolic and must use the separate formulas/database queries. It is an audit snippet, not a new formal tool or universal SQL parser.

```python
"""Read-only SQL declaration inventory. No external DB access; no SQL writes.
Run from the repository root. Generated INSERT SELECT populations are reported,
not guessed. Source statements are lexed, not counted by lines/grep.
"""
from pathlib import Path
import re,json,hashlib,xml.etree.ElementTree as ET

def clean(src):
    out=[];i=0;q=None
    while i<len(src):
        c=src[i]
        if q:
            out.append(c)
            if c==q:
                if i+1<len(src) and src[i+1]==q:out.append(src[i+1]);i+=1
                else:q=None
            i+=1;continue
        if c in "'\"`":q=c;out.append(c);i+=1;continue
        if src.startswith('--',i):
            j=src.find('\n',i);i=len(src) if j<0 else j;continue
        if src.startswith('/*',i):
            j=src.find('*/',i+2);i=len(src) if j<0 else j+2;out.append(' ');continue
        out.append(c);i+=1
    return ''.join(out)

def split(s,sep=','):
    out=[];start=0;depth=0;i=0;q=None
    while i<len(s):
        c=s[i]
        if q:
            if c==q:
                if i+1<len(s) and s[i+1]==q:i+=1
                else:q=None
        elif c in "'\"`":q=c
        elif c=='(':depth+=1
        elif c==')':depth-=1
        elif c==sep and depth==0:out.append(s[start:i].strip());start=i+1
        i+=1
    if s[start:].strip():out.append(s[start:].strip())
    return out

def literal(s):
    s=s.strip()
    if s[:1]=="'" and s[-1:]=="'":return s[1:-1].replace("''", "'")
    if s.upper()=='NULL':return None
    if re.fullmatch(r'[-+]?\d+(?:\.\d+)?',s):return float(s) if '.' in s else int(s)
    raise ValueError('Nonliteral VALUES expression: '+s[:60])

def parse(p):
    tables={};dynamic=[]
    for st in split(clean(p.read_text()),';'):
        m=re.match(r'INSERT(?:\s+OR\s+\w+)?\s+INTO\s+([\w]+)\s*(\([^)]*\))?\s*VALUES\s*(.*)$',st,re.S|re.I)
        if not m:
            if re.search(r'\bINSERT(?:\s+OR\s+\w+)?\s+INTO\b',st,re.I):dynamic.append(st)
            continue
        t,cols,tail=m.groups();columns=[x.strip().lower() for x in cols[1:-1].split(',')] if cols else None
        for row in split(tail):
            assert row.startswith('(') and row.endswith(')'),(p,row[:60])
            v=[literal(x) for x in split(row[1:-1])]
            tables.setdefault(t.lower(),[]).append(dict(zip(columns,v)) if columns else {'$values':v})
    return tables,dynamic

def inventory(root):
    manifest=ET.parse(root/'Mod/SpecializationP0.modinfo').getroot();loaded=[]
    for scope in ('FrontEndActions','InGameActions'):
        for a in manifest.find(scope):
            if a.tag=='UpdateDatabase':
                for f in a.findall('File'):
                    loaded.append({'scope':scope,'action':a.get('id'),'order':int(a.findtext('Properties/LoadOrder','0')),'path':f.text,'criteria':a.findtext('Criteria')})
    files={};allrows={}
    for p in sorted((root/'Mod').rglob('*.sql')):
        rows,dyn=parse(p);path=str(p.relative_to(root/'Mod'))
        files[path]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'lines':len(p.read_text().splitlines()),'literal':{t:len(rs) for t,rs in rows.items()},'dynamic':dyn,'rows':rows}
        if any(x['scope']=='InGameActions' and x['path']==path for x in loaded):
            for t,rs in rows.items():allrows.setdefault(t,[]).extend(rs)
    return {'loaded':loaded,'files':files,'allrows':allrows}

# Catalog-independent INSERT SELECT expansion, mechanically derived from source
# ranges. No SQL is executed. Catalog-dependent statements remain symbolic.
def fixed_expansion(data):
    files=data['files'];out={k:list(v) for k,v in data['allrows'].items()}
    for p,needle in [('Data/Commerce.sql','Bit<30'),('Data/CultureInsightsTourism.sql','n<192')]:
        assert needle in clean(Path('Mod',p).read_text()),'Source range changed: '+p
    bits=files['Data/CultureAesthetic.sql']['rows']['spc_cultureaestheticbits']
    assert len(bits)==16 and [x['$values'][0] for x in bits]==list(range(16))
    for prefix,n in [('BUILDING_SPC_COMMERCE_GOLD_',31),('BUILDING_SPC_INSIGHT_TOURISM_',192)]:
        for bit in range(n):
            name=prefix+str(bit);mid=name if 'COMMERCE' in name else name.removeprefix('BUILDING_')
            for table,row in [('buildings',{'buildingtype':name,'internalonly':1}),('types',{'type':name,'kind':'KIND_BUILDING'}),('modifiers',{'modifierid':mid}),('buildingmodifiers',{'buildingtype':name,'modifierid':mid})]:out.setdefault(table,[]).append(row)
    for bit in range(16):
        mid='SPC_CULTURE_AESTHETIC_'+str(bit)
        for table,row in [('modifiers',{'modifierid':mid,'subjectrequirementsetid':mid+'_SET'}),('buildingmodifiers',{'buildingtype':'BUILDING_SPC_CULTURE_AESTHETIC','modifierid':mid}),('requirements',{'requirementid':mid+'_REQ'}),('requirementsets',{'requirementsetid':mid+'_SET'})]:out.setdefault(table,[]).append(row)
    for t,k in [('modifiers','modifierid'),('buildings','buildingtype'),('types','type'),('requirements','requirementid'),('requirementsets','requirementsetid')]:
        ids=[x[k] for x in out[t]];assert len(ids)==len(set(ids)),(t,'duplicate');print('FIXED_EXPANDED',t,len(ids))
    return out

if __name__ == '__main__':
    root=Path.cwd();data=inventory(root);rows=data['allrows']
    print('SQL_FILES',len(data['files']))
    selected=[x for x in data['loaded'] if x['scope']=='InGameActions']
    print('IG_ACTIONS',len({x['action'] for x in selected}),'IG_FILES',len(selected))
    digest=hashlib.sha256()
    for path,f in sorted(data['files'].items()):
        digest.update((path+'\0'+f['sha256']+'\n').encode())
    print('SQL_DIGEST',digest.hexdigest())
    print('MANIFEST_DIGEST',hashlib.sha256((root/'Mod/SpecializationP0.modinfo').read_bytes()).hexdigest())
    for load in sorted(selected,key=lambda x:x['path']):
        f=data['files'][load['path']]
        print(load['path'],load['order'],f['literal'],'UNRESOLVED_INSERT_SELECT',len(f['dynamic']))
    for table,key in [('modifiers','modifierid'),('buildings','buildingtype'),('types','type'),('requirements','requirementid'),('requirementsets','requirementsetid'),('units','unittype')]:
        ids=[x[key] for x in rows[table]]
        assert len(ids)==len(set(ids)),('duplicate ID',table)
        print('LITERAL_UNIQUE',table,len(ids))
    def links(rs):
        for ft,col,tt,key in [('modifierarguments','modifierid','modifiers','modifierid'),('buildingmodifiers','modifierid','modifiers','modifierid'),('buildingmodifiers','buildingtype','buildings','buildingtype'),('buildings','buildingtype','types','type'),('requirementarguments','requirementid','requirements','requirementid'),('requirementsetrequirements','requirementid','requirements','requirementid'),('requirementsetrequirements','requirementsetid','requirementsets','requirementsetid'),('traitmodifiers','modifierid','modifiers','modifierid')]:
            target={x[key] for x in rs.get(tt,[])}
            missing={x[col] for x in rs.get(ft,[]) if x[col] not in target}
            assert not missing,(ft,col,missing)
        sets={x['requirementsetid'] for x in rs['requirementsets']}
        for row in rs['modifiers']:
            for col in ('ownerrequirementsetid','subjectrequirementsetid'):
                assert not row.get(col) or row[col] in sets,(col,row)
    links(rows)
    for table,keys in [('modifierarguments',('modifierid','name')),('buildingmodifiers',('buildingtype','modifierid')),('requirementarguments',('requirementid','name')),('requirementsetrequirements',('requirementsetid','requirementid')),('traitmodifiers',('traittype','modifierid'))]:
        ids=[tuple(x[k] for k in keys) for x in rows[table]]
        assert len(ids)==len(set(ids)),('duplicate pair',table)
    expanded=fixed_expansion(data);links(expanded)
    print('SOURCE_GRAPH_CHECKS_PASS; SELECT-dependent native/HD references NOT_RUN')

```

The `rows` subtotal is specifically the literal VALUES population. The expanded graph checks do not execute recursive SQL, resolve native engine EffectTypes or prove the dynamic families' foreign keys. BuildingModifiers and modifier instances are not interchangeable counts.

## Resolve effective-loaded counts when a current database is available

**NOT_RUN this session:** `SPC_DEBUG_GAMEPLAY_DB` and ignored `local/config.json:debug_gameplay_db` were unavailable. A non-SPC legacy application cache is not a replacement for a current HD/SPC database. No configuration was created, inferred or edited; no database copied into the repository. This missing input is an evidence prerequisite, not a new gameplay decision.

Use the existing `DevelopmentTests/project_paths.py:5` resolver. Open with SQLite URI `mode=ro`; set `PRAGMA query_only=ON`; perform only SELECT/PRAGMA reads. Record its hash (including relevant WAL identity if present), source/deployment receipt and loaded-mod/error evidence separately; a database timestamp or matching row count alone cannot prove which runtime executed. Never run source SQL on the original database. The following queries are a future read-only audit procedure, not results obtained here.

```python
from pathlib import Path
import sqlite3,sys
root=Path.cwd()
sys.path.insert(0,str(root/'DevelopmentTests'))
from project_paths import external_database
path=external_database(root)
db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
db.execute('PRAGMA query_only=ON')
# Scope is the reserved SPC source namespace, not all mods' rows.
owned_m="(ModifierId GLOB 'SPC_*' OR ModifierId GLOB 'BUILDING_SPC_*')"
queries={
 'owned_modifiers':f'SELECT COUNT(DISTINCT ModifierId) FROM Modifiers WHERE {owned_m}',
 'internal_buildings':"SELECT COUNT(DISTINCT BuildingType) FROM Buildings WHERE BuildingType GLOB 'BUILDING_SPC_*' AND InternalOnly=1",
 'E':'SELECT COUNT(*) FROM Eras',
 'B':'SELECT COUNT(DISTINCT BuildingType) FROM SPC_B054_Targets',
 'D':"SELECT COUNT(*) FROM SPC_StandardizationTargets WHERE Kind='DISTRICT'",
 'C':'SELECT COUNT(*) FROM SPC_ResearchChairTargets',
 'R':'SELECT COUNT(*) FROM SPC_DevelopmentEffects',
 'Y':"SELECT COUNT(*) FROM Yields WHERE YieldType<>'YIELD_FOOD'",
 'Q':"SELECT COUNT(*) FROM Requirements WHERE RequirementId GLOB 'SPC_CROSS_DISTRICT_*'",
 'S':"SELECT COUNT(*) FROM Types WHERE Kind='KIND_PROJECT' AND Type GLOB 'PROJECT_SPC_CREW_*_S[0-9]*'",
 'missing_argument_modifier':"SELECT COUNT(*) FROM ModifierArguments a LEFT JOIN Modifiers m ON m.ModifierId=a.ModifierId WHERE (a.ModifierId GLOB 'SPC_*' OR a.ModifierId GLOB 'BUILDING_SPC_*') AND m.ModifierId IS NULL",
 'missing_link_modifier':"SELECT COUNT(*) FROM BuildingModifiers b LEFT JOIN Modifiers m ON m.ModifierId=b.ModifierId WHERE b.BuildingType GLOB 'BUILDING_SPC_*' AND m.ModifierId IS NULL",
 'missing_link_building':"SELECT COUNT(*) FROM BuildingModifiers bm LEFT JOIN Buildings b ON b.BuildingType=bm.BuildingType WHERE bm.BuildingType GLOB 'BUILDING_SPC_*' AND b.BuildingType IS NULL",
 'missing_building_type':"SELECT COUNT(*) FROM Buildings b LEFT JOIN Types t ON t.Type=b.BuildingType AND t.Kind='KIND_BUILDING' WHERE b.BuildingType GLOB 'BUILDING_SPC_*' AND t.Type IS NULL",
 'missing_requirement':"SELECT COUNT(*) FROM RequirementSetRequirements r LEFT JOIN Requirements q ON q.RequirementId=r.RequirementId WHERE r.RequirementSetId GLOB 'SPC_*' AND q.RequirementId IS NULL",
 'missing_requirement_set':"SELECT COUNT(*) FROM RequirementSetRequirements r LEFT JOIN RequirementSets s ON s.RequirementSetId=r.RequirementSetId WHERE r.RequirementSetId GLOB 'SPC_*' AND s.RequirementSetId IS NULL",
 'missing_requirement_argument_owner':"SELECT COUNT(*) FROM RequirementArguments a LEFT JOIN Requirements r ON r.RequirementId=a.RequirementId WHERE a.RequirementId GLOB 'SPC_*' AND r.RequirementId IS NULL",
 'missing_owner_set':f"SELECT COUNT(*) FROM Modifiers WHERE {owned_m} AND OwnerRequirementSetId IS NOT NULL AND OwnerRequirementSetId NOT IN (SELECT RequirementSetId FROM RequirementSets)",
 'missing_subject_set':f"SELECT COUNT(*) FROM Modifiers WHERE {owned_m} AND SubjectRequirementSetId IS NOT NULL AND SubjectRequirementSetId NOT IN (SELECT RequirementSetId FROM RequirementSets)",
 'missing_trait_modifier':"SELECT COUNT(*) FROM TraitModifiers t LEFT JOIN Modifiers m ON m.ModifierId=t.ModifierId WHERE t.TraitType GLOB 'TRAIT_*SPC*' AND m.ModifierId IS NULL",
}
try:
    for label,query in queries.items():
        print(label,db.execute(query).fetchone()[0])
finally:
    db.close()
```

The namespace query includes legacy and experiments, not only production. Compare exact IDs and family totals with the source inventory; any extra external SPC-namespace rows need attribution rather than silently counting them as this package. Check native ModifierType→DynamicModifiers/Types and native target/RequirementType existence separately against the loaded schema. Full `PRAGMA foreign_key_check` may expose unrelated HD/base issues; scope attributable failures explicitly. Do not falsely report a global database PASS from these bounded joins.

Stable building IDs can survive while graph details change; neither the SELECT counts nor source graph checks prove native save serialization/removal compatibility. Activity requires an already available installed-instance census or a separately authorized native experiment. None was added here.

## Review record and exclusions

Three bounded parallel source reviews covered Boost/Copy compatibility, Great Work/Probe productionization, and remaining generated families/scaling. Primary reconciled their counts and independently checked source formulas and reference graphs. Draft review corrected the DistrictPrecision packaging wording, distinguished attached effects from positive numeric values, and kept historical native failures separate from present ability acceptance. Raw intermediate data, original databases/logs/screenshots and private absolute paths are not report artifacts.

No source/SQL/generator/manifest/test/config/Architecture/Design/Status/Workflow edits; no gameplay test, benchmark, collector change, new probe, PR, main promotion, deployment or game launch. Existing historical reports and v3 artifacts stay unchanged. Only this topic's new Markdown is eligible for reviewed publication.
