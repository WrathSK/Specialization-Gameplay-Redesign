"""Conservative review alarms, not a Lua semantic proof. New/widened occurrences fail baseline comparison."""
from collections import Counter
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
MISSING=('CityBuildQueueChanged','CityBuildingsChanged','CityConquered','CityYieldChanged','CityYieldsChanged','PlayerTurnStartComplete','TradeRoutePlundered','BuildingPillaged','BuildingRepaired','DistrictRepaired')

def scan(root=ROOT):
    alarms=[]
    for path in sorted((root/'Mod').rglob('*.lua')):
        text=path.read_text();relative=str(path.relative_to(root));lines=text.splitlines()
        # String appearances are review candidates: a static scan cannot prove native registration/signature.
        for event in MISSING:
            for match in re.finditer(r"['\"]"+event+r"['\"]",text):
                line=text[:match.start()].count('\n')+1
                context='\n'.join(lines[max(0,line-3):min(len(lines),line+2)])
                if any(word in context for word in ('hook','Hook','.Add','ipairs')):
                    alarms.append({'rule':'MEASURED_MISSING_EVENT','path':relative,'line':line,'detail':event,'confidence':'REVIEW'})
        if 'function data.Audit(scope)' in text and 'for _,c in cities:Members()' in text:
            alarms.append({'rule':'SCOPED_WRAPPER_PLAYER_LOOP','path':relative,'line':1,'detail':'review actual city filtering, not wrapper signature','confidence':'REVIEW'})
        if not relative.startswith('Mod/UI/'):
            for m in re.finditer(r'(?:shared|s)\.DistrictCompleteness\.Read\(',text):
                alarms.append({'rule':'DETAIL_READER_BUSINESS','path':relative,'line':text[:m.start()].count('\n')+1,'detail':'review summary/detail caller closure','confidence':'REVIEW'})
        for i,line in enumerate(lines,1):
            if 'GameCoreEventPublishComplete' in line and any(x in line for x in ('FlushPending','Retry','Pulse')):
                alarms.append({'rule':'PUBLISH_PENDING_BUDGET','path':relative,'line':i,'detail':'review progress/attempt budget','confidence':'REVIEW'})
        if ':SetProperty(' in text or 'P.SetProperty(' in text:
            alarms.append({'rule':'PROPERTY_PRODUCER_OWNERSHIP','path':relative,'line':1,'detail':'review declared invalidation/exit ownership','confidence':'REVIEW'})
    return alarms

def counts(alarms):
    return dict(sorted(Counter(row['path']+'|'+row['rule'] for row in alarms).items()))

def check(selection,root=ROOT):
    rows=scan(root);current=counts(rows);baseline=selection['static_alarm_baseline']
    widened={key:{'before':baseline.get(key,0),'after':value}for key,value in current.items()if value>baseline.get(key,0)}
    return {'status':'FAIL_NEW_OR_WIDENED_ALARM'if widened else 'PASS_NO_NEW_ALARMS','widened':widened,'alarms':rows,
      'limits':'REVIEW alarms are not proof of dead hooks, scope discard, missing budgets or invalid ownership. Human caller review and targeted tests remain mandatory.'}

if __name__=='__main__':
    selection=json.loads(Path(__file__).with_name('refactor_selection.json').read_text());result=check(selection);print(json.dumps(result,indent=2));raise SystemExit(bool(result['widened']))
