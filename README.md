# LLM Prompt Injection Test Kit

![CI](https://github.com/KaanTuran28/LLM-Prompt-Injection-Test-Kit/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> ⚠️ **Defensive use only.** This kit is intended to help you test the prompt-injection resilience of your **own** LLM-integrated applications (or ones you have explicit permission to test). It ships with fully offline mock targets — no API keys or third-party services required. References: [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (LLM01: Prompt Injection).

A small, dependency-free toolkit for running a library of known prompt-injection patterns against an LLM-backed target and reporting whether each one leaked, was blocked, or needs manual review.

## Overview

- A categorized library of ~18 public/well-documented injection patterns (`payloads/injection_payloads.json`).
- A test harness (`prompt_injection_tester.py`) that sends each payload to a pluggable target function and classifies the response as `LEAKED`, `SUSPICIOUS`, or `BLOCKED`.
- Two offline mock targets (`demo_target.py`) — `vulnerable_target` and `hardened_target` — so you can see the tool in action with zero setup.

## Installation

No external dependencies. Requires Python 3.9+.

```bash
git clone <this-repo-url>
cd LLM-Prompt-Injection-Test-Kit
pip install -e .
```

This installs a `prompt-injection-tester` console command (via `pyproject.toml`). You can also just run `python prompt_injection_tester.py ...` directly without installing.

## Usage

Run the bundled demo targets:

```bash
prompt-injection-tester --target vulnerable --output vulnerable_report.md
prompt-injection-tester --target hardened --output hardened_report.md

# Or as machine-readable JSON:
prompt-injection-tester --target vulnerable --format json --output vulnerable_report.json
```

### Plugging in your own target

Replace the mock import with a function that calls your real application, then reuse `run_tests` directly:

```python
from prompt_injection_tester import load_payloads, run_tests, render_report

def my_target(prompt: str) -> str:
    # Call your own LLM-integrated app/API here.
    return my_app.handle_message(prompt)

payloads = load_payloads("payloads/injection_payloads.json")
results = run_tests(my_target, payloads, secret_marker="MY_CANARY_VALUE")
print(render_report("My App", results))
```

Tip: seed your target's context with a unique canary string (via `--secret-marker`) so leakage is unambiguous to detect.

## CI Integration

`--fail-on-leak` turns a run into a regression gate: wire your real target into the harness (see above) and fail the pipeline if any payload achieves a `LEAKED` verdict.

```bash
prompt-injection-tester --target vulnerable --fail-on-leak   # exits 1
prompt-injection-tester --target hardened --fail-on-leak     # exits 0
```

```yaml
# GitHub Actions step (after adapting main() or run_tests() to call your own target)
- name: Prompt-injection regression check
  run: prompt-injection-tester --target vulnerable --fail-on-leak
```

Without the flag, the exit code is always `0` — safe for ad-hoc report generation.

## Testing

```bash
pip install -r requirements-dev.txt
pytest -v
ruff check .
```

## Payload Categories

| Category | Description |
|---|---|
| `direct_override` | Attempts to make the model discard its system prompt/instructions outright. |
| `roleplay_jailbreak` | Persona or fictional-framing patterns (e.g. DAN-style) meant to bypass restrictions. |
| `exfiltration_probe` | Attempts to make the model reveal its system prompt or hidden context/secrets. |
| `indirect_injection` | Instructions hidden inside untrusted tool output, documents, or web content passed to the model. |

## Example Output

Against the naive `vulnerable_target`, every payload leaked:

```
### Vulnerable Target Results
- Total payloads: 18
- LEAKED: 18 | SUSPICIOUS: 0 | BLOCKED: 0
```

Against `hardened_target`, which recognizes the same cue patterns and refuses:

```
### Hardened Target Results
- Total payloads: 18
- LEAKED: 0 | SUSPICIOUS: 0 | BLOCKED: 18
```

See [`sample_report.md`](./sample_report.md) for the full generated report, including per-payload verdicts.

## Project Structure

```
LLM-Prompt-Injection-Test-Kit/
├── prompt_injection_tester.py   # CLI + reusable run_tests()/render_report() functions
├── demo_target.py                # Offline vulnerable/hardened mock targets
├── payloads/
│   └── injection_payloads.json   # Categorized test payload library
├── sample_report.md              # Real output from running both demo targets
├── tests/
│   └── test_prompt_injection_tester.py
├── .github/workflows/ci.yml      # Lint (ruff) + test jobs on every push/PR
├── pyproject.toml                # Packaging (pip install -e .) + ruff config
├── requirements.txt
├── requirements-dev.txt
└── LICENSE
```

## License

MIT — see [LICENSE](./LICENSE).
