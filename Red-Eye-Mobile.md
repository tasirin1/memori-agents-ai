# Memori Sesi — Red Eye Mobile

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/Red-Eye-Mobile` — aplikasi Android (build SELALU di GitHub Actions; lokal hanya edit + cek sintaks ringan + validasi XML).
- Aturan main (ringkas dari `AGENTS.md`): jangan install SDK lokal; jangan commit secret (bot token/chat ID); changelog Keep a Changelog untuk perubahan perilaku/build/workflow; rilis via bump `versionCode`/`versionName` + tag `vX.Y.Z`.

## Sesi #14 (2026-10-04 07:33 UTC) — selesai
- Permintaan: audit jilid 7, lebih agresif seluruh area (tanpa patch).
- Cakupan: regresi `v1.6.58` (crash embed, wipe, generasi save, cap 64, KEEP, pool bersama, `/ping` owner-only, varian seluler, banner-skip), `MonitoringService` penuh (polling, gerbang, SMS/ring/record/foto/audio, FGS timeout), `CameraService`, `MessageQueue`, `PreferencesManager`, `SendMessageWorker`, `BootRestartWorker`, `SetupActivity`, `MainActivity`, repo, util, manifest, workflow, gradle.
- Temuan baru (14: 3 sedang, 11 rendah): dual-konsumen `/ping` dobel dari sisi main; kursor periodik maju walau kirim gagal; `photoPausedUntil` basi saat boot via `USER_PRESENT`; flush foto tanpa gate auth; setup history kosong kini sunyi; FGS timeout tak reset kamera; `lastSmsSendAt` walau gagal; baca prefs di main-thread; `USER_PRESENT` mungkin no-op API 26+; menu bot bocorkan daftar sensitif; flush crash abaikan blokir auth; jendela initial-sync 100; drop forwarder sunyi di `/lastnotif`; `lastSyncTime` ikut pong.
- Validasi: XML OK, grep secret bersih, tanpa perubahan kode.
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.59`).

## Sesi #13 (2026-10-04 07:32 UTC) — selesai
- Permintaan: perbaiki semua temuan audit jilid 6 (regresi `v1.6.57` + sisa forensik).
- Perbaikan: crash tulis tanpa IO `boot_meta` (elapsed disemat di berkas); wipe reset kursor SMS/panggilan/sync/foto + flag sync; antrean forwarder dibatasi 64; save/test pakai nomor generasi; backoff worker 60 dtk + retry `KEEP`; `boot_meta` di-exclude backup; fallback `USER_PRESENT` kembali + throttle 60 dtk; satu connection pool + dispatcher 4/3 dan 2/1; `/ping` owner-only; varian nomor khusus seluler `628`/`08` tanpa alokasi per baris; banner initial sync dilewati bila tak ada history baru.
- Rilis: commit `9e3370e` + tag `v1.6.58` (`versionCode` 85), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.58` rilis, menunggu hasil CI.

## Sesi #12 (2026-10-04 07:25 UTC) — selesai
- Permintaan: audit jilid 6, lebih agresif seluruh area (tanpa patch).
- Cakupan: regresi `v1.6.57` (crash IO, wipe sisa, serial unbounded, cancel race, boot_meta backup, USER_PRESENT, double pool, help/pong, wake double, idVariants, worker priority), manifest, workflow, repo query.
- Temuan baru (11): IO prefs di crash-thread; kursor history selamat dari wipe; serial 1 antrean tak bounded; cancel kooperatif masih balapan; boot_meta tak di-exclude; hapus USER_PRESENT kurangi reliabilitas; double pool 10/6; pong viewer bocor liveness; double restart ping; false-positive 626 + GC churn; backoff 5 mnt blokir pesan urgent.
- Validasi: XML OK, grep secret bersih, tanpa perubahan kode.
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.58`).

## Sesi #11 (2026-10-04 07:19 UTC) — selesai
- Permintaan: perbaiki semua 11 temuan audit jilid 5.
- Perbaikan: dedup sync + eviksi while; wipe SMS pending + hash + offset; varian `62`/`0`; ring null fail-fast; forwarder serial tunggal; worker backoff 5 mnt; kursor initial hanya saat sukses; hapus `USER_PRESENT`; `TelegramMediaClient` pisah; status/battery/uptime/storage owner-only + help peran; cancel job save/test; crash elapsed monotonic.
- Rilis: commit `e0b4eeb` + tag `v1.6.57` (`versionCode` 84), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.57` rilis, menunggu hasil CI.

## Sesi #10 (2026-10-04 07:17 UTC) — selesai
- Permintaan: audit jilid 5, lebih agresif seluruh area (tanpa patch).
- Cakupan: regresi `v1.6.56` (dedup, dispatcher, channel, Setup IO, crash prune, mutex, boot_meta), `clearCredentials` sisa forensik, `numberMatches` lintas-format ID, `ringDevice` null-URI, order forwarder, hot-loop worker, double initial-sync, receiver spoof, media vs poll, `/help` disclosure, interval race, wall-clock age.
- Temuan baru (11): synchronizedSet tanpa sync + eviksi tunggal; pending SMS + offset basi selamat dari wipe; `0812` vs `62812` miss; ring null tahan busy; order FIFO hilang; reschedule immediate saat gagal; initial-sync ganda; `USER_PRESENT` spoofable; foto blocking slot + captive hang 90 dtk; help/status bocor kapasitas; double-tap save race.
- Validasi: XML OK, grep secret bersih, tanpa perubahan kode.
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.57`).

## Sesi #9 (2026-10-04 07:14 UTC) — selesai
- Permintaan: perbaiki semua 10 temuan audit jilid 4.
- Perbaikan: dispatcher 6/4; dedup 300 updateId + reset offset kondisional; channel MIN + recreate + resume tanpa badge; exclude `crash_pending.txt`; Setup IO-background; hapus crash saat opt-out + prune 7 hari; `/apps` `/log` `/version` owner-only; kalkulator eksponen kecil + secret via operator; lepas mutex forwarder; throttle `boot_meta` persisten + thread daemon.
- Rilis: commit `4713e06` + tag `v1.6.56` (`versionCode` 83), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.56` rilis, menunggu hasil CI.

## Sesi #8 (2026-10-04 07:09 UTC) — selesai
- Permintaan: audit jilid 4, paling agresif seluruh area (tanpa patch).
- Cakupan: `ParentalMonitorApp`, `MessageQueue`, `PreferencesManager`, `MonitoringService` full (polling, gerbang, `/ping`, SMS/record/ring, media, FGS), `CameraService`, `NotificationForwarderService` (wake, dedup, mutex), `SendMessageWorker`, `BootRestartWorker`, `BootReceiver`, `MainActivity` kalkulator, `SetupActivity`, repo SMS/call, `TelegramApi` dispatcher, `MessageScheduler`, `CrashReporter`, manifest, backup/extraction rules, channel.
- Temuan baru (10): (1) starvasi dispatcher OkHttp perHost=2 vs 2 long-poll; (2) replay perintah mutasi saat offset reset 0; (3) channel notifikasi immutable beda DEBUG/release; (4) backup rules tak lindungi filesDir crash_pending; (5) Setup baca encrypted prefs di main-thread; (6) crash stale tak dihapus saat opt-out; (7) `/apps`/`/log`/`/version` bocor ke viewer grup; (8) kalkulator desimal kecil jadi 0 + secret 1234 hilang bila operator dulu; (9) `fwdMutex` tahan kunci selama HTTP; (10) `BootReceiver` goAsync thread mentah + throttle memori saja.
- Validasi: XML OK, grep secret bersih (hanya KEY_/regex), tanpa perubahan kode repo ini (hanya M AGENTS.md docs).
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.56`).

## Status terakhir (2026-10-03)

- `AGENTS.md` ditambah pointer wajib baca/update `MEMORY.md` tiap sesi (repo download-manager sudah lebih dulu).

## Tugas terbuka

- (belum ada)

## Cara pakai file ini

- Awal sesi: baca file ini, lalu `git status --short` + `git log --oneline -5`.
- Akhir sesi: update tanggal, status terakhir, dan tugas terbuka.

## Sesi #2 (2026-10-04 03:38 UTC) — selesai
- Permintaan: audit seluruh kode, temukan bug (tanpa patch).
- Hasil: 12 temuan dilaporkan ke user (kritikal: MessageQueue/PreferencesManager volatile-first race + snapshot loss; SendMessageWorker KEEP stall backlog >20; tombol inline grup mati; cache kredensial forwarder basi; join HandlerThread dari callback; LIKE nomor tidak dinormalisasi; VALIDATED over-strict; short-code <7 digit tak ter-search).
- Validasi: XML 4 file OK, grep secret bersih, tanpa perubahan kode repo ini.
- Status terakhir: audit selesai, menunggu keputusan owner bug mana yang diperbaiki dulu.

## Sesi #3 (2026-10-04 03:52 UTC) — selesai
- Permintaan: perbaiki semua 12 temuan audit sesi #2.
- Perbaikan: `ownerUserId` + gerbang mutasi/baca + tombol grup hidup; delta-copy upgrade prefs + registry listener; `APPEND` scheduler; restore antrean forwarder; normalisasi digit + exact short-code + fallback 200; internet-only check; `elapsedRealtimeNanos`; regex tag ketat; tanpa IO prefs di crash-thread; `applicationContext` di thread; rescale sesi speed; reset owner; guard restart loop `/ping camera`.
- Koreksi audit: klaim deadlock `stopBackgroundThread` dan korutin-bocor `fetchLocation` gugur (kode sudah guard `join` dan `withTimeoutOrNull`).
- Rilis: commit `f2c0c59` + tag `v1.6.53` (`versionCode` 80), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.53` rilis, menunggu hasil CI dan uji grup-mode owner.

## Sesi #4 (2026-10-04 04:10 UTC) — selesai
- Permintaan: audit jilid 2, lebih dalam (tanpa patch).
- Cakupan: seluruh `MonitoringService` (perintah, SMS/record/ring/lock, media, loop), wake-loop forwarder, `CameraService`, worker, `TimeFmt`, repo, model, resource cross-check (semua id/string resolve), `network_security_config`, proguard, workflow, regresi diff `v1.6.53` (bersih).
- Temuan baru: (1) wake-loop `pollWakeOnce` masih lockout owner grup + tanpa gate opt-out user (poll tiap 25 dtk meski monitoring dimatikan); (2) double-pong forwarder vs service; (3) cache `MessageQueue` tak pernah prune kedaluwarsa; (4) `/ping` bare bisa dipakai viewer grup untuk restart loop; (5) `LIKE '%%'` bila query non-digit; (6) fallback kamera bisa salah lensa diam-diam; (7) tolak notifikasi = autostart mati diam-diam; (8) duplikat chunk retry.
- Validasi: XML OK, grep secret bersih, tidak ada perubahan kode.
- Status terakhir: menunggu keputusan owner apakah temuan jilid 2 diperbaiki (usul: rilis `v1.6.54` bila ya).

## Sesi #5 (2026-10-04 04:35 UTC) — selesai
- Permintaan: perbaiki semua 9 temuan audit jilid 2.
- Perbaikan: wake-loop owner-aware + gate opt-out + hapus double-pong; prune cache antrean; `/ping` restart khusus owner; early-return non-digit; tanpa fallback lensa; notifikasi keluar dari syarat autostart; jeda chunk 1000 ms.
- Rilis: commit `1800e8f` + tag `v1.6.54` (`versionCode` 81), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.54` rilis, menunggu hasil CI.

## Sesi #6 (2026-10-04 05:00 UTC) — selesai
- Permintaan: audit jilid 3, lebih dalam (tanpa patch).
- Cakupan: loop `checkAndSendNewData`, `sendFitted`/`safeCut`, SMS pending/confirm, ring restore, audio/photo outcome, `CrashReporter.install` (chaining benar), inputType Setup (token `textPassword` baik), mutex+cap forwarder, `BootRestartWorker`, kalkulator hardcode (wajar), `@Volatile` audit.
- Temuan utama: (1) relaksasi `v1.6.53` membuka data sensitif (`/photo`, `/location`, `/lastcalls`, `/lastsms`, `/lastnotif`, `/contacts`, `/history`) untuk semua viewer grup via `chatOk` — usul gerbang 3 lapis; (2) field cache kredensial/config tanpa `@Volatile` di kedua service; (3) skew jam >5 mnt membunuh semua perintah; (4) APK release non-tag debug-signed tapi bernama release.
- Validasi: tanpa perubahan kode.
- Status terakhir: menunggu keputusan owner apakah temuan jilid 3 diperbaiki (`v1.6.55`).

## Sesi #7 (2026-10-04 05:15 UTC) — selesai
- Permintaan: perbaiki semua 4 temuan audit jilid 3.
- Perbaikan: gerbang 3 lapis + `SENSITIVE_COMMANDS`; petunjuk jam untuk stempel masa depan; `@Volatile` cache kedua service; artefak `redeye-release-debugsigned.apk` + catatan README.
- Rilis: commit `43a7c88` + tag `v1.6.55` (`versionCode` 82), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.55` rilis, menunggu hasil CI.
