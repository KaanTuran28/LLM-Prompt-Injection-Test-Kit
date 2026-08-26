# Durum Günlüğü

> En üstteki kayıt en güncelidir. Her çalışma sonrası buraya kısa bir not düşülür.

---

## 2026-08-21 — CI gating için `--fail-on-leak` eklendi

- Konu: `--fail-on-leak` bayrağı eklendi — herhangi bir payload `LEAKED` sonucu verirse çıkış kodu 1 (regresyon testi olarak CI'a bağlanabilir).
- 3 yeni test eklendi (8 → 11), hepsi geçti. Ruff temiz.
- Durum: ✅ Henüz push edilmedi.

**Sıradaki iş:** GitHub'da `LLM-Prompt-Injection-Test-Kit` adıyla repo aç, git init + push. Öncelikli push edilecek proje.

---

## 2026-08-20 — Paketleme, JSON çıktı ve lint eklendi

- Konu: `pyproject.toml` ile pip kurulabilir hale getirildi (`pip install -e .` → `prompt-injection-tester` komutu), `--format json` seçeneği eklendi (2 yeni testle), ruff lint + CI'a ayrı bir `lint` job'u eklendi.
- Durum: ✅ `ruff check .` temiz, `pytest -v` 8/8 geçti, `pip install -e .` ile kurulan `prompt-injection-tester` komutu gerçekten çalıştırılıp doğrulandı (JSON çıktı, 18 payload, exit code 0), sonra `pip uninstall` ile temizlendi.

**Sıradaki iş:** GitHub'da `LLM-Prompt-Injection-Test-Kit` adıyla repo aç, git init + push. Öncelikli push edilecek proje.

---

## 2026-08-20 — Test suite ve CI eklendi

- Konu: pytest test paketi (`tests/test_prompt_injection_tester.py`, 6 test — tamamen offline, mock hedeflerle) ve GitHub Actions CI iş akışı (`.github/workflows/ci.yml`) eklendi. README'ye CI/Python/License badge'leri ve `## Testing` bölümü eklendi.
- Durum: ✅ `pytest -v` çalıştırıldı, 6/6 test geçti.

**Sıradaki iş:** GitHub'da `LLM-Prompt-Injection-Test-Kit` adıyla repo aç, git init + push. Öncelikli push edilecek proje.

---

## 2026-08-20 — Proje oluşturuldu ve test edildi

- Konu: LLM uygulamaları için offline, savunma odaklı prompt-injection dayanıklılık test kiti.
- Dosya: `prompt_injection_tester.py`, `demo_target.py`, `payloads/injection_payloads.json`
- Durum: ✅ Çalışıyor — hem `vulnerable` hem `hardened` mock hedeflere karşı gerçek çalıştırma yapıldı, `sample_report.md` üretildi. Vulnerable hedefte 18/18 LEAKED, hardened hedefte 18/18 BLOCKED çıktı — aracın ayrım gücünü net gösteriyor.

**Sıradaki iş:** GitHub'da `LLM-Prompt-Injection-Test-Kit` adıyla repo aç, `git init` + ilk commit + push. Portföydeki 5 projeden **öncelikli push edilecek olan** — AI Security hedefiyle en çok örtüşen ve en ayırt edici proje.
