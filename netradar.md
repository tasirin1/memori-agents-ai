# Memori Sesi — NetRadar

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/netradar` — radar jaringan Android, Jetpack Compose (minSdk 29, targetSdk 36).
- Aturan main (ringkas dari `AGENTS.md`): build resmi HANYA via CI; semua Bahasa Indonesia; commit `type: deskripsi` (`feat`/`fix`/`refactor`/`test`/`perf`/`docs`); `versionName` tetap `"2.0"`, `versionCode` otomatis; guard changelog di CI (perubahan `app/src`, `scripts/`, `.github/workflows/`, `app/build.gradle.kts` wajib sertakan `CHANGELOG.md`); unit test logika murni tanpa Robolectric.
- Workflow Build docs-only skip (`**.md`, `LICENSE`, `.gitignore`) — selaras repo Tasirin lain.

## Status terakhir (2026-10-03)

- Onboarding ke mesin: clone + pointer `MEMORY.md` di `AGENTS.md` + docs-only skip CI.

## Tugas terbuka

- (belum ada)

## Cara pakai file ini

- Awal sesi: baca file ini, lalu `git status --short` + `git log --oneline -5`.
- Akhir sesi: update tanggal, status terakhir, dan tugas terbuka.
