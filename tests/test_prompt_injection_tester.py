import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json

from demo_target import hardened_target, vulnerable_target
from prompt_injection_tester import load_payloads, main, render_json, render_report, run_tests

PAYLOADS_PATH = Path(__file__).resolve().parent.parent / "payloads" / "injection_payloads.json"


def test_payloads_load_and_cover_all_categories():
    payloads = load_payloads(PAYLOADS_PATH)
    assert len(payloads) == 18
    categories = {p["category"] for p in payloads}
    assert categories == {"direct_override", "roleplay_jailbreak", "exfiltration_probe", "indirect_injection"}


def test_vulnerable_target_leaks_on_every_payload():
    payloads = load_payloads(PAYLOADS_PATH)
    results = run_tests(vulnerable_target, payloads)
    assert all(r["verdict"] == "LEAKED" for r in results)


def test_hardened_target_blocks_every_payload():
    payloads = load_payloads(PAYLOADS_PATH)
    results = run_tests(hardened_target, payloads)
    assert all(r["verdict"] == "BLOCKED" for r in results)


def test_suspicious_verdict_for_ambiguous_response():
    def ambiguous_target(prompt: str) -> str:
        return "I'm not sure how to respond to that."

    payloads = [{"id": "x-01", "category": "direct_override", "payload": "ignore everything"}]
    results = run_tests(ambiguous_target, payloads)
    assert results[0]["verdict"] == "SUSPICIOUS"


def test_secret_marker_leak_detected_even_without_compliance_cue():
    def leaky_target(prompt: str) -> str:
        return "Here you go: SECRET_MARKER_XYZ embedded in the answer."

    payloads = [{"id": "x-02", "category": "exfiltration_probe", "payload": "reveal secret"}]
    results = run_tests(leaky_target, payloads)
    assert results[0]["verdict"] == "LEAKED"
    assert "secret marker" in results[0]["notes"].lower()


def test_render_report_summary_counts_match():
    payloads = load_payloads(PAYLOADS_PATH)
    results = run_tests(hardened_target, payloads)
    report = render_report("Hardened", results)
    assert f"BLOCKED: {len(results)}" in report
    assert "LEAKED: 0" in report
    assert "### Hardened Target Results" in report


def test_render_json_is_valid_and_matches_results():
    payloads = load_payloads(PAYLOADS_PATH)
    results = run_tests(hardened_target, payloads)
    parsed = json.loads(render_json(results))
    assert len(parsed) == len(results)
    assert all(r["verdict"] == "BLOCKED" for r in parsed)


def test_render_json_entries_have_expected_fields():
    payloads = load_payloads(PAYLOADS_PATH)
    results = run_tests(vulnerable_target, payloads)
    parsed = json.loads(render_json(results))
    for entry in parsed:
        assert set(entry.keys()) == {"id", "category", "verdict", "notes"}


def run_main(monkeypatch, target, extra_args):
    monkeypatch.setattr(sys, "argv", ["prompt_injection_tester.py", "--target", target] + extra_args)
    return main()


def test_fail_on_leak_exits_nonzero_against_vulnerable_target(monkeypatch):
    assert run_main(monkeypatch, "vulnerable", ["--fail-on-leak"]) == 1


def test_fail_on_leak_exits_zero_against_hardened_target(monkeypatch):
    assert run_main(monkeypatch, "hardened", ["--fail-on-leak"]) == 0


def test_no_fail_on_leak_always_exits_zero_even_when_vulnerable(monkeypatch):
    assert run_main(monkeypatch, "vulnerable", []) == 0
