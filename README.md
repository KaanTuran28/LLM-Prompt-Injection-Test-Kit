# LLM Prompt Injection Test Kit

![CI](https://github.com/KaanTuran28/LLM-Prompt-Injection-Test-Kit/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

<p align="center"><b><a href="#english">English</a></b> · <b><a href="#türkçe">Türkçe</a></b></p>

---

## English

> ⚠️ **Defensive use only.** This kit is intended to help you test the prompt-injection resilience of your **own** LLM-integrated applications (or ones you have explicit permission to test). It ships with fully offline mock targets — no API keys or third-party services required. References: [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (LLM01: Prompt Injection).

A small, dependency-free toolkit for running a library of known prompt-injection patterns against an LLM-backed target and reporting whether each one leaked, was blocked, or needs manual review.

### Overview

- A categorized library of ~18 public/well-documented injection patterns (`payloads/injection_payloads.json`).
- A test harness (`prompt_injection_tester.py`) that sends each payload to a pluggable target function and classifies the response as `LEAKED`, `SUSPICIOUS`, or `BLOCKED`.
- Two offline mock targets (`demo_target.py`) — `vulnerable_target` and `hardened_target` — so you can see the tool in action with zero setup.

### Installation

No external dependencies. Requires Python 3.9+.

```bash
git clone <this-repo-url>
cd LLM-Prompt-Injection-Test-Kit
pip install -e .
```

This installs a `prompt-injection-tester` console command (via `pyproject.toml`). You can also just run `python prompt_injection_tester.py ...` directly without installing.

### Usage

Run the bundled demo targets:

```bash
prompt-injection-tester --target vulnerable --output vulnerable_report.md
prompt-injection-tester --target hardened --output hardened_report.md

# Or as machine-readable JSON:
prompt-injection-tester --target vulnerable --format json --output vulnerable_report.json
```

#### Plugging in your own target

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

### CI Integration

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

### Testing

```bash
pip install -r requirements-dev.txt
pytest -v
ruff check .
```

### Payload Categories

| Category | Description |
|---|---|
| `direct_override` | Attempts to make the model discard its system prompt/instructions outright. |
| `roleplay_jailbreak` | Persona or fictional-framing patterns (e.g. DAN-style) meant to bypass restrictions. |
| `exfiltration_probe` | Attempts to make the model reveal its system prompt or hidden context/secrets. |
| `indirect_injection` | Instructions hidden inside untrusted tool output, documents, or web content passed to the model. |

### Example Output

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

### Project Structure

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

### License

MIT — see [LICENSE](./LICENSE).

---

## Türkçe

> ⚠️ **Yalnızca savunma amaçlı kullanım.** Bu kit, **kendi** LLM entegrasyonlu uygulamalarınızın (veya test etmek için açık izniniz olan uygulamaların) prompt injection saldırılarına karşı dayanıklılığını test etmenize yardımcı olmak için tasarlanmıştır. Tamamen çevrimdışı çalışan mock hedeflerle birlikte gelir — API anahtarı veya üçüncü taraf servis gerektirmez. Referanslar: [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (LLM01: Prompt Injection).

Bilinen prompt injection kalıplarından oluşan bir kütüphaneyi LLM tabanlı bir hedefe karşı çalıştıran ve her birinin sızdırıp sızdırmadığını, engellenip engellenmediğini ya da manuel inceleme gerektirip gerektirmediğini raporlayan, bağımlılıksız, küçük bir araç seti.

### Genel Bakış

- Yaklaşık 18 adet herkese açık/iyi belgelenmiş injection kalıbından oluşan kategorize edilmiş bir kütüphane (`payloads/injection_payloads.json`).
- Her payload'ı takılabilir (pluggable) bir hedef fonksiyona gönderen ve yanıtı `LEAKED`, `SUSPICIOUS` veya `BLOCKED` olarak sınıflandıran bir test altyapısı (`prompt_injection_tester.py`).
- Aracı sıfır kurulumla aksiyonda görebilmeniz için iki çevrimdışı mock hedef (`demo_target.py`) — `vulnerable_target` ve `hardened_target`.

### Kurulum

Harici bağımlılık yoktur. Python 3.9+ gerektirir.

```bash
git clone <this-repo-url>
cd LLM-Prompt-Injection-Test-Kit
pip install -e .
```

Bu, (`pyproject.toml` üzerinden) bir `prompt-injection-tester` konsol komutu kurar. Kurulum yapmadan da doğrudan `python prompt_injection_tester.py ...` şeklinde çalıştırabilirsiniz.

### Kullanım

Birlikte gelen demo hedefleri çalıştırın:

```bash
prompt-injection-tester --target vulnerable --output vulnerable_report.md
prompt-injection-tester --target hardened --output hardened_report.md

# Ya da makine tarafından okunabilir JSON olarak:
prompt-injection-tester --target vulnerable --format json --output vulnerable_report.json
```

#### Kendi hedefinizi eklemek

Mock import'u kendi uygulamanızı çağıran bir fonksiyonla değiştirin, ardından `run_tests`'i doğrudan yeniden kullanın:

```python
from prompt_injection_tester import load_payloads, run_tests, render_report

def my_target(prompt: str) -> str:
    # Call your own LLM-integrated app/API here.
    return my_app.handle_message(prompt)

payloads = load_payloads("payloads/injection_payloads.json")
results = run_tests(my_target, payloads, secret_marker="MY_CANARY_VALUE")
print(render_report("My App", results))
```

İpucu: sızıntının tespitinin belirsiz olmaması için hedefinizin bağlamına (`--secret-marker` ile) benzersiz bir kanarya (canary) dizesi yerleştirin.

### CI Entegrasyonu

`--fail-on-leak`, bir çalıştırmayı regresyon kapısına (regression gate) dönüştürür: gerçek hedefinizi test altyapısına bağlayın (yukarıya bakın) ve herhangi bir payload `LEAKED` sonucu alırsa pipeline'ı başarısız kılın.

```bash
prompt-injection-tester --target vulnerable --fail-on-leak   # exits 1
prompt-injection-tester --target hardened --fail-on-leak     # exits 0
```

```yaml
# GitHub Actions step (after adapting main() or run_tests() to call your own target)
- name: Prompt-injection regression check
  run: prompt-injection-tester --target vulnerable --fail-on-leak
```

Bu flag olmadan çıkış kodu her zaman `0`'dır — ad-hoc rapor üretimi için güvenlidir.

### Test

```bash
pip install -r requirements-dev.txt
pytest -v
ruff check .
```

### Payload Kategorileri

| Kategori | Açıklama |
|---|---|
| `direct_override` | Modelin sistem prompt'unu/talimatlarını doğrudan yok saymasını sağlamaya yönelik girişimler. |
| `roleplay_jailbreak` | Kısıtlamaları aşmayı amaçlayan persona veya kurgusal çerçeveleme kalıpları (ör. DAN tarzı). |
| `exfiltration_probe` | Modelin sistem prompt'unu veya gizli bağlamını/sırlarını ifşa etmesini sağlamaya yönelik girişimler. |
| `indirect_injection` | Modele iletilen güvenilmeyen araç çıktısı, belge veya web içeriği içine gizlenmiş talimatlar. |

### Örnek Çıktı

Naif `vulnerable_target`'a karşı, tüm payload'lar sızdırdı:

```
### Vulnerable Target Results
- Total payloads: 18
- LEAKED: 18 | SUSPICIOUS: 0 | BLOCKED: 0
```

Aynı ipucu kalıplarını tanıyıp reddeden `hardened_target`'a karşı:

```
### Hardened Target Results
- Total payloads: 18
- LEAKED: 0 | SUSPICIOUS: 0 | BLOCKED: 18
```

Payload bazında sonuçlar dahil olmak üzere tam üretilen rapor için [`sample_report.md`](./sample_report.md) dosyasına bakın.

### Proje Yapısı

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

### Lisans

MIT — bkz. [LICENSE](./LICENSE).

---
