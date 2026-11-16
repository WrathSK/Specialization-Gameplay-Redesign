#!/usr/bin/env python3
"""Read frozen official/HD databases for assembly review; never infer approved Tier.

Output is regenerable local evidence, not a runtime catalog or native PASS.
No external packages. SQLite connections use mode=ro and immutable snapshots.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3

WRAPPERS = (
    'MODIFIER_CITY_ADJUST_BUILDING_PURCHASE_COST',
    'MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE',
    'MODIFIER_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION',
)

def digest(path):
    with path.open('rb') as stream:
        h = hashlib.sha256()
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def inspect(path):
    before = digest(path)
    with sqlite3.connect(path.as_uri() + '?mode=ro&immutable=1', uri=True) as db:
        db.row_factory = sqlite3.Row
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required = {'Buildings', 'BuildingPrereqs', 'BuildingReplaces', 'DistrictReplaces', 'DynamicModifiers'}
        if not required <= tables:
            raise ValueError('Required schema missing: ' + ','.join(sorted(required - tables)))
        check = [r[0] for r in db.execute('PRAGMA quick_check')]
        if check != ['ok']:
            raise ValueError('Database quick_check failed')
        def rows(sql, args=()):
            return [dict(r) for r in db.execute(sql, args)]
        buildings = rows('SELECT BuildingType, PrereqDistrict, InternalOnly, IsWonder, MustPurchase, '
                         'EnabledByReligion, GovernmentTierRequirement FROM Buildings ORDER BY BuildingType')
        prereqs = rows('SELECT Building, PrereqBuilding FROM BuildingPrereqs ORDER BY Building,PrereqBuilding')
        replacements = rows('SELECT * FROM BuildingReplaces ORDER BY CivUniqueBuildingType,ReplacesBuildingType')
        districts = rows('SELECT * FROM DistrictReplaces ORDER BY CivUniqueDistrictType,ReplacesDistrictType')
        names = {r['BuildingType'] for r in buildings}
        missing = [r for r in prereqs if r['Building'] not in names or r['PrereqBuilding'] not in names]
        wrappers = {name: rows('SELECT * FROM DynamicModifiers WHERE ModifierType=?', (name,)) for name in WRAPPERS}
        old = rows('SELECT * FROM HD_BuildingTiers ORDER BY BuildingType') if 'HD_BuildingTiers' in tables else None
        dummy = rows('SELECT * FROM HD_DUMMY_BUILDINGS ORDER BY BuildingType') if 'HD_DUMMY_BUILDINGS' in tables else None
        result = dict(sha256=before, quick_check=check, buildings=buildings,
                      prerequisites=prereqs, replacements=replacements, district_replacements=districts,
                      missing_prerequisite_rows=missing, legacy_hd_tiers=old, legacy_hd_dummy=dummy,
                      wrapper_definitions=wrappers)
    if digest(path) != before:
        raise ValueError('Input snapshot changed during inspection')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--official-db', type=Path, required=True)
    parser.add_argument('--hd-db', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='New local JSON file; existing files are never overwritten')
    args = parser.parse_args()
    paths = [p.expanduser().resolve(strict=True) for p in (args.official_db, args.hd_db)]
    output = args.output.expanduser().resolve()
    if paths[0] == paths[1] or output in paths:
        raise ValueError('Independent inputs and separate output required')
    result = {'schema': 1, 'evidence': 'STATIC_DATABASE_OBSERVATION_NOT_NATIVE_EFFECT_PASS',
              'official': inspect(paths[0]), 'hd': inspect(paths[1])}
    if result['official']['legacy_hd_tiers'] is not None:
        raise ValueError('Official baseline contains HD tier table')
    if result['hd']['legacy_hd_tiers'] is None:
        raise ValueError('HD comparison lacks HD tier table')
    with output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'output_sha256': digest(output), 'profiles': {
        name: {'buildings': len(result[name]['buildings']),
               'prerequisites': len(result[name]['prerequisites']),
               'missing_prerequisite_rows': len(result[name]['missing_prerequisite_rows'])}
        for name in ('official', 'hd')}}, sort_keys=True))

if __name__ == '__main__':
    main()
