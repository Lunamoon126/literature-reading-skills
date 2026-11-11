"""Validate package structure, Markdown and constrained frontmatter; optional full YAML."""
from pathlib import Path
import argparse
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['literature-screening', 'literature-deep-reading', 'literature-method-reproduction']

def frontmatter(text):
    # Package frontmatter intentionally uses only plain keys + quoted strings.
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('missing opening frontmatter')
    end = lines.index('---', 1)
    out = {}
    for line in lines[1:end]:
        match = re.fullmatch(r'([a-z_]+): (.+)', line)
        if not match:
            raise ValueError(f'unsupported frontmatter syntax: {line}')
        key, value = match.groups()
        if key in out:
            raise ValueError(f'duplicate key: {key}')
        if value.startswith('"'):
            value = json.loads(value)
        elif not re.fullmatch(r'[a-z0-9-]+', value):
            raise ValueError(f'unsupported scalar: {key}')
        out[key] = value
    return out

def validate(root=ROOT, full_yaml=False):
    root = Path(root)
    errors = []
    required = ['README.md', 'research-profile.yaml', 'knowledge-base/README.md',
                'knowledge-base/index.csv', 'tests/TEST_PLAN.md', 'scripts/check_evidence.py',
                '.agents/skills/_literature-shared/references/evidence-schema.json']
    for rel in required:
        if not (root / rel).is_file():
            errors.append(f'missing {rel}')
    skills = sorted(p.parent.name for p in (root / '.agents/skills').glob('*/SKILL.md'))
    if skills != sorted(NAMES):
        errors.append('expected exactly three named skills')
    for name in NAMES:
        path = root / '.agents/skills' / name / 'SKILL.md'
        if not path.is_file():
            continue
        try:
            meta = frontmatter(path.read_text(encoding='utf-8'))
            if meta.get('name') != name or not meta.get('description', '').strip():
                errors.append(f'{name}: invalid name/description')
            if len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
                errors.append(f'{name}: invalid skill name')
        except (ValueError, TypeError) as exc:
            errors.append(f'{path}: {exc}')
    for path in root.rglob('*.md'):
        text = path.read_text(encoding='utf-8')
        fences = [line for line in text.splitlines() if line.startswith('```')]
        if len(fences) % 2:
            errors.append(f'{path}: unmatched code fence')
        if text.startswith('---\n'):
            try:
                frontmatter(text)
            except (ValueError, TypeError) as exc:
                errors.append(f'{path}: {exc}')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'):
                continue
            target = unquote(target.split('#')[0])
            if not (path.parent / target).resolve().exists():
                errors.append(f'{path.relative_to(root)}: broken link {target}')
    for path in root.rglob('*.json'):
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except ValueError as exc:
            errors.append(f'{path}: {exc}')
    if full_yaml:
        try:
            import yaml
            class UniqueLoader(yaml.SafeLoader):
                pass
            def mapping(loader, node):
                result = {}
                for key_node, value_node in node.value:
                    key = loader.construct_object(key_node)
                    if key in result:
                        raise ValueError(f'duplicate YAML key: {key}')
                    result[key] = loader.construct_object(value_node)
                return result
            UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
            for path in root.rglob('*'):
                if path.suffix in ('.yaml', '.yml'):
                    yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader)
                elif path.suffix == '.md':
                    text = path.read_text(encoding='utf-8')
                    if text.startswith('---\n'):
                        yaml.load(text.split('---', 2)[1], Loader=UniqueLoader)
        except (ImportError, ValueError) as exc:
            errors.append(f'full YAML: {exc}')
        except Exception as exc:
            errors.append(f'YAML parsing failed: {exc}')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full-yaml', action='store_true')
    args = parser.parse_args()
    errors = validate(full_yaml=args.full_yaml)
    for error in errors:
        print('ERROR:', error)
    print(f'{"FAIL" if errors else "PASS"}: package static validation; full_yaml={args.full_yaml}')
    sys.exit(bool(errors))
