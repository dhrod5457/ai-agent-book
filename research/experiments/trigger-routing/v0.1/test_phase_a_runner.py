import importlib.util
import json
import sys
import unittest
from pathlib import Path

SPEC_H = importlib.util.spec_from_file_location("harness", Path(__file__).with_name("harness.py"))
harness = importlib.util.module_from_spec(SPEC_H)
assert SPEC_H.loader is not None
SPEC_H.loader.exec_module(harness)
sys.modules["harness"] = harness

SPEC_R = importlib.util.spec_from_file_location("phase_a_runner", Path(__file__).with_name("phase_a_runner.py"))
runner = importlib.util.module_from_spec(SPEC_R)
assert SPEC_R.loader is not None
SPEC_R.loader.exec_module(runner)


class PhaseARunnerTests(unittest.TestCase):
    def test_gemini_native_activation(self):
        text = json.dumps({
            "type": "tool_use",
            "name": "activate_skill",
            "arguments": {"name": "bugfix"},
        }) + "\n"
        actual, observable, evidence, body_loaded = runner.extract_result("gemini", text, 0)
        self.assertEqual("bugfix", actual)
        self.assertTrue(observable)
        self.assertEqual("activate_skill:bugfix", evidence)
        self.assertTrue(body_loaded)

    def test_sentinel_fallback(self):
        actual, observable, evidence, body_loaded = runner.extract_result(
            "codex",
            '{"type":"result","text":"SKILL_ACTIVATED:refactor"}\n',
            0,
        )
        self.assertEqual("refactor", actual)
        self.assertTrue(observable)
        self.assertEqual("sentinel:refactor", evidence)
        self.assertTrue(body_loaded)

    def test_claude_absence_is_unobservable(self):
        actual, observable, evidence, body_loaded = runner.extract_result(
            "claude",
            '{"type":"result","result":"no skill"}\n',
            0,
        )
        self.assertEqual("unobservable", actual)
        self.assertFalse(observable)
        self.assertFalse(body_loaded)

    def test_claude_command_uses_safe_mode(self):
        command = runner.build_command("claude", "hello", "claude-opus-x")
        self.assertIn("--permission-mode", command)
        self.assertIn("plan", command)
        self.assertIn("--no-session-persistence", command)


if __name__ == "__main__":
    unittest.main()
