# Memori Sesi — Red Eye Mobile

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/Red-Eye-Mobile` — aplikasi Android (build SELALU di GitHub Actions; lokal hanya edit + cek sintaks ringan + validasi XML).
- Aturan main (ringkas dari `AGENTS.md`): jangan install SDK lokal; jangan commit secret (bot token/chat ID); changelog Keep a Changelog untuk perubahan perilaku/build/workflow; rilis via bump `versionCode`/`versionName` + tag `vX.Y.Z`.

## Sesi #23 (2026-10-04 08:45 UTC) — selesai
- Permintaan: audit jilid 12, seluruh area lebih agresif (tanpa patch).
- Cakupan: `checkAndSendNewData`/`sendInitialData` progresif, `fetchLocation` (`removeUpdates` di `finally` benar), `registerBotCommands` (hanya sekali saat start), `sendDropNotice`, `getNewCalls` komposit, `MessageQueue` prune/snapshot, `sendStatusNow`, lifecycle FGS, regresi `v1.6.63`.
- Temuan baru (8, belum diperbaiki): (1) DUPLIKAT `numberMatches`/`numbersEqualFast` di `MonitoringService` tak ikut gate >= 9 digit v1.6.62 + tanpa cek `==` dulu — filter akhir `/history` bobol privasi sufiks; plus `idVariants` dead code; (2) menu owner tak re-register sampai restart usai `rememberOwner`; (3) `sendDropNotice` sample tak di-escape + `parseMode` default HTML — notif drop bisa 400 hilang diam; (4) `sendFitted` gandakan antrean per-part saat auth gagal; (5) `pruneVolatileLocked` drop kedaluwarsa tanpa counter/notice; (6) residual replay crash antara handle & persist offset (perintah non-idempoten bisa ganda); (7) `BootReceiver` unlock rutin picu thread+IO tiap buka kunci (throttle 60 dtk, boros ringan); (8) `sendStatusNow` direct tanpa antre (gagal = hilang, hanya toast).
- Koreksi audit: `fetchLocation` tak bocor; `getNewCalls` komposit benar; `registerBotCommands` scope serialisasi benar.
- Validasi: XML OK, secret bersih, tanpa perubahan kode repo ini.
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.64` bila ya).

## Sesi #22 (2026-10-04 08:40 UTC) — selesai
- Permintaan: perbaiki semuanya (8 temuan audit jilid 11).
- Perbaikan: baris Owner + petunjuk DM di status Setup; alert Telegram saat admin dinonaktifkan; buang eksklusi backup basi; deskripsi admin jujur `force-lock`; `/stop` sebut notif ikut pause; cancel audio usai-sukses antre notif via `audioOutcome`; cek paket update equals; channel tak dihapus; fallback `/history` `100`.
- Validasi: XML semua OK, brace/paren 7 file seimbang, grep secret bersih, tanpa Gradle lokal.
- Rilis: commit `f64494a` + bump `versionCode` 90/`1.6.63` + tag `v1.6.63` (`40f1c52`), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.63` rilis, menunggu hasil CI.

## Sesi #21 (2026-10-04 08:36 UTC) — selesai
- Permintaan: audit jilid 11, seluruh area lebih agresif (tanpa patch).
- Cakupan: `ParentalMonitorApp`, `AdminReceiver`, `TelegramApi` (semua `SerializedName` lengkap), kalkulator+jalur rahasia, `refreshLoopConfig`/cache, `sendInitialData`, handler `/stop`-`/lock`, `NotificationForwarderService` (revive hormati opt-out), `MessageQueue` (terkunci konsisten), audio/ring `finally`, `stop/startMonitoringConfirmed`, XML `network_security`/`backup`/`device_admin`, `SYNC_INTERVAL`, `onDestroy`/`onTaskRemoved`/`handleFgsTimeout`, regresi `v1.6.62` (aman: replay callback dicover dedup `update_id`, sub-`ping` tetap owner-only).
- Temuan baru (8, belum diperbaiki): (1) owner-learning implisit — grup-only terkunci sampai DM privat pertama, tanpa petunjuk Setup; (2) `onDisabled` admin tak lapor owner (buta pra-uninstall); (3) eksklusi backup basi (`secure_prefs_fallback`, `message_queue`); (4) `device_admin.xml` hanya `force-lock` vs deskripsi over-claim; (5) `/stop` ikut hentikan forward notif diam-diam; (6) cancel usai kirim audio hilangkan notif sukses; (7) cek `MY_PACKAGE_REPLACED` pakai `contains` bukan equals; (8) recreate channel hapus setelan channel pengguna + fallback `/history` 200-row boros.
- Koreksi audit: tak ada bypass baru; semua revive hormati opt-out; `SYNC_INTERVAL` kosong aman default `5`.
- Validasi: XML semua OK, grep secret bersih, pola token live nihil, tanpa perubahan kode repo ini.
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.63` bila ya).

## Sesi #20 (2026-10-04 08:33 UTC) — selesai
- Permintaan: perbaiki semuanya (9 temuan audit jilid 10).
- Perbaikan 8 + 1 koreksi: callback tap=kini (`0L`) + runtuh cabang mati + jawab spinner saat drop; reset offset tiap `400` ber-offset; `/ping` polos keluar `SENSITIVE` (sub-camera/location tetap owner-only); sufiks `endsWith` hanya >= 9 digit di `SmsRepository`+`CallLogRepository`; SMS timeout per-part + lapor parsial `x/y` + `failCount`; toast `setup_superseded` ganti gugur diam; fallback param URI `limit` sebelum full-scan; potong entity-safe `CrashReporter`.
- Koreksi audit: `activePhotoFile` ternyata sudah `finally`-null, tanpa perubahan; slot ke-9 diisi hardening potong entity `CrashReporter`.
- Validasi: XML 5 file OK, brace/paren 5 file seimbang, grep secret bersih, tanpa Gradle lokal.
- Rilis: commit `052e6d0` + bump `versionCode` 89/`1.6.62` + tag `v1.6.62` (`060e2f9`), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.62` rilis, menunggu hasil CI.

## Sesi #19 (2026-10-04 08:31 UTC) — selesai
- Permintaan: audit jilid 10, seluruh area lebih agresif (tanpa patch).
- Cakupan: `MonitoringService` (gate callback, expiry 900 dtk, offset 400, `/history` suffix, SMS multipart, loop kamera/auth, `registerBotCommands` hash), `NotificationForwarderService` (escape HTML, history 20), `SendMessageWorker`/`BootRestartWorker` (retry vs success), `SetupActivity` save/test seq, `SmsRepository`/`CallLogRepository` (`LIMIT` OEM), `MainActivity` stealth, `CrashReporter` (finally reset benar), `TelegramApi` dispatcher `6`/`4`, proguard keep, manifest, workflow.
- Temuan baru (9, belum diperbaiki): (1) tombol inline kedaluwarsa 15 mnt (`msgDate` pesan lama vs `COMMAND_MAX_AGE_SEC`); (2) offset 400 brick (reset hanya bila `cur<0`, tak pernah tercapai); (3) `handleCallbackQuery` cabang `MUTATING` identik mati + spinner gantung saat drop diam; (4) menu publik `/ping` vs gerbang `SENSITIVE` tak sinkron; (5) `/history` suffix `endsWith` 7 digit bisa cocok nomor asing; (6) SMS multipart non-atomik (1 part gagal = lapor gagal total, retry = duplikat + biaya); (7) balap Save-vs-Test diam-diam gugur tanpa toast; (8) `LIMIT` via `sortOrder` di OEM tak support = full-scan + spike memori; (9) `activePhotoFile` bocor bila capture batal = file zombie dikecualikan prune selamanya.
- Koreksi audit: dugaan bypass owner via callback GUGUR (gate dalam tetap `senderOk`); dugaan cache foto unbounded saat auth-blocked GUGUR (`captureAndSendPhoto` gate `authBlocked`); dugaan `flushing` macet GUGUR (`finally` reset ada); dispatcher/proguard/consent sudah benar.
- Validasi: XML 4 file OK, grep secret bersih (hanya `KEY_` + regex), pola token live nihil, tanpa perubahan kode repo ini.
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.62` bila ya).

## Sesi #18 (2026-10-04 08:09 UTC) — selesai
- Permintaan: perbaiki semua temuan audit jilid 9.
- Perbaikan 10: keystore tag jadi warning; Setup kecualikan `POST_NOTIFICATIONS`; Save/Test cross-invalidate; `scheduleMessageSendCoalesced` (`KEEP`) untuk cooldown auth + `APPEND` untuk rate-limit; `authBlocked`+`CrashReporter` hormati `400`; `README` nama debugsigned; pause basi >`480` mnt dibuang; chunk berhenti di gagal pertama; `tools:targetApi` `35`; reskala speed per-counter.
- Koreksi audit: Test-ikut-save dan tier GB `NetSpeed` ternyata sudah benar, tanpa perubahan.
- Rilis: commit `ba0cb97` + tag `v1.6.61` (`versionCode` 88), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.61` rilis, menunggu hasil CI.

## Sesi #17 (2026-10-04 08:06 UTC) — selesai
- Permintaan: audit jilid 9, lebih agresif seluruh area (tanpa patch).
- Cakupan: regresi `v1.6.60` (offset-reset, callback `1L`, boot-SDK, operator secret, dispatcher `6`/`4`, `APPEND`, busy-reset, `lastSyncTime`, notif `400`, kursor chunked, forwarder `BIG_TEXT`, foto `.tmp`), `ParentalMonitorApp`, `AdminReceiver`, `AppPermissions`, `SpeedMonitorActivity`, `NetSpeed`, `CrashReporter`, `BootRestartWorker`, `SendMessageWorker`, `SetupActivity` save/test, `SmsRepository`, manifest, workflow, `app/build.gradle`, `README`, `builder.sh`.
- Koreksi klaim: `CrashReporter` hormati blokir auth (cek `401`/`403` ada); `builder.sh` sudah ada banner legacy.
- Temuan baru: tag tanpa keystore (`assertReleaseKeystore` vs fallback debugsigned); nama artefak workflow vs `README`/`CHANGELOG`; gate `POST_NOTIFICATIONS` Setup vs Main; test sukses ikut `saveCoreConfig` (reset offset sebelum Save eksplisit); `APPEND` + delay 30 mnt head-of-line; worker/`CrashReporter` abaikan `400`; sisa OEM stale-pause; duplikat chunk worker; balap save/test seq; `tools:targetApi` basi; kosmetik speed.
- Validasi: XML OK, grep secret bersih, tanpa perubahan kode repo ini.
- Status terakhir: menunggu keputusan owner perbaiki mana dulu (usul `v1.6.61` bila ya).

## Sesi #16 (2026-10-04 08:00 UTC) — selesai
- Permintaan: audit jilid 8 lebih agresif seluruh area, lalu perbaiki semuanya.
- Audit jilid 8: 14 temuan (2 dikoreksi tidak jadi bug: owner-learning ternyata hidup karena `rememberOwner` di luar gerbang `chatOk||ownerOk`; fallback `400` ke plain ternyata sudah tangani `401`/`403`).
- Perbaikan 12: reset offset `lastUpdateId`/`wakeUpdateId` + wake ping saat ganti token/chat; fallback tanggal callback sensitif `1L`; reset foto hanya boot nyata; secret kalkulator hanya `1234` + `=`; dispatcher `6`/`4` + pool `6` dan media `4`/`2`; `scheduleMessageSendNext` `APPEND`; reset 5 busy flag saat stop/FGS timeout; `lastSyncTime` khusus SMS/panggilan; notif lokal `Chat not found (400)`; kursor `checkAndSendNewData` progresif per chunk 10; forwarder `BIG_TEXT`/`TEXT_LINES`/`SUB_TEXT` + tanpa record spam; foto via `.tmp` + rename atomik + prune `.tmp` basi.
- Rilis: commit `70a847d` + tag `v1.6.60` (`versionCode` 87), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.60` rilis, menunggu hasil CI.

## Sesi #15 (2026-10-04 07:40 UTC) — selesai
- Permintaan: perbaiki semua 14 temuan audit jilid 7 + gagal build.
- Akar gagal build: import `TelegramMediaClient` hilang di `MonitoringService` sejak `v1.6.57` (`Unresolved reference`, 2 titik); build `v1.6.56` terakhir hijau.
- Perbaikan: import + 14 temuan (ping terkompensasi tanpa restart ganda; kursor kondisional; reset jeda foto saat unlock; gate flush foto; paging 500 + kabar setup kosong; reset kamera saat FGS timeout; throttle SMS saat konfirmasi; prefs IO-background; menu bot scope owner; flush crash hormati blokir auth; drop forwarder tercatat; `lastSyncTime` khusus data).
- Rilis: commit `49f6c0a` + tag `v1.6.59` (`versionCode` 86), push main + tag; build + GitHub Release oleh workflow.
- Status terakhir: `v1.6.59` rilis, menunggu hasil CI.

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
