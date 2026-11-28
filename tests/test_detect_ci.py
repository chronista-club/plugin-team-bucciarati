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

    def test_mise_formal_tasks_included_when_no_aggregate_check(self):
        result = self.detect(['lint', 'test', 'formal:lean', 'formal:quint', 'formal:aeneas'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout)['commands'],
            ['mise run lint', 'mise run test', 'mise run formal:lean', 'mise run formal:quint', 'mise run formal:aeneas'],
        )

    def test_formal_directory_detected_alongside_cargo(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'Cargo.toml').write_text('[package]\nname = "demo"\nversion = "0.1.0"\n')
            (root / 'formal/lean').mkdir(parents=True)
            (root / 'formal/lean/Core.lean').write_text('theorem t : True := trivial\n')
            (root / 'formal/quint').mkdir(parents=True)
            (root / 'formal/quint/check.ts').write_text('// quint runner\n')
            (root / 'formal/aeneas').mkdir(parents=True)
            (root / 'formal/aeneas/check.ts').write_text('// aeneas runner\n')
            result = subprocess.run(
                ['bash', str(ROOT / 'scripts/detect-ci.sh'), str(root)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            cmds = json.loads(result.stdout)['commands']
            self.assertIn('lean -DwarningAsError=true formal/lean/Core.lean', cmds)
            self.assertIn('bun formal/quint/check.ts', cmds)
            self.assertIn('bun formal/aeneas/check.ts', cmds)

    def test_mise_without_aggregate_check_falls_back_to_formal_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'mise.toml').write_text('')
            shim = root / 'mise'
            shim.write_text("#!/bin/sh\ncat <<'TASKS'\n" + json.dumps([{'name': 'lint'}, {'name': 'test'}]) + "\nTASKS\n")
            shim.chmod(0o755)
            (root / 'formal/lean').mkdir(parents=True)
            (root / 'formal/lean/Core.lean').write_text('theorem t : True := trivial\n')
            (root / 'formal/quint').mkdir(parents=True)
            (root / 'formal/quint/check.ts').write_text('// quint runner\n')
            result = subprocess.run(
                ['bash', str(ROOT / 'scripts/detect-ci.sh'), str(root)],
                env={**os.environ, 'PATH': str(root) + os.pathsep + os.environ['PATH']},
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload['runner'], 'mise')
            self.assertEqual(
                payload['commands'],
                ['mise run lint', 'mise run test', 'lean -DwarningAsError=true formal/lean/Core.lean', 'bun formal/quint/check.ts'],
            )

    def test_standalone_formal_repo_and_empty_lean_dir(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'formal/lean').mkdir(parents=True)
            (root / 'formal/quint').mkdir(parents=True)
            (root / 'formal/quint/check.ts').write_text('// quint runner\n')
            result = subprocess.run(
                ['bash', str(ROOT / 'scripts/detect-ci.sh'), str(root)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload['runner'], 'formal')
            self.assertEqual(payload['commands'], ['bun formal/quint/check.ts'])
