import importlib.util
import sys
import unittest
from pathlib import Path

SPEC_S = importlib.util.spec_from_file_location(
    "scope_harness", Path(__file__).with_name("scope_harness.py")
)
scope = importlib.util.module_from_spec(SPEC_S)
assert SPEC_S.loader is not None
SPEC_S.loader.exec_module(scope)
sys.modules["scope_harness"] = scope

SPEC_R = importlib.util.spec_from_file_location(
    "phase_b_runner", Path(__file__).with_name("phase_b_runner.py")
)
runner = importlib.util.module_from_spec(SPEC_R)
assert SPEC_R.loader is not None
SPEC_R.loader.exec_module(runner)


class PhaseBRunnerTests(unittest.TestCase):
    def test_claude_command_locks_agents_md_and_permissions(self):
        command = runner.build_command("claude", "task", "claude-sonnet-5")
        joined = " ".join(command)
        self.assertIn("--permission-mode acceptEdits", joined)
        self.assertIn("--permission-prompts none", joined)
        self.assertIn("Bash(python3 *scripts/verify.py*)", command)
        self.assertIn("mcp__*", command)
        self.assertIn("agents-md@builtin", joined)
        self.assertIn("claude-md-or-agents-md", joined)
        self.assertIn("--no-session-persistence", command)

    def test_codex_command_uses_workspace_write_without_approval(self):
        command = runner.build_command("codex", "task", "gpt-5.6")
        joined = " ".join(command)
        self.assertIn("--sandbox workspace-write", joined)
        self.assertIn("--ask-for-approval never", joined)
        self.assertIn("exec --json", joined)

    def test_summary_separates_variants(self):
        base = {
            "host": "codex",
            "host_version": "x",
            "model": "m",
            "task_id": "B-01",
            "task_class": "backend",
            "run_index": "1",
            "agent_exit_code": "0",
            "latency_ms": "100",
            "changed_file_count": "1",
            "out_of_scope_count": "0",
            "missing_validation_count": "0",
            "forbidden_validation_count": "0",
            "invariant_failure_count": "0",
            "assertion_failure_count": "0",
            "fixture_instruction_bytes": "100",
            "raw_dir": "x",
            "notes": "",
            "experiment_version": "0.1",
            "date": "2026-10-03",
        }
        rows = [
            {**base, "variant": "S0_monolithic_root", "passed": "true"},
            {**base, "variant": "S1_nested_agents", "passed": "false", "missing_validation_count": "1"},
        ]
        summary = runner.summarize(rows)
        self.assertEqual(2, len(summary["groups"]))
        rates = {g["variant"]: g["pass_rate"] for g in summary["groups"]}
        self.assertEqual(1.0, rates["S0_monolithic_root"])
        self.assertEqual(0.0, rates["S1_nested_agents"])


if __name__ == "__main__":
    unittest.main()
