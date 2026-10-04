# Memori Sesi — Tasirin Vaultwarden Host

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-vaultwarden-host` — host Vaultwarden Android (minSdk 21, targetSdk 28).
- Aturan main (ringkas dari `AGENTS.md`): DILARANG KERAS build/test/lint lokal dalam bentuk apa pun; verifikasi lokal hanya baca kode, `grep`/`rg`, `git diff`/`log`, parse XML; satu-satunya build/test/rilis via push ke `main` + GitHub Actions; semua Bahasa Indonesia; commit `feat:`/`fix:`/`docs:`/`chore:`/`perf:`; tiap selesai perbaikan langsung commit + push.

## Status terakhir (2026-10-03)

- `AGENTS.md` ditambah pointer wajib baca/update `MEMORY.md` tiap sesi (repo download-manager sudah lebih dulu).

## Tugas terbuka

- (belum ada)

## Cara pakai file ini

- Awal sesi: baca file ini, lalu `git status --short` + `git log --oneline -5`.
- Akhir sesi: update tanggal, status terakhir, dan tugas terbuka.

## Sesi #1 — 2026-10-04 06:37 UTC (selesai)
- Audit baca-saja seluruh kode (tanpa build lokal, sesuai Aturan No.1): Util, PinCrypto/PinGate, KernelCompat, StoragePerm, HttpsCompat, FileShareProvider, LogExport/LogActivity, TlsCert, ServerService, Updater, TgBot/TgBackup, Settings/Main/Alarm/Boot/TgBotReceiver, AutoUpdate, manifest, build.gradle.
- Temuan 3 bug baru (dilaporkan ke user, belum diperbaiki — menunggu perintah fix+push):
  1. Clipboard Settings/Main tak tahan mati proses (token mengendap); LogActivity sudah persisten via prefs.
  2. TgBot.authDangerous upgrade hash PIN tanpa cek-ulang (race timpa hash baru); Settings/Main sudah cek-ulang.
  3. SettingsActivity.portEfektifUntukSalin pakai port mentah tanpa normalisasiPort (URL salinan bisa invalid/privileged).
- Status terakhir: audit selesai, 3 bug dilaporkan, belum ada perbaikan/push di repo app (hanya AGENTS.md termodifikasi lokal pre-existing).

## Sesi #2 — 2026-10-04 06:47 UTC (selesai)
- Perbaiki 3 bug audit sesi #1, tiap fix satu commit + push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `42e2138 fix: clipboard satu pintu tahan mati proses` (LogActivity helper statis `salinBersihOtomatis`/`bersihkanClipBasiJikaAda`; Settings/Main reuse + cleanup saat buka).
  - `92cb517 fix: cegah bot timpa hash PIN baru saat upgrade` (TgBot baca-ulang hash sebelum tulis, selaras Settings/Main).
  - `1cd01ef fix: salin URL selalu pakai port ternormalisasi` (Settings pakai `ServerService.normalisasiPort`).
  - Plus `8343611 docs:` untuk perubahan AGENTS.md lokal yang menggantung.
- Verifikasi milik CI (build-apk ringan); tidak menjalankan `gh run watch` sesuai aturan.

## Sesi #3 — 2026-10-04 06:57 UTC (selesai)
- Audit agresif baca-saja (tanpa build lokal): ServerService (env/health/wakelock/killStale/dataDir/log-thread/gantiAtomik/verifier loopback), Updater (redirect/resume/SHA/staging/trust-anchor/shim), TgBackup (schedule/secret/crypto/restore/retensi), TgBot (auth/PIN-parse/callback/kunci tugas), Settings/Main/Log (PIN/import/export/clipboard), TlsCert (encoder DER penuh), HttpsCompat, FileShareProvider, receiver, AutoUpdate, manifest+net-config, proguard, gradle, kedua workflow CI, daftar test.
- Vonis: tidak ada bug kritikal/tinggi. 2 nit rendah dilaporkan (START_TERTUNDA dikonsumsi sebelum start sukses; verifikasi PIN pakai hash tangkapan basi) — menunggu perintah perbaiki.

## Sesi #4 — 2026-10-04 07:05 UTC (selesai)
- Perbaiki 2 nit audit agresif sesi #3, tiap fix satu commit + push ke `main`:
  - `75f0975 fix: flag susulan start tak hangus bila gagal` (MainActivity hapus START_TERTUNDA hanya bila start sukses; gagal = coba lagi saat buka berikut).
  - `3cac864 fix: verifikasi PIN lawan hash segar` (Main/Settings baca hash di worker; TgBot nilai ulang bila hash berganti selama PBKDF2).
- Verifikasi milik CI; tidak memantau build sesuai aturan.
