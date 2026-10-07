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

## Sesi #5 — 2026-10-04 07:15 UTC (selesai)
- Audit super-agresif: cek otomatis ID/string/drawable/warna/layout-land/night-sync/vektor (semua cocok; `stat_notify_sync` milik framework), plus telusur health/restart, resume/SHA, restore-streaming, kirim-Telegram, latestVersion, saveAndStart.
- Temuan: 1 bug sedang — `saveAndStart` menerima port 1-1023 lalu server diam-diam jalan di default (prefs/UI/server tak sepakat); fix `b5478ae` sembuhkan ke default di depan + set ulang field + toast/log.
- `d20832e docs:` lengkapi CHANGELOG untuk 6 fix audit terakhir (lolos CI, hanya md).
- Verifikasi milik CI; tidak memantau build sesuai aturan.

## Sesi #6 — 2026-10-07 01:42 UTC (selesai)
- Tanya-jawab baca-saja (tanpa build lokal): user tanya kenapa binary diunduh ulang terus bila tidak di-reset manual.
- Diagnosis: `ensureBinary` (ServerService.java) hanya pakai cache bila patch-rev cocok + (marker `update_version` ada atau `version.txt` cocok APK) + smoke test `--version` lolos + versi cocok kuncian; gagal satu saja jatuh ke unduh. `tryUpdateVersi`/`AutoUpdate` bandingkan versi PROSES yang sedang jalan (`ServerService.binaryVersion`), bukan file — bila update terunduh tapi server tak restart, tiap cek mengunduh ulang file yang sama. Reset manual (hapus file + `version.txt` + marker) memaksa satu unduhan bersih yang mengisi marker/patch-rev/tag konsisten + proses jalan dari file baru sehingga loop berhenti.
- Kandidat fix (belum dikerjakan, menunggu perintah): prioritaskan versi file di `tryUpdateVersi`, tulis `KEY_UPDATE_VERSION` di jalur manual-copy path 2, persist `KEY_BIN_PATCH` walau fallback-cache.

## Sesi #7 — 2026-10-07 01:42 UTC (selesai)
- Perbaiki loop unduh binary (laporan user sesi #6), 2 commit + push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `95e532c fix: hentikan unduh binary berulang tanpa reset manual` (Updater nilai versi file dulu + pesan restart bermarker; binary manual catat `update_version`; throttle 6 jam unduhan perbaikan gagal; `bin_dl_gagal_at` tak ikut export; 5 uji baru).
  - `3ce0a77 docs: changelog unduh binary berulang` (md saja, CI dilewati).
- Penyimpangan sadar dari usulan awal: `KEY_BIN_PATCH` TIDAK ditulis saat fallback-cache (akan menutupi binary belum-patch); sebagai gantinya throttle coba-ulang.
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.

## Sesi #8 — 2026-10-07 02:15 UTC (selesai)
- Audit agresif baca-saja seluruh area (tanpa build lokal): ServerService (start/stop/restart/health/killStale/port/dataDir/log), Updater (tryUpdate/download/resume/SHA/webvault/shim/trust/redirect), TgBot (auth/PIN/callback/update/restore), TgBackup (k WinG/GCM/restore/zip-slip/jadwal/export), Settings/Main (port/PIN/kuncian/import/restore/susulan), PinGate, TlsCert, KernelCompat, StoragePerm, FileShareProvider, LogExport, HttpsCompat, Util, Alarm/Boot/TgBotReceiver, AutoUpdate, manifest, res (ID/night/vektor), workflow CI, gradle, proguard.
- Vonis: tidak ada bug kritikal/tinggi. 1 regresi sedang dari sesi #7 ditemukan + langsung diperbaiki (`4811235`: jalan pintas unduh abaikan butuhRefresh; cap gagal dibatasi refresh-only; uji `unduhTetapJalanBilaPatchBasi`). Push terkonfirmasi di origin.
- Temuan rendah/kosmetik dilaporkan ke user, belum diperbaiki (menunggu perintah): WV redirect-offline tak cap marker (unduh ulang 35MB), komentar isPortBusy basi, Start saat stopping diabaikan diam-diam, pesan gagal /restart hampir mati, RSS cache basi, hint restart palsu pasca-update WV, toast restart-notice tiap buka app, START_TERTUNDA hapus saat intent terkirim, Unduh&Start tanpa batal.

## Sesi #9 — 2026-10-07 (selesai)
- User tanya ulang kenapa binary unduh terus bila tak di-reset manual (log: 3x "gagal uji jalan --version", reset lalu sukses) + "perbaiki semuanya".
- Diagnosis lanjutan: reset bukan obat (cuma kebetulan jaringan/shim pulih). Akar loop: (1) downloadBinaryInner unduh ~20MB dulu baru pastikan shim — di kernel lama tanpa shim valid, uji asap pasti gagal, tmp dibuang, cek berikut unduh lagi; (2) throttle 6 jam hanya di ensureBinary, jalur AutoUpdate/tryUpdate unduh tiap buka app; (3) tiap gagal auto-update memicu notifikasi "tersedia" tanpa dedup; (4) bolehCobaUnduhLagi salah pasca-reboot (elapsed reset); (5) reset tak buang cap gagal.
- Fix `75da093` + docs `bf4d51d`, push ke main (tanpa build/pantau): fail-fast shim sebelum unduh; AutoUpdate cooldown berbagi cap (sukses hapus, gagal catat) + tanpa notif tiap gagal; throttle tahan reboot; reset buang cap; AutoUpdateTest baru + uji reboot.
- Verifikasi milik CI; tidak memantau build sesuai aturan.

## Sesi #10 — 2026-10-07 (selesai)
- Audit agresif seluruh area atas perintah user: 19k baris dibaca via grep/sed (tanpa build lokal). Vonis: tanpa kritikal; PIN/bot/restore/crypto/TLS/provider/alarm/redirect bersih.
- Temuan: 2 sedang (health-restart uncapped + spam Telegram; race restartTunda vs killer async = restart hilang diam-diam) + 8 kecil (WV redirect 35MB, Settings activity-leak, toast tiap buka, gagal-unduh-tetap-start x2, START_TERTUNDA hangus, PID-reuse RSS, rotasi log truncate, komentar isPortBusy).
- Fix 2 commit kode + 1 docs, push ke main (tanpa pantau CI): `ef737ca` (service: sync-wait + recordRestart health, rotasi log, PID ketat, 2 uji), `9987dc6` (updater/UI: cap WV redirect, toast sekali, no-start-on-fail, app-context, flag susulan, 2 uji), `8fb912a` docs.
- Sengaja tak diubah: cabang prefs.has tg_notified/wv_from di applyPrefsFromJson (mati suri tapi aman untuk config edit-manual).

## Sesi #11 — 2026-10-07 02:48 UTC (selesai)
- Audit agresif baca-saja seluruh area atas perintah user (tanpa build lokal, sesuai Aturan No.1): ServerService (lock/log/health/smoke), Updater (resume/hash/redirect), TgBackup (GCM/restore/import), TgBot auth, PinCrypto/PinGate, TlsCert/HttpsCompat, FileShareProvider, StoragePerm, Alarm/Boot receiver, AutoUpdate, Util, manifest.
- Vonis: tanpa kritikal/tinggi. Terverifikasi bersih: baca logBuffer semua terkunci, LOG_TS semua synchronized, redirect max-5 https+host-GitHub, TUGAS_DATA semua try-finally, configJson kecualikan secret, provider exported=false, smoke watchdog+TOCTOU ok.
- Temuan baru dilaporkan ke user, belum diperbaiki (menunggu perintah): 1 sedang (samarkanLog 12 regex di dalam synchronized logBuffer di LogActivity:384-385,603-604 — tahan lock + risiko ANR; pola benar sudah ada di :631-634), 3 rendah (adaSymlinkInduk fail-open bila lstat gagal; normVersion tanpa validasi → URL asset malformed bila tag API aneh; TlsCert baca-vs-tulis tanpa lock di jeda ensure).
- Status terakhir: audit sesi #11 selesai, temuan dilaporkan, tanpa perubahan/push di repo app.

## Sesi #12 — 2026-10-07 02:48 UTC (selesai)
- Perbaiki 4 temuan audit sesi #11 atas perintah user, tiap fix satu commit + push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `fee9f06 fix: samarkan log di luar kunci buffer agar tak tahan thread server` (LogActivity shareLog/copyLog).
  - `2765079 fix: cek symlink fail-closed bila lstat gagal di perangkat` (FileShareProvider + uji `symlinkIndukBersihDiJvm`).
  - `b0bf904 fix: tolak tag versi aneh agar tak ditempel ke URL asset` (Updater.normVersion + uji `normVersion_tolakTagAneh`).
  - `e4a6486 fix: baca ulang sertifikat bila hilang sesaat saat tukar atomik` (TlsCert.sisaMs retry 100ms).
  - `6ece938 docs: changelog audit lock log symlink versi sertifikat` (md saja, CI dilewati).
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.
