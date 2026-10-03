# Memori Sesi — Tasirin Download Manager

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-download-manager` — download manager Android (Kotlin, minSdk 21, targetSdk 36).
- Aturan main (ringkas dari `AGENTS.md`): build resmi HANYA via CI, DILARANG install SDK lokal; UI Inggris, komentar Indonesia; commit `type(scope): deskripsi`; jangan ubah `versionName`/`versionCode` manual (CI bump per run); sumber remote web = `remote.src.html` + `python3 scripts/prepare_remote.py` (jangan edit `assets/remote.html` manual); guard `scripts/check_repo.py` + `scripts/security_audit.py`; perubahan kode wajib entri `CHANGELOG.md`; setelah fix langsung push tanpa pantau workflow (aturan 19).

## Status terakhir (2026-10-03, HEAD a133b8f)

- HEAD: `e2d54c2` fix(audit) jilid 8.
- Sesi audit jilid 10 (2026-10-03, commit a46de8d, push main sukses): 3 race diperbaiki — (1) `DownloadEngine` reset/hapus `throttleTotals` satu lock dengan `addThrottleTotal`; (2) sampel speed/ETA dua map digabung satu holder `Pair` atomik; (3) `HttpControlServer.uploadLockFor()` nullable + tegak batas `MAX_UPLOAD_LOCKS` atomik. Guard: `security_audit` 0 error/0 warning (self-test OK), `check_readme_sync` sinkron. `prepare_remote --check` tak disentuh (remote tak diubah).
- Sesi audit → 7 bug ditemukan → SEMUA diperbaiki dan SUDAH push (commit 32d5165 + 41aa4b9, 2026-10-03):
  1. `util/MediaLibrary.kt` — total galeri = distinct penuh sebelum `take(3000)` (`hasMore`/load-more tidak berhenti palsu).
  2. `remote/ServerVideoDurations.kt` — `save()` via staging + rename (crash tak tinggalkan JSON setengah jadi).
  3. `download/DownloadEngine.kt` — `segProgress` jadi `AtomicLongArray` + lock bersama create/clear/snapshot; ganti array bila `segCount` berubah.
  4. `download/DownloadEngine.kt` — `SpeedThrottle.sleepIfNeeded()` hitung total di LUAR lock.
  5. `util/FileSaver.kt` — merge pakai 8 strip-lock per nama file (pola `zipCached`).
  6. `WebExtractActivity.kt` — skema `ignoreCase` + subdomain sehost diizinkan (challenge Cloudflare lolos).
  7. `util/Updater.kt` — baca daftar 20 rilis dulu; rilis tanpa APK = null, bukan cache basi (`getOrElse`, bukan `getOrNull() ?:`).
  - `util/UpdaterTest.kt` — test baru: rilis tanpa APK → null; kode tertinggi lintas rilis.
- Guard: `security_audit.py` 0 error/0 warning; `check_readme_sync.py` sinkron; `prepare_remote --check` tak jalan penuh (remote tak disentuh).

## Tugas terbuka

- [x] `check_repo.py` 10/10 hijau; push ke `main` sukses (tidak pantau workflow).
- [ ] Pastikan CI Build APK hijau pasca-push (a46de8d).
- [x] Soul lintas-repo: user minta 1 soul nyambung semua repo — ternyata sudah ada (`SOUL.md` + 4 memori + pointer `AGENTS.md` di 4 repo). Perbaiki 1 yang belum sinkron: `AGENTS.md` download-manager belum baca `SOUL.md` (commit a133b8f, docs-only, push sukses tanpa pantau workflow).

## Pola bug langganan (jangan ulangi)

- Cache dua field volatil bisa sobek → satu holder `Pair` atomik.
- `getOrPut` Kotlin tak atomik di `ConcurrentHashMap` → `synchronized` eksplisit.
- `SimpleDateFormat` tak thread-safe → `ThreadLocal` / dalam lock.
- `LongArray` lintas thread → `AtomicLongArray` / snapshot di dalam lock.
- `getOrNull() ?: cache` mengubah null-sukses jadi cache basi → `getOrElse`.
- Total dihitung setelah `take()` → total dari distinct penuh SEBELUM `take()`.

## Sesi soul lintas-repo (2026-10-03)

- Verifikasi: 4 repo (`tasirin-download-manager`, `tasirin-vaultwarden-host`, `Red-Eye-Mobile`, `netradar`) semua pointer `AGENTS.md` sudah ke `memori-agents-ai` + `SOUL.md`; hanya download-manager yang tertinggal satu kata (`SOUL.md`) di working tree — sudah di-commit/push (a133b8f).
- Tidak ada perubahan `SOUL.md` — identitas tetap sudah tepat.

## Sesi tanya soul (2026-10-03)

- User tanya soal 1 soul lintas-repo, lalu tanya "gaya bicara?" — dijelaskan isi `SOUL.md` bagian Gaya bicara.

## Cara pakai file ini

- Awal sesi: baca file ini, lalu `git status --short` + `git log --oneline -5` untuk konteks.
- Akhir sesi: update tanggal, status terakhir, dan tugas terbuka.

- `AGENTS.md` kini mewajibkan baca/update `MEMORY.md` tiap sesi (commit 0214eeb) — sesi baru otomatis nyambung selama cwd sama.
- Pointer `MEMORY.md` dipasang di SEMUA repo mesin ini (download-manager 0214eeb, vaultwarden-host 7a3eff9, Red-Eye-Mobile 80de38a) — tiap repo punya `MEMORY.md` lokal sendiri.
- Repo ke-4 dikelola: `tasirin1/netradar` di `/root/netradar` (branch `master`!) — onboarding 2026-10-03: pointer MEMORY.md + workflow docs-only skip (d6a75aa). Guard changelog netradar: perubahan `app/src`, `scripts/`, `.github/workflows/`, `app/build.gradle.kts` wajib sertakan `CHANGELOG.md`.
- Tata kelola diseragamkan (2026-10-03): download-manager `build.yml` docs-only skip + aturan 16 selaras model 19 (3dba05d); Red-Eye pengecualian rilis docs-only (243e976); vaultwarden sudah benar, tak diubah.
- Migrasi memori ke repo pusat (2026-10-03): repo `tasirin1/memori-agents-ai` dibuat; 4 memori lokal dipindah ke sini (c3f7af3); pointer `AGENTS.md` keempat repo dialihkan ke sini + file lokal dihapus (download-manager c615b1f, vaultwarden f84dc3e, Red-Eye c7c8961, netradar 009e31a). Alur: awal sesi pull repo memori, akhir sesi update + commit/push.
