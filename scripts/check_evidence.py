"""Offline structural validation; never a scientific truth evaluator."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / '.agents/skills/_literature-shared/references/evidence-schema.json'

def schema_errors(value, schema, where='$'):
    errors = []
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str}
    if kind and not isinstance(value, types[kind]):
        return [f'{where}: expected {kind}']
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{where}: invalid enum')
    if isinstance(value, str) and len(value.strip()) < schema.get('minLength', 0):
        errors.append(f'{where}: empty string')
    if kind == 'object':
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{where}: missing {key}')
        props = schema.get('properties', {})
        for key, item in value.items():
            if key in props:
                errors += schema_errors(item, props[key], f'{where}.{key}')
            elif schema.get('additionalProperties') is False:
                errors.append(f'{where}: unexpected {key}')
    elif kind == 'array':
        for i, item in enumerate(value):
            errors += schema_errors(item, schema['items'], f'{where}[{i}]')
    return errors

def check(data, base=ROOT):
    errors = schema_errors(data, json.loads(SCHEMA.read_text(encoding='utf-8')))
    if errors:
        return errors
    base = Path(base).resolve()
    sources = {}
    for source in data['sources']:
        sid = source['source_id']
        if sid in sources:
            errors.append(f'duplicate source_id: {sid}')
        sources[sid] = source
        path = (base / source['path']).resolve()
        if not path.is_relative_to(base):
            errors.append(f'{sid}: path escapes base')
        elif source['availability'] == 'provided' and not path.is_file():
            errors.append(f'{sid}: provided source does not exist')
    seen = set()
    for claim in data['claims']:
        cid = claim['claim_id']
        if cid in seen:
            errors.append(f'duplicate claim_id: {cid}')
        seen.add(cid)
        if claim['kind'] in ('reported', 'observed', 'inference') and not claim['evidence']:
            errors.append(f'{cid}: factual or inference claim requires evidence')
        for evidence in claim['evidence']:
            sid = evidence['source_id']
            source = sources.get(sid)
            if not source:
                errors.append(f'{cid}: unknown source_id {sid}')
            elif source['availability'] != 'provided':
                errors.append(f'{cid}: cited source is missing')
            elif re.fullmatch(r'L\d+(?:-L\d+)?', evidence['locator']):
                path = (base / source['path']).resolve()
                if path.is_relative_to(base) and path.is_file():
                    try:
                        lines = path.read_text(encoding='utf-8').splitlines()
                        nums = [int(n) for n in re.findall(r'\d+', evidence['locator'])]
                        if min(nums) < 1 or max(nums) > len(lines) or nums != sorted(nums):
                            errors.append(f'{cid}: locator outside source text')
                    except UnicodeError:
                        errors.append(f'{cid}: line locator requires UTF-8 text')
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    parser.add_argument('--base', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        errors = check(json.loads(args.ledger.read_text(encoding='utf-8')), args.base)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    for error in errors:
        print('ERROR:', error)
    if not errors:
        print('PASS: evidence structure and resolvable references; semantic review still required')
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
