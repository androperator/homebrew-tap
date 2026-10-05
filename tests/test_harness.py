"""Keep local formula validation unlinked and exercise supported brew commands."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HarnessTests(unittest.TestCase):
    def run_harness(self, installed, linked):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            binaries = temp / 'bin'
            binaries.mkdir()
            log = temp / 'calls'
            brew = binaries / 'brew'
            brew.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
with open(os.environ['MOCK_LOG'], 'a') as output:
    output.write(json.dumps(args) + '\\n')
if args == ['--repository']:
    print(os.environ['MOCK_REPOSITORY'])
elif args[:2] == ['list', '--versions']:
    sys.exit(0 if os.environ['MOCK_INSTALLED'] == 'yes' else 1)
elif args[:2] == ['info', '--json=v2']:
    print(json.dumps({'formulae': [{'linked_keg': '0.1.1' if os.environ['MOCK_LINKED'] == 'yes' else ''}]}))
elif args[0] == 'reinstall' and '--skip-link' in args:
    sys.exit(99)
''')
            brew.chmod(0o755)
            ruby = binaries / 'ruby'
            ruby.write_text('#!/bin/sh\nexit 0\n')
            ruby.chmod(0o755)
            result = subprocess.run(['bash', str(ROOT / 'scripts/test-formulae.sh')],
                                    env={**os.environ, 'PATH': f'{binaries}:{os.environ["PATH"]}',
                                         'MOCK_LOG': str(log), 'MOCK_REPOSITORY': str(temp / 'brew'),
                                         'MOCK_INSTALLED': 'yes' if installed else 'no',
                                         'MOCK_LINKED': 'yes' if linked else 'no'},
                                    capture_output=True, text=True)
            return result, [json.loads(line) for line in log.read_text().splitlines()]

    def test_fresh_installations_are_unlinked_and_tests_accept_unlinked_formulae(self):
        result, calls = self.run_harness(False, False)
        self.assertEqual(result.returncode, 0, result.stderr)
        installs = [args for args in calls if args[0] == 'install']
        self.assertEqual(len(installs), 2)
        self.assertTrue(all('--skip-link' in args for args in installs))
        self.assertTrue(all('--force' in args for args in calls if args[0] == 'test'))

    def test_unlinked_reinstall_does_not_pass_unsupported_install_flag(self):
        result, calls = self.run_harness(True, False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sum(args[0] == 'reinstall' for args in calls), 2)

    def test_linked_installation_is_refused_before_any_package_mutation(self):
        result, calls = self.run_harness(True, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Refusing to test linked', result.stderr)
        self.assertFalse(any(args[0] in ('install', 'reinstall', 'test') for args in calls))
