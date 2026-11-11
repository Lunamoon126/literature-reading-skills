from pathlib import Path
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / 'tests/fixtures'
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
checker = load('check_evidence')
validator = load('validate')

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((FIX / 'expected-evidence.json').read_text(encoding='utf-8'))
    def test_valid(self):
        self.assertEqual(checker.check(self.data, FIX), [])
    def test_missing_evidence(self):
        self.data['claims'][0]['evidence'] = []
        self.assertTrue(checker.check(self.data, FIX))
    def test_unknown_source(self):
        self.data['claims'][0]['evidence'][0]['source_id'] = 'INVENTED'
        self.assertTrue(checker.check(self.data, FIX))
    def test_missing_material_cannot_support_claim(self):
        self.data['sources'][0]['availability'] = 'missing'
        self.assertTrue(checker.check(self.data, FIX))
    def test_duplicate_claim(self):
        self.data['claims'].append(copy.deepcopy(self.data['claims'][0]))
        self.assertTrue(checker.check(self.data, FIX))
    def test_duplicate_source(self):
        self.data['sources'].append(copy.deepcopy(self.data['sources'][0]))
        self.assertTrue(checker.check(self.data, FIX))
    def test_invalid_kind(self):
        self.data['claims'][0]['kind'] = 'scientific-proof'
        self.assertTrue(checker.check(self.data, FIX))
    def test_undeclared_field(self):
        self.data['claims'][0]['fake_doi'] = 'invented'
        self.assertTrue(checker.check(self.data, FIX))
    def test_out_of_range_locator(self):
        self.data['claims'][0]['evidence'][0]['locator'] = 'L999'
        self.assertTrue(checker.check(self.data, FIX))
    def test_empty_locator(self):
        self.data['claims'][0]['evidence'][0]['locator'] = ' '
        self.assertTrue(checker.check(self.data, FIX))
    def test_missing_file(self):
        self.data['sources'][0]['path'] = 'not-supplied.txt'
        self.assertTrue(checker.check(self.data, FIX))
    def test_path_escape(self):
        self.data['sources'][0]['path'] = '../TEST_PLAN.md'
        self.assertTrue(checker.check(self.data, FIX))
    def test_unknown_can_have_no_evidence(self):
        self.data['claims'].append({'claim_id':'C-UNKNOWN','kind':'unknown','text':'Software version unavailable','evidence':[], 'limitations':'Synthetic source does not report it'})
        self.assertEqual(checker.check(self.data, FIX), [])

class PackageTests(unittest.TestCase):
    def test_package(self):
        self.assertEqual(validator.validate(), [])
    def test_negative_broken_link(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'package'
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__'))
            readme = target / 'README.md'
            readme.write_text(readme.read_text(encoding='utf-8')+'\n[bad](missing-target.md)\n', encoding='utf-8')
            self.assertTrue(any('broken link' in e for e in validator.validate(target)))
    def test_frontmatter_duplicate_key(self):
        with self.assertRaises(ValueError):
            validator.frontmatter('---\nname: a\nname: b\n---\n')
    def test_toy_reproduction(self):
        # This is a fixture oracle only; no scientific interpretation.
        count = (FIX / 'toy-input.txt').read_text(encoding='utf-8').split().count('A')
        self.assertEqual(count, 2)

if __name__ == '__main__':
    unittest.main()
