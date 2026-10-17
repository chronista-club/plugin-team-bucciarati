"""Behavior of command discovery; the external mise CLI is a JSON fixture.
Task: mem_1Cfv9MWjUrXiHT8SMVVpaE"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DetectCI(unittest.TestCase):
    def detect(self, names, *, fail=False, payload=None, shell="bash"):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'mise.toml').write_text('')
            shim = root / 'mise'
            data = payload if payload is not None else json.dumps([{'name': n} for n in names])
            shim.write_text('#!/bin/sh\n' + ('echo discovery-failed >&2\nexit 7\n' if fail else
                            "cat <<'TASKS'\n" + data + '\nTASKS\n'))
            shim.chmod(0o755)
            return subprocess.run([shell, str(ROOT / 'scripts/detect-ci.sh'), str(root)],
                                  env={**os.environ, 'PATH': str(root) + os.pathsep + os.environ['PATH']},
                                  text=True, capture_output=True)

    def test_aggregate_check_keeps_project_validation_and_avoids_duplicates(self):
        result = self.detect(['check', 'validate', 'sync-check', 'lint', 'test'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['commands'], ['mise run check'])

    def test_individual_tasks_when_no_aggregate(self):
        result = self.detect(['test', 'lint', 'deploy'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['commands'], ['mise run lint', 'mise run test'])

    def test_no_known_tasks_does_not_invent_test(self):
        result = self.detect(['deploy'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['commands'], [])

    def test_discovery_failure_is_not_success(self):
        result = self.detect([], fail=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('mise', result.stderr)

    def test_invalid_schema_is_not_success(self):
        for payload in ['not-json', '{}', '[{}]', '[{"name":42}]']:
            with self.subTest(payload=payload):
                result = self.detect([], payload=payload)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')

    def test_empty_tasks_on_system_bash(self):
        result = self.detect([], shell='/bin/bash')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['commands'], [])
