# Memori Sesi — Tasirin Download Manager

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-download-manager` — download manager Android (Kotlin, minSdk 21, targetSdk 36).
- Aturan main (ringkas dari `AGENTS.md`): build resmi HANYA via CI, DILARANG install SDK lokal; UI Inggris, komentar Indonesia; commit `type(scope): deskripsi`; jangan ubah `versionName`/`versionCode` manual (CI bump per run); sumber remote web = `remote.src.html` + `python3 scripts/prepare_remote.py` (jangan edit `assets/remote.html` manual); guard `scripts/check_repo.py` + `scripts/security_audit.py`; perubahan kode wajib entri `CHANGELOG.md`; setelah fix langsung push tanpa pantau workflow (aturan 19).

## Status terakhir (2026-10-07, HEAD a0a7177 — loop perintah chat jilid 33-38: 1 fix + 5 bersih berturut-turut = STOP)

- Loop perintah `/root/chat.md` jilid 33-38 (HEAD a0a7177, push main sukses, guard `security_audit` 0/0 + `git diff --check` bersih):
  - Jilid 33 (Settings/Prefs/Crypto/Service/Boot/Repository/Notif/App/Cleanup): 1 temuan layak-fix — `StorageCleanup.lastRunElapsed = 0` berarti "baru jalan saat boot" sehingga 5 menit pertama pasca-reboot `runIfLow()` selalu ter-throttle padahal belum pernah jalan (tepat saat autostart-boot paling butuh); kini `-MIN_INTERVAL_MS` + `isThrottleOpen()` murni + `StorageCleanupTest`. Commit `a0a7177 fix(storage): pembersihan storage boleh jalan langsung setelah boot` + CHANGELOG. Bersih: PinHash PBKDF2/parse/verify, `setServerPin` unchanged-rotate, session-secret DCL, `persistItems` lock ordering, Boot trampoline, `resumeInterrupted` in-memory, notif thread-safe.
  - Jilid 34 (FileSaver/MediaLibrary/Updater): BERSIH — merge staging+rename+parts-hanya-saat-sukses, sweeper `.merge.` covered, `rename`/`move`/`uniqueTargetFile` klaim-atomik, `destinationFreeBytes` multi-volume, observer DCL+flag-saat-sukses, `scanCacheUsable`, token cap 4096, Updater list-first/`getOrElse`/512KB-cap/redirect-credential-strip.
  - Jilid 35 (MainActivity dialog + DownloadAdapter): BERSIH — probe stale-guard (job-identity + URL-compare), dismiss batalkan job, DiffUtil payload mencakup semua field static-bind, `smoothProgress` direct-set tanpa animator.
  - Jilid 36 (ServerSecurity/ShareToken/ServerStreams): BERSIH — HMAC domain-separated (`partial:`/`upload:`), redaksi log mencakup semua param secret aktual (pin/token/verify/zt/password), canonical-path roots, cookie parse per-segmen, SAF prefix-check, `ChainInputStream` fd-close inline.
  - Jilid 37 (DownloadEngine inti): BERSIH — mirror-switch terminasi (drop+failedUrl filter), yt-403 fail-fast, failedUrl LRU-bound, throttle total-di-luar-lock, watchdog slowSince-reset, invalidate-resume ETag.
  - Jilid 38 (SocialMediaExtractor): BERSIH — brace-matcher gagal-aman, regex bounded, redirect manual + allowlist + strip kredensial lintas-host, `readBodyLimited`, cookie tak diteruskan lintas-origin di `isUrlForbidden`.
  - STOP: 5 jilid bersih berturut-turut (34-38) + putaran penuh modul utama tersapu (26-38). Loop selesai; sesi berikut mulai jilid 39 bila ada perintah baru.

- Diskusi-diri jilid 32 (DownloadEngine `handleFailure`/mirror/segmen + HttpControlServer map/cache/endpoint + WebExtract/Gallery/Log lifecycle + `saveVideoPos`): 1 temuan layak fix — `refreshExpiredCdnUrl()` membuka validasi HEAD di luar `try` sehingga blip jaringan meledak keluar handler Range-reject, melewatkan fallback satu-alur, lalu retry-Range berulang sampai FAILED; kini gagal-buka = null. Area lain bersih (mirror-switch ber-guard PENDING, upload-lock bound ganda, galleryJson clamp page, WebExtract onDestroy, GalleryActivity main-thread-only, LogActivity removeCallbacks). Commit `28ff854 fix(download): validasi HEAD URL segar tak boleh melempar` + CHANGELOG. Guard: `security_audit` 0/0, `git diff --check` bersih.

- Audit jilid 31 (mode baca-saja, HEAD 37e8ca8): 3 temuan baru — (1) `trimGalleryTop()` baca-tulis selang-seling per cell (layout thrash); (2) `thumbPending` Array O(n) + tumpuk ref saat fling; (3) `notifyItemFinished()` requestCode unik per unduhan (PendingIntent menumpuk).
- Fix + push sukses: `028082d perf(gallery): scroll jank susulan windowing` (dua pass trim + `thumbPending` jadi `Set`, regen `remote.html`, +CHANGELOG) dan `4da4aa4 fix(notification): PendingIntent selesai menumpuk per unduhan` (requestCode stabil 0, +CHANGELOG). Guard: `security_audit` 0/0, `prepare_remote --check` OK, `git diff --check` bersih.

- HEAD: `004f63c` docs(agents) kunci prefs.
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


## Sesi audit jilid 11 (2026-10-03 13:54 UTC, commit 99b65d6, push main sukses)

- Perintah user: "cek seluruh kode temukan bug" — audit menyeluruh ke-11.
- 3 race diperbaiki:
  1. `remote/ServerThumbnail.kt` — eviksi + `getOrPut` dalam satu `synchronized(thumbLocks)` (eviksi luar lock bisa buang lock baru → decode ganda + JPEG interleave korup).
  2. `download/DownloadEngine.kt` — `scheduleSegFlush()` kunci sempit `segFlushJobs` bukan `synchronized(this)` + hapus job SEBELUM flush (lock global = jank, record susulan hilang).
  3. `remote/HttpControlServer.kt` — `pruneLoginAttempts()` dalam `synchronized(loginAttempts)` (minBy+remove luar lock bisa buang entry baru → throttle lolos).
- Guard: `security_audit.py` 0 error/0 warning; `git diff --check` bersih; `check_repo --pre-commit` full run tertunda sesi (satuan cepat hijau). Push main sukses tanpa pantau workflow (aturan 19).
- Pola langganan baru: eviksi cache di luar lock pembuatan → pindahkan ke dalam lock yang sama; hapus-job-setelah-flush → hapus-sebelum-flush; prune tanpa lock → samakan lock dengan writer.


## Sesi remote lanjutan (2026-10-03 14:05 UTC, commit e20f925, push main sukses)

- Perintah user: "lanjutkan" — audit `remote.src.html` (6584 baris).
- Guard lama utuh: `fmtDate` tunggal, handler `tabDownloads` ada, argumen `uploadFiles()` urut, `resetFileProgress()` + `postFsAction` rethrow + SSE counter + select-mode in-place (tanpa `reRenderGalleryLoaded`). `prepare_remote --check` + smoke upload hijau.
- 1 bug baru diperbaiki: `loadGallery()` naikkan tiket sebelum guard → panggilan drop ikut naikkan tiket + bersihkan flag prematur → dua fetch halaman sama paralel + `concat` ganda (galeri duplikat). Tiket naik hanya setelah lolos guard. `remote.html` diregenerasi via `prepare_remote.py`.
- Guard: `security_audit` 0/0, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).


## Sesi server lanjutan (2026-10-03 14:15 UTC, commit 2f73ff4, push main sukses)

- Perintah user: "lanjutkan" — audit `HttpControlServer` (3279 baris) + `ServerSecurity` (277) + upload/stream/share.
- Jalur login/throttle/token/redaksi/header aman: PIN hash + cookie acak, throttle per-IP, token parsial HMAC, redaksi log, CSP. `ServerSecurity` tetap murni + unit test, tanpa duplikasi di server.
- 1 bug diperbaiki: `writeUploadChunk()` catch-all balas keep-alive saat body setengah terbaca → sisa byte meracuni request berikut. Kini `closeConnection()` seperti jalur error lain.
- Guard: `security_audit` 0/0, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).


## Sesi engine lanjutan (2026-10-03 14:30 UTC, commit 5627326, push main sukses)

- Perintah user: "lanjutkan" — audit `DownloadEngine` (3642 baris) + `FileSaver` + `SegmentPlanner`/`SpeedTracker`/`QueueOrder` + `DownloadRepository` + `DownloadService`.
- Yang dicek dan aman: resume/ETag, Range-reject + CDN refresh, mirror GitHub, watchdog, redirect SSRF, finalize guards, merge staging, orphan sweep, antrean prioritas, wake lock, throttle persist.
- 1 hardening: `DownloadRepository.saveProgress()` tanpa lock bisa commit sebelum snapshot penuh yang di-encode lebih dulu (lalu terhapus) → byte mundur satu tick. Kini `@Synchronized` satu monitor dengan `persistItems`/`load`.
- Guard: `security_audit` 0/0, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).


## Sesi galeri lanjutan (2026-10-03 14:40 UTC, commit 50dda62, push main sukses)

- Perintah user: "lanjutkan" — audit `MediaLibrary` (701) + `GalleryActivity` (434) + `ServerThumbnail` + `ServerVideoDurations`.
- Yang dicek dan aman: cache scan TTL + lock, dedupe path, fallback filesystem, observer seumur proses, LRU thumbnail + lock per media, staging thumbnail, tanggal main-thread, izin baca intent.
- 1 bug diperbaiki: job thumbnail `GalleryAdapter` hanya cek posisi — job lama lolos cancel bisa timpa cell yang rebind ke item lain di posisi sama (flash gambar tetangga). Kini cek token juga.
- Guard: `security_audit` 0/0, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).


## Sesi ekstraksi lanjutan (2026-10-03 14:50 UTC, commit 59620ce, push main sukses)

- Perintah user: "lanjutkan" — audit `WebExtractActivity` (295) + `SocialMediaExtractor` (1476) + `extract.js`.
- Yang dicek dan aman: kunci skema http(s), blokir navigasi luar host (batas dot), tanpa JS bridge, cookie host final, redirect manual + buang kredensial lintas host, blokir host berbahaya, batas body 16MB, header user first-party saja, regex domain presisi.
- 1 bug diperbaiki: `extract()` tanpa batas total (rantai fallback menahan worker), `extractAll()` sudah 60 detik. Kini sama via `withTimeoutOrNull`, timeout = null.
- Guard: `security_audit` 0/0, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).


## Sesi prefs lanjutan (2026-10-03 15:00 UTC, commit 004f63c, push main sukses, docs-only)

- Perintah user: "lanjutkan terus" — audit `SettingsActivity` (986) + `StoragePrefs` (486) + `Updater` (182).
- Yang dicek dan aman: cache prefs app-context, secret acak 256-bit, rotasi sesi saat PIN berubah, migrasi hash lama, clamp semua angka, save tunggal anti ganda, cek-saja update via browser.
- 1 drift diperbaiki (docs-only, tanpa build): daftar kunci aktif di `AGENTS.md` memuat `recent_urls` + `sort_mode` yang sudah tak ada di kode (nol referensi), dan kehilangan `auto_open_on_complete` + `user_agent` + `gallery_folders` yang hidup. Kini 32 kunci sinkron.
- Guard: `security_audit` 0/0, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).


## Sesi sapuan luas (2026-10-03 15:15 UTC, tanpa commit kode — bersih)

- Perintah user: "jangan satu satu" — audit SEKALIGUS semua sisa: `App` + `MainActivity` (1735) + `LogActivity` + `DownloadAdapter` + `DownloadService` + `BootReceiver`/`BootResumeJobService` + `ShareToken`/`ServerLog`/`HttpBody` + `NotificationHelper` + `Crypto`/`PinHash` + manifest/permissions.
- Verdict: BERSIH, tanpa perbaikan. Yang diverifikasi: init background + callback GC-safe, SEND/URL extract, dialog probe anti-basi, installer 3 fallback, ekspor log tanpa yatim/0-byte, adapter main-thread + tanpa animator, wake lock refcount-off + release, job boot API 35, redaksi token log, batas body 4MB + drain/close disiplin, PendingIntent immutable, enkripsi GCM + prefix eksplisit, PBKDF2 clamp iterasi, izin manifest lengkap (termasuk RECEIVE_BOOT_COMPLETED untuk job persisted).
- Guard: `security_audit` 0/0 (dari sesi sebelumnya, kode tak berubah). Tanpa push main (tak ada perubahan).

## Tugas terbuka

- [x] `check_repo.py` 10/10 hijau; push ke `main` sukses (tidak pantau workflow).
- [ ] Pastikan CI Build APK hijau pasca-push (a46de8d).
- [x] Soul lintas-repo: user minta 1 soul nyambung semua repo — ternyata sudah ada (`SOUL.md` + 4 memori + pointer `AGENTS.md` di 4 repo). Perbaiki 1 yang belum sinkron: `AGENTS.md` download-manager belum baca `SOUL.md` (commit a133b8f, docs-only, push sukses tanpa pantau workflow).

## Pola bug langganan (jangan ulangi)

- Eviksi di luar lock pembuatan → eviksi + getOrPut satu lock.
- Hapus job setelah flush → hapus sebelum flush + reschedule otomatis.
- Prune tanpa lock → synchronized sama dengan writer.

- Cache dua field volatil bisa sobek → satu holder `Pair` atomik.
- `getOrPut` Kotlin tak atomik di `ConcurrentHashMap` → `synchronized` eksplisit.
- `SimpleDateFormat` tak thread-safe → `ThreadLocal` / dalam lock.
- `LongArray` lintas thread → `AtomicLongArray` / snapshot di dalam lock.
- `getOrNull() ?: cache` mengubah null-sukses jadi cache basi → `getOrElse`.
- Total dihitung setelah `take()` → total dari distinct penuh SEBELUM `take()`.

## Sesi soul lintas-repo (2026-10-03)

- Verifikasi: 4 repo (`tasirin-download-manager`, `tasirin-vaultwarden-host`, `Red-Eye-Mobile`, `netradar`) semua pointer `AGENTS.md` sudah ke `memori-agents-ai` + `SOUL.md`; hanya download-manager yang tertinggal satu kata (`SOUL.md`) di working tree — sudah di-commit/push (a133b8f).
- Tidak ada perubahan `SOUL.md` — identitas tetap sudah tepat.

## Sesi gaya sederhana (2026-10-03)

- User minta semua penjelasan dibuat sederhana, tidak terlalu teknis — `SOUL.md` bagian Gaya bicara ditambah aturan bahasa sehari-hari + analogi sederhana.

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

## Sesi audit sapuan penuh (2026-10-03 23:49 UTC, tanpa ubah kode — temuan minor)

- Perintah user: "cek seluruh kode temukan bug" — sapuan semua area: `DownloadEngine` (jobs/segProgress/throttle), `HttpControlServer` (upload chunk + reservasi + lock + itemsJson/SSE), `FileSaver` (merge staging + unique claim), `MediaLibrary`/`ServerThumbnail` (cache/TTL/lock), `ServerSecurity`/`HttpBody`/`ZipCreator`/`ServerLog`, `Updater`, `DownloadRepository`, `StoragePrefs`, `DownloadService`, `GalleryActivity`, `MainActivity` dialog probe, `WebExtractActivity`, `remote.src.html` (SSE/tab/upload/fmtDate), `BootResumeJobService`.
- Guard: `security_audit` 0 error / 0 warning; area berat (race/throttle/upload-lock/galeri-total/staging-merge) sudah bersih dari sesi sebelumnya.
- Temuan baru (semua minor, BELUM diperbaiki — tunggu pilihan owner):
  1. `DownloadEngine.importStream` mencatat `length` deklarasi sebagai `bytesDownloaded/totalBytes`; upload single-shot chunked (length 0) tampil 0 byte. Fix: stat ukuran file hasil publish.
  2. `HttpControlServer.handleUpload` menerima `chunk` negatif selain -1 (mis. -5) sebagai single-shot diam-diam; harusnya ditolak eksplisit. Fix: validasi `chunkIdx < -1`.
  3. `App.onCreate` menulis cap `thumb_cleanup_last` walau `cleanupOldThumbs` gagal; gagal bersih tak dicoba lagi 7 hari. Fix: update cap hanya bila sukses.
- Tanpa push ke `main` (tak ada perubahan kode); guard `check_repo.py` tak selesai dibaca penuh sesi ini (hanya `security_audit` yang terkonfirmasi hijau).

## Sesi fix sapuan jilid 12 (2026-10-04 00:17 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 5 temuan jadi 1 commit `73ea48f` (satu tujuan: temuan sapuan jilid 12) + 5 entri `CHANGELOG.md` + unit test baru `SseStreamTest` (2 test).
- Fix: (1) `sseJob = null` di dalam `ssePumpLock` + cek identitas (exit pump & `stopServer`, urutan lock aman); (2) guard baca 0-byte 32x beruntun di `readForm`/`drainBody`/`copyUploadBody` (`HttpBody`, konstanta `MAX_ZERO_READS`); (3) `serveShare` prune+baca dalam `shareLock`; (4) `SseStream.wakeBlockedReader()` + `SseStreamTest`; (5) `scannedGallery` pakai `elapsedRealtime`.
- Guard: `security_audit` 0/0, `check_readme_sync` sinkron, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).

## Sesi sapuan penuh jilid 12 (2026-10-04 00:06 UTC, tanpa ubah kode — 2 minor + 3 catatan)

- Perintah user: "cek seluruh kode temukan bug" — sapuan semua file: `HttpControlServer` (serve/auth/throttle/upload-chunk/finalisasi/fs/galeri/share/partial/SSE/zip/login), `DownloadEngine` (resume/segmen/HLS/watchdog/throttle/muxer/ADTS), `FileSaver`, `MediaLibrary`, `ServerSecurity`, `ServerThumbnail`, `ServerVideoDurations`, `DownloadRepository`/`DownloadItemCodec`, `StoragePrefs`/`PinHash`/`Crypto`, `Updater`, `App`/`DownloadService`/`BootReceiver`/`BootResumeJobService`, `MainActivity` (probe/openApk), `GalleryActivity`, `SettingsActivity` (PIN/port), `LogActivity` (ekspor), `WebExtractActivity`/`extract.js`, `remote.src.html` (SSE/upload/galeri/fs), `ZipCreator`/`HttpBody`/`ServerLog`/`SseStream`/`MediaStream`/`ServerStreams`, `QueueOrder`/`SegmentPlanner`/`SpeedTracker`, `StorageCleanup`, `NotificationHelper`.
- Temuan (BELUM diperbaiki — tunggu pilihan owner):
  1. (minor-real) `HttpControlServer`: `sseJob = null` di luar `ssePumpLock` (jalur exit pump + `stopServer`) — balapan bisa bikin pump ganda / pump yatim tak terlacak. Fix: null-kan di dalam lock dengan cek identitas `=== me`.
  2. (minor-teoretis) `HttpBody`: loop baca `readForm`/`drainBody`/`copyUploadBody` tak menangani `read() == 0` — kontrak InputStream membolehkan 0 sehingga thread HTTP bisa busy-loop selamanya; di socket blocking praktis tak terjadi. Fix: hitung nol beruntun lalu IOException/closeConnection.
  3. (catatan) `serveShare` memanggil `pruneShares()` tanpa `shareLock` (tempat lain pakai lock) — CHM aman dari crash, sekadar inkonsistensi.
  4. (catatan) `SseStream.push` saat antrean penuh menandai tutup tapi tak membangunkan `poll` 25 dtk — teardown SSE bisa telat sampai 25 dtk.
  5. (catatan) `scannedGallery` pakai wall-clock untuk TTL 15 dtk sementara `MediaLibrary` monotonik — lompatan jam bikin cache basi sebentar.
- Yang diverifikasi bersih: signature/cache `itemsJson` (immutable + list baru tiap update, `===` aman), resume/ETag/Range-reject+CDN-refresh, merge staging, throttle/watchdog, upload reservasi+lock+finalisasi background, PIN PBKDF2 + cookie sesi acak, `isPathAllowed` sudah kanonikal di dalam (serveMedia aman), ZigZag ZIP/symlink/depth/budget, galeri total/dedupe/TTL, probe basi dialog, openApk 3 fallback, ekspor log tanpa yatim, wake lock, boot job, muxer/ADTS.
- Guard: `security_audit` 0/0. Tanpa push (tak ada perubahan kode).

## Sesi tombol remote lanjutan (2026-10-04 00:06 UTC, push main sukses)

- Perintah user: "lanjutkan" — audit saudara bug `moveHere` (commit 96b8c0a) di `remote.src.html`: semua situs `disabled = true` dicek satu per satu.
- 1 bug sekeluarga ditemukan & diperbaiki (commit 005f1c8): `fsLoadMore()` hanya mengaktifkan lagi tombol di jalur error — load-more sukses yang masih menyisakan halaman, dan respons basi (`seq !== fsLoadSeq` saat navigasi di tengah fetch), membuat tombol "Load more" lumpuh sampai reload. Kini tombol dipulihkan di `finally` selama masih menempel di DOM (`isConnected`; tombol yang di-remove karena tak ada sisa dilewati).
- Yang dicek dan aman: `runFsActions`/`fsTaskCancelBtn` (diaktifkan lagi tiap `showFsTask`), tombol upload (callback + catch), `moveYes` (sudah `finally` di 96b8c0a).
- Guard: `prepare_remote --check` OK (sinkron + JS valid + UI Inggris + smoke upload), `security_audit` 0/0, `check_readme_sync` sinkron, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).

## Sesi fix 3 temuan minor (2026-10-04 00:05 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 3 commit terpisah (satu tujuan per commit) + entri `CHANGELOG.md` tiap commit, push `main` `004f63c..00a903f` tanpa pantau workflow (aturan 19).
- Commit: `0bace1c` fix(download) ukuran importStream dari stat file asli; `dd5acde` fix(server) tolak `chunk < -1`; `00a903f` fix(app) cap thumb-cleanup hanya bila sukses.
- Guard: `security_audit` 0/0, `check_repo.py` 10/10 SEMUA SEHAT.

## Sesi sapuan penuh jilid 13 (2026-10-04 01:00 UTC, tanpa ubah kode — 2 minor + 2 catatan)

- Perintah user: "cek seluruh kode temukan bug lagi" — sapuan semua file: `HttpControlServer` (upload-chunk/offset/itemsJson/galeri/login/zip), `DownloadEngine`, `FileSaver`, `MediaLibrary`, `ServerSecurity`, `Updater`, `TlsCompat`, `DownloadRepository`/`DownloadItemCodec`, `MainActivity`, `GalleryActivity`, `LogActivity`, `SettingsActivity`, `WebExtractActivity`, `SocialMediaExtractor`, `remote.src.html` (tombol/fs/galeri/upload).
- Temuan (BELUM diperbaiki — tunggu pilihan owner):
  1. (minor) `HttpControlServer.writeReservedUploadChunk`: 2 jalur reject (`invalid offset`, `invalid upload range`) tanpa `drainBody` langsung `closeConnection` — benar tak desync, tapi bunuh keep-alive sia-sia + klien berisiko tak baca JSON error bersih (jalur tetangga semuanya drain dulu).
  2. (minor) `serveGallery` `hasMore` salah di halaman terakhir hasil filter `q`: `matched < scan.total` membandingkan hitungan terfilter vs total tanpa filter → fetch halaman kosong sia-sia sekali. Fix: bila `q` non-kosong, `hasMore = matched > pageEnd`.
  3. (catatan/cleanup) `itemsJson`: `else if (oldObj.has("error")) oldObj.remove("error")` dead branch — `oldObj` objek baru, tak pernah punya `error` basi (tak ada bug fungsional, komentar menyesatkan).
  4. (catatan/teoretis) `TlsCompat` fallback `extraTm.checkServerTrusted` hanya lawan 3 root bundle, bukan gabungan system+extra — rantai cross-signed yang butuh keduanya tetap gagal; plus exception asli system hilang.
- Yang diverifikasi bersih: reservasi buffer upload + finally, lock upload atomik, login throttle per-IP, zip strip-lock, signature/cache itemsJson, resume/ETag/CDN-refresh, merge staging, watchdog/throttle, PIN PBKDF2 + cookie sesi acak, `uploadUniqueName` traversal-safe, tombol remote (`fsLoadMore`/`moveYes`/upload sudah `finally`), `Updater` (bufferedReader default UTF-8 Kotlin, cache 24 jam), `scanCacheFolderKey` di dalam `scanLock`.
- Guard: `security_audit` 0/0. Tanpa push repo (tak ada perubahan kode).

## Sesi fix 4 temuan jilid 13 (2026-10-04 01:10 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `005f546` (precedent `73ea48f`) + 4 entri `CHANGELOG.md`, push `main` sukses tanpa pantau workflow (aturan 19).
- Fix: (1) `writeReservedUploadChunk` 2 jalur reject kuras body dulu, tutup koneksi hanya bila kuras gagal; (2) `serveGallery` `hasMore = matched > pageEnd` bila `q` non-kosong; (3) hapus dead branch `oldObj.has("error")`; (4) `TlsCompat` satu store gabungan (salin anchor sistem + 3 root bundle), hapus import tak terpakai.
- Guard: `security_audit` 0/0, `check_repo.py --pre-commit` 10/10 SEMUA SEHAT, `diff --check` bersih.

## Sesi sapuan lanjutan jilid 14 (2026-10-04 01:20 UTC, push main sukses)

- Perintah user: "lanjutkan" — sapuan fokus area belum tersentuh: `SocialMediaExtractor` (httpGet/redirect/YouTube fallback), `SegmentPlanner`, `FileSaver.uniqueTargetFile`, redirect-safety tests.
- 2 bug ditemukan & diperbaiki (commit `362cf8d`, +2 entri `CHANGELOG.md`, push main tanpa pantau workflow):
  1. `extractYouTubeViaCobalt` loop-never-continues: `return ...?.let { return it }` membuat parse tanpa URL me-return null dari fungsi (loop 1 instance tak masalah hari ini, tapi logika salah vs pola Piped) — kini `val result` + lanjut bila null.
  2. `resolveInvidiousLatest` ikuti `Location` tanpa `isExtractRedirectAllowed` + `301..308` memakan 304/305/306 — kini kode redirect eksplisit + tolak target terlarang; + unit test metadata/samaran loopback di `SocialMediaExtractorTest`.
- Diverifikasi bersih: `SegmentPlanner` (total=1, coerce), `uniqueTargetFile` (klaim atomik), `httpGetWithCookies`/`httpPostJson` (sudah validasi + strip kredensial), `isUrlForbidden` (tanpa follow redirect).
- Guard: `security_audit` 0/0, `check_repo.py --pre-commit` 10/10 SEMUA SEHAT, `diff --check` bersih.

## Sesi sapuan total jilid 15 (2026-10-04 01:35 UTC, push main sukses)

- Perintah user: "cek seluruh area temukan bug" — sapuan total semua area: `App`/`DownloadService`/`BootReceiver`/`BootResumeJobService`, `DownloadEngine` (runDownload/runSingle/segmen/HLS/mux), `FileSaver` (publish/MediaStore/unique), `MediaLibrary` (scan/lock/observer), `Crypto`/`PinHash`/`StorageCleanup`, `DownloadAdapter`, `GalleryActivity`/`SettingsActivity`/`LogActivity`/`MainActivity.openApk`, `WebExtractActivity`, `SseStream`/`ServerStreams`/`ShareToken`/`ServerVideoDurations`/`HttpBody`/`ZipCreator`, `QueueOrder`/`SpeedTracker`, `Streams`, remote JS (upload-chunk/SSE/galeri/tombol).
- 1 bug ditemukan & diperbaiki (commit `03494c8`, +1 entri `CHANGELOG.md`, +2 unit test `StreamsTest`, push main tanpa pantau workflow): `readBounded` busy-loop pada `read() = 0` ( imports engine HLS probe, body ekstraktor, cache durasi, extract.js) — kini 32 nol beruntun = kembalikan parsial, selaras guard `HttpBody` jilid 12.
- Diverifikasi bersih (temuan nihil): FGS/job boot, wake lock, throttle notifikasi monotonik, resume/segmen/HLS staging, publish atomik + orphan-guard, scanLock + observer tunggal, AES-GCM + plaintext eksplisit, PIN PBKDF2, tombol remote + SSE give-up + upload retry/finalisasi, ChainInputStream fd, ZIP budget/symlink, ekspor log tanpa yatim.
- Guard: `security_audit` 0/0, `check_repo.py --pre-commit` 10/10 SEMUA SEHAT, `diff --check` bersih.

## Sesi sapuan jilid 16 (2026-10-04 01:50 UTC, push main sukses)

- Perintah user: "lanjutkan" ("cek seluruh area") — sapuan ulang semua area: dialog probe `MainActivity` (staleness guard OK), `WebExtractActivity`/`extract.js`, thumbs galeri/LruCache, section adapter/DiffUtil, SAF `FileSaver`, `ServerThumbnail` locks, `HlsParser.resolveUrl`, watchdog/throttle/mirror engine, `serveMedia`/`snapshot` server, `DownloadRepository` kredensial, `StoragePrefs` secret, SSE/upload/galeri remote.
- 2 minor diperbaiki (1 commit + 2 entri `CHANGELOG.md`, push main tanpa pantau workflow): (1) `saveToMediaStore` cek-duplikat + insert kini satu lock (nama kembar paralel tak mungkin dalam proses); (2) `scan()` teruskan `usedFallback` (invarian cache utuh).
- Diverifikasi bersih: probe basi, cookie WebView, DiffUtil payload, redirect manual + same-origin auth, batch pause/resume, PIN/session rotation, tombol/SSE/upload remote, fd ChainInputStream, ZIP budget, ekspor log.
- Guard: `security_audit` 0/0, `check_repo.py --pre-commit` 10/10 SEMUA SEHAT, `diff --check` bersih.

## Sesi sapuan agresif jilid 17 (2026-10-04 13:00 UTC, tanpa ubah kode — 1 bug + 3 catatan)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif" — sapuan semua file Kotlin + remote JS + guard: `AdtsAac`/`HlsMp4Muxer`/`HlsParser`/`QueueOrder`/`SpeedTracker`, `HttpBody`/`SseStream`/`ShareToken`/`MediaStream`/`ServerStreams`/`ServerLog`/`ServerThumbnail`/`ServerVideoDurations`/`ZipCreator`, `Checksums`/`Crypto`/`Hex`/`Streams`/`PinHash`/`FileNames`/`Formats`/`MimeTypes`, `StorageCleanup`/`CrashLog`/`NotificationHelper`, `DownloadService`/`BootReceiver`/`BootResumeJobService`/`App`, `DownloadItem`/`Codec`/`Repository`, `FileSaver` (merge/staging/unique/publish), `StoragePrefs` (PIN/secret), `DownloadEngine` (runSingle/runSegmented/downloadSegment/handleFailure/monitor/probe/import/estimate/HLS-plan), `HttpControlServer` (serve/pinOk/login/zip-token/share/serveFile/servePartial/serveMedia/galeri/SSE/fsAction), `MediaLibrary` (token/scan), `Updater`, `SocialMediaExtractor` (http/redirect/regex), `MainActivity` (socialJob), `GalleryActivity` (adapter), `LogActivity` (ekspor), `SettingsActivity` (junk-cleanup), `WebExtractActivity`, `DownloadAdapter`, `remote.src.html` (XSS/escaping), util kecil.
- Temuan (BELUM diperbaiki — tunggu perintah owner):
  1. (bug, medium-low) `DownloadEngine.estimateBytes` (:2212) overflow Long: `(bandwidth * totalUs) / 8_000_000` — 1 jam @8 Mbps = 2,88e19 > Long.MAX → estimasi negatif → totalBytes negatif di UI/SSE + cek storage pra-unduh lolos palsu. Sama di `estimateAudioBytes` (:2223, jebol >~20 jam) dan penjumlahan di :2136. Fix: bagi-dulu-kali-kemudian + saturasi (jadikan fungsi internal murni + unit test ala `HlsDurationTest`).
  2. (wart, low) Jalur tolak-dini tanpa baca body: login terkunci (`loginPage` tanpa `readForm`), CSRF-403, `unauthorized()` 401 untuk POST — respons keep-alive dengan body tak-terbaca = desync koneksi sekali untuk klien itu. Opsi fix: drain-or-close di jalur tersebut.
  3. (nit docs) Komentar `setServerPin` "PBKDF2-SHA256" vs implementasi `PBKDF2WithHmacSHA1` di `PinHash`.
  4. (catatan/teoretis) `AdtsAac.readExact` tanpa guard zero-read (pola `MAX_ZERO_READS` sudah ada di `HttpBody`/`Streams`); praktis aman (blocking stream tak return 0 untuk len>0).
- Dugaan gugur: `serveMedia` cabang `f:` pakai `absolutePath` — TERNYATA AMAN karena `ServerSecurity.isPathAllowed` mengkanonikalkan di dalam (sama proteksinya dengan `serveFile`).
- Diverifikasi bersih: budget cap + verifikasi Content-Range segmen, klaim atomik publish, PIN/session rotation, throttle login per-IP, token ZIP sekali pakai, share symlink-kanonikal, sanitasi nama + unik saat antre/rename, junk-cleanup aman (nama selalu tersanitasi), socialJob cancel + stale-guard, escaping XSS remote disiplin, WebView tanpa JS bridge + blokir navigasi luar host.
- Guard saat audit: `security_audit` 0/0, `check_repo.py` 10/10 SEMUA SEHAT.
- Koreksi angka saat fix: 1 jam = 3,6e9 us (bukan 3,6e12) — overflow mentah butuh BANDWIDTH raksasa dari playlist tak-terpercaya atau video sangat panjang; fix tetap sah sebagai hardening input tak-terpercaya.

## Sesi fix 4 temuan jilid 17 (2026-10-04 13:15 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 4 commit satu tujuan + entri `CHANGELOG.md` tiap commit, push `main` `24d0176..bde3ee5` tanpa pantau workflow (aturan 19).
- Commit: `4dd64aa` fix(download) estimasi HLS anti-overflow (`safeMulDiv`/`saturatingAdd` internal murni + `SafeMulDivTest` 6 test); `f0395db` fix(server) `closeConnection()` di tolak CSRF-403, 401, login-terkunci; `1cd7005` docs(app) komentar PBKDF2-HMAC-SHA1; `bde3ee5` fix(download) guard zero-read `AdtsAac.readExact`.
- Guard: `security_audit` 0/0, `check_repo.py` 10/10 SEMUA SEHAT, `diff --check` bersih.

## Sesi hotfix CI jilid 18 (2026-10-04 13:25 UTC, push main sukses)

- Pemicu: anotasi CI "Build APK exit 1" — `compileDebugKotlin` gagal `Unresolved reference 'values'` di `FileSaver.kt:258-260`, bawaan commit `24d0176` (klaim nama MediaStore atomik), bukan dari 4 commit jilid 17. Build `24d0176` sebelumnya juga sudah gagal untuk alasan sama.
- Fix (1 commit + entri `CHANGELOG.md`): `f1f176d` fix(app) `values` MediaStore keluar dari lock — `val values` dideklarasikan di dalam blok `synchronized` tapi dipakai setelahnya; kini `Triple(uri, unique, values)` didestruktur keluar lock.
- Guard: `security_audit` 0/0, `check_repo.py` 10/10 SEMUA SEHAT, `diff --check` bersih. Push `main` tanpa pantau workflow (aturan 19).

## Sesi sapuan agresif jilid 19 (2026-10-04 13:46 UTC, tanpa ubah kode — 3 temuan)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif" — sapuan penuh: `DownloadEngine` (Range/resume/ETag/CDN-refresh/watchdog/throttle/HLS/monitor/probe/redirect-SSRF), `HttpControlServer` (snapshot-throttle/itemsJson-signature/galeri/zip/share/upload/login/SSE/statPool), `FileSaver` (merge-staging/unique/publish/MediaStore), `MediaLibrary` (scan-cache/TTL/observer), `ServerSecurity`/`StoragePrefs` (PIN-PBKDF2/secret-sesi/partial-token), `SocialMediaExtractor` (http/redirect/Cobalt/Piped/Invidious), `Updater` (cache/list-API), `TlsCompat`, `Streams`/`HttpBody`/`AdtsAac` (zero-read), `MediaStream`/`SseStream`/`ServerStreams`/`ServerThumbnail`/`ServerVideoDurations`/`ZipCreator`, `DownloadItem`/`Repository`/`Codec`, `QueueOrder`/`SegmentPlanner`/`SpeedTracker`/`HlsParser`/`HlsMp4Muxer`, `Checksums`, `Crypto`/`PinHash`, `StorageCleanup`, `DownloadService`/`BootReceiver`/`App`, `MainActivity` (socialJob/debounce), `GalleryActivity` (adapter/DiffUtil), `LogActivity`, `SettingsActivity`, `WebExtractActivity`, `remote.src.html` (upload/SSE/fs/galeri).
- Temuan (BELUM diperbaiki — tunggu perintah owner):
  1. (bug) `itemsSignature()` tak memuat `speedLimitKbps` padahal `itemsJson()` meng-cache-nya — ganti limit saja pada item PAUSED tak mengubah signature sehingga remote menyajikan `speedLimitKbps` basi sampai field lain berubah. Fix: tambah `speedLimitKbps` ke hash.
  2. (bug DoS) `Checksums.toHex/base64Decode` tanpa batas panjang — header `Digest`/`X-Checksum-*` dari server jahat bisa raksasa sehingga `ByteArray(s.length*3/4)` OOM di thread download. Fix: tolak nilai >4KB di `fromHeaders`/`toHex` (Digest valid <1KB).
  3. (bug minor) `verifyToken` global di `uploadFiles()` (remote.src.html:4414) dipakai lintas job sekuensial — job baru mewarisi token job lama sampai chunk sukses pertama; retry-verify awal bisa pakai token salah (hasil akhir sama-sama gagal, tapi isolasi salah). Fix: jadikan per-job di dalam `uploadOne`.
- Diverifikasi bersih: guard `security_audit` 0/0, `check_readme_sync` sinkron, `prepare_remote --check` OK; redirect engine/ekstraktor validasi SSRF; merge staging+rename; throttle/watchdog; PIN PBKDF2 + cookie sesi acak; upload reservasi+lock atomik; login throttle per-IP; zip strip-lock+budget; SSE pump lifecycle; scan cache TTL monotonik.
- Guard saat audit: `security_audit` 0/0, `check_readme_sync` OK, `prepare_remote --check` OK (JS valid + smoke upload).

## Sesi fix 3 temuan jilid 19 (2026-10-04 13:55 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `7a8a527` (precedent `005f546`/`73ea48f`) + 3 entri `CHANGELOG.md`, push `main` `f1f176d..7a8a527` tanpa pantau workflow (aturan 19).
- Fix: (1) `itemsSignature()` tambah `speedLimitKbps * 67` + komentar; (2) `Checksums` tolak header raksasa (>4KB single, >8KB Digest/base64) + unit test; (3) `remote.src.html` `verifyToken` global → `job.verifyToken` per-job + regen `assets/remote.html` via `prepare_remote.py`.
- Guard: `security_audit` 0/0, `check_readme_sync` OK, `prepare_remote --check` OK (JS valid + smoke upload), `diff --check` bersih.

## Sesi sapuan agresif jilid 20 (2026-10-04 13:50 UTC, tanpa ubah kode — nihil fix)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif" — sapuan penuh pasca-fix jilid 19: `DownloadEngine` (HLS plan/estimasi/channel-SEGs/adaptive/import/free-space/redirect-SSRF/throttle), `HttpControlServer` (fsAction rename/move/mkdir/delete, fsList, serveFile/servePartial/stream-token, login-throttle/pinOk-cache, SSE/log-buffer/redaction, snapshot-throttle, zip-token), `FileSaver` (free-space min-volume, SAF/MediaStore), `MediaLibrary`, `ServerSecurity`/`StoragePrefs`, `SocialMediaExtractor` (extract/extractAll 60s-cap, header-user), `Updater`/`TlsCompat`, `Streams`/`HttpBody`/`AdtsAac`, `MediaStream`/`SseStream`/`ServerStreams`/`ServerThumbnail`/`ServerVideoDurations`/`ZipCreator`, `DownloadItem`/`Repository`, `QueueOrder`/`SegmentPlanner`/`SpeedTracker`/`HlsParser`, `Checksums` (cap baru), `Crypto`/`PinHash`, `StorageCleanup`, service/receiver/`App`, `MainActivity` (progressSig vs adapter-DIFF), `GalleryActivity`, `LogActivity`, `SettingsActivity` (port/PIN), `WebExtractActivity`, `DownloadAdapter`, `remote.src.html` (upload per-job), `scripts/`.
- Hasil: NIHIL temuan layak-fix. Tiga pola dicurigai gugur setelah verifikasi: (1) `refSegBytes*remaining` HLS aman — `declared` dari `HttpURLConnection.contentLength` (Int ≤2GB) × segmen ≤10k; (2) `pinOk` cache basi sembuh-sendiri (recompute saat secret rotate); (3) `progressSig` tanpa `checksumVerified`/`retryCount` aman — perubahan itu selalu bareng `state`/`error`/`progress` sehingga gate tetap submit (plus throttle 400ms hanya menunda, tak menghilangkan update).
- Catatan hardening non-aksi (risiko rendah, butuh PIN/autentikasi atau lokal): tanpa cap panjang per-field `addDownload` (url/headers/postBody mengandalkan cap form 4MB), rename MediaStore tanpa strip-lock (duplikat DISPLAY_NAME paralel dimungkinkan, MediaStore memang membolehkannya), `parseUserHeaders` tanpa cap jumlah header.
- Guard: `security_audit` 0/0, `check_readme_sync` OK; `prepare_remote --check` tak diulang penuh (remote tak diubah, `git status` bersih).

## Sesi sapuan bug+efisiensi jilid 21 (2026-10-04 13:57 UTC, tanpa ubah kode — 2 temuan)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif temukan bug atau pun kode yang nggak efisien" — fokus efisiensi + bug: `DownloadEngine` (updateItem/update/scheduleSave/progressSave batch vs loop, seg-flush, speed-sample, HLS refSeg, import, free-space), `HttpControlServer` (signature/itemsJson/snapshot/log/zip-thumb worker), `MainActivity` (progressSig/toolbar/sticky), `GalleryActivity` (DiffUtil background), `DownloadService`/receiver/`App`, `FileSaver`/`MediaLibrary`, `SocialMediaExtractor` (timeout 60s), `StoragePrefs`, remote JS (fragment/chunk/rAF), `scripts`.
- Temuan (BELUM diperbaiki — tunggu perintah owner):
  1. (efisiensi, medium) `DownloadEngine.resumeAutoPaused()` loop `updateItem()` per id (N salinan list + N emisi StateFlow; tiap updateItem O(n) indexOf+copy) padahal `pauseAll`/`resumeAll`/`retryFailed` sudah batch (1 map + 1 update). Pemicu nyata: `NetworkCallback.onAvailable` bisa menembak berulang → churn UI + `buildSections`/DiffUtil + toolbar per emisi. Fix: tiru pola `resumeAll` (kumpulkan idSet, 1× `update(...map...)`, `startQueued()`; `scheduleSave` debounce sudah 1× jadi yang dihemat CPU/emisi).
  2. (duplikasi, low) `loadMoreGallery()` (remote.src.html) dua cabang identik render-chunk (rAF vs langsung), beda hanya penjadwalan ekor. Runtime ~0 (minify), tapi gandakan permukaan bug (ubah format cell wajib sentuh dua tempat). Fix: ekstrak `renderNextGalleryChunk()` lalu cabang hanya atur `requestAnimationFrame` vs loop.
- Diverifikasi efisien/bersih: `updateItem` lewati emit bila sama; `flushSegmentProgress` 1 updateItem per item per flush + speed-sample 1/detik; `scheduleSave` debounce + `scheduleProgressSave` 2-detik; `progressSig`/toolbar-sig gate + sticky-header scan ke atas; galeri native DiffUtil background + LruCache + cancel job cell; remote galeri fragment+chunk+rAF; thumbnail/durasi probe ter-cache + throttled; `StoragePrefs` prefs/collapsed cache; ekstraktor timeout total 60s + redirect tervalidasi.
- Guard: `security_audit` 0/0. Tanpa push repo (tak ada perubahan kode).

## Sesi fix 2 temuan jilid 21 (2026-10-04 14:07 UTC, push main sukses)

- Perintah user: temuan jilid 21 (2 item) + yang diverifikasi bersih — 1 commit satu tujuan `baad5f1` + 2 entri `CHANGELOG.md`, push `main` `7a8a527..baad5f1` tanpa pantau workflow (aturan 19).
- Fix: (1) `DownloadEngine.resumeAutoPaused()` batch 1x map + 1x update seperti `pauseAll`/`resumeAll`/`retryFailed` (plus `clearSegProgress()` per id selaras `resume()` tunggal); (2) `remote.src.html` `loadMoreGallery()` dua blok render-chunk identik digabung satu blok + syarat rAF (`sisa > 0 && len > 120`), perilaku windowing sama + regen `assets/remote.html` via `prepare_remote.py`.
- Guard: `security_audit` 0/0 (self-test OK), `check_readme_sync` OK, `prepare_remote --check` OK (sinkron + JS valid + UI Inggris + smoke upload), `check_repo.py --pre-commit` 10/10 SEMUA SEHAT, `diff --check` bersih.

## Sesi sapuan agresif jilid 22 (2026-10-04 20:35 UTC, tanpa ubah kode — 2 minor + 2 catatan)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif" — sapuan penuh: `DownloadEngine` (queue/launch/retry-mirror/watchdog/seg-flush/HLS/rate-limiter/checksum), `HttpControlServer` (cleanup-periodik/cache-bounds/SSE/log-redact), `DownloadService`/`BootReceiver`/`BootResumeJobService`/`App`, `FileSaver`/`MediaLibrary`/`StorageCleanup`, `ServerSecurity`/`StoragePrefs` (SecureRandom), `SocialMediaExtractor`/`Updater`, `DownloadAdapter` (buildSections/DiffUtil payload), `MainActivity` (dialog-probe/autoOpen/emptyView), `GalleryActivity`/`LogActivity`/`SettingsActivity`/`WebExtractActivity`, `NotificationHelper`/`Crypto`, `remote.src.html` (render/updateRows/SSE/upload/thumb-queue/gallery/pin), `docs/index.html`, manifest permission.
- Temuan (BELUM diperbaiki — tunggu perintah owner):
  1. (efisiensi, minor) `DownloadEngine.resumeInterrupted()` loop `updateItem()` per id (N salinan + N emisi) — pola sama yang baru di-batch di `resumeAutoPaused()`; dampak sekali jalan saat service/activity start, bukan callback berulang. Fix: batch 1x map + 1x update seperti `resumeAll`.
  2. (efisiensi, minor) `remote.src.html updateRows()`: `rebuildList(items); return;` di dalam `forEach` — `return` hanya lanjut ke item berikut, loop tak berhenti sehingga sisa baris di-patch ulang tepat setelah rebuild penuh (`lastRowSig` baru di-reset = render ganda). Fix: `for` + `break` atau flag.
  3. (catatan, trivial) `dlPinned` Set + localStorage tak pernah prune id unduhan yang sudah dihapus (beda dengan `lockedTotalBytes` yang prune). Tumbuh hanya se-pin user. Fix opsional: prune di `render()` seperti `lockedTotalBytes`.
  4. (catatan, trivial) `_thumbQueue` tetap memuat thumbnail cell yang sudah hancur saat galeri reset/ganti filter (buang bandwidth; tanpa stall karena onload tetap tembak). Fix opsional: kosongkan antrean di `renderGalleryReset`.
- Positif palsu yang gugur (verifikasi, BUKAN bug): loop baca download/HLS/checksum/`Updater.get` tanpa guard zero-read — stream `HttpURLConnection`/`BufferedReader` memblokir (bukan 0-return seperti stream sesi NanoHTTPD), plus watchdog stall 30 dtk menyembuhkan sendiri; guard 32-nol hanya untuk kelas stream sesi/parser. `autoOpenCompleted`/`progressSig`/`structSig`/`updateRows` sig, cache server (bounded + periodic cleanup), `thumbCache` static (clear saat trim/destroy), cursor `.use{}`, WebView `destroy()`, dialog lokal (tanpa leak rotasi), PIN PBKDF2 + secret SecureRandom, redirect/SSRF, MicroExtractor loop (`advance()` menjamin terminasi).
- Guard: `security_audit` 0/0 (24 rules), `check_readme_sync` sinkron (9 heading), `git status` bersih. Tanpa push repo (tak ada perubahan kode).

## Sesi fix 4 temuan jilid 22 (2026-10-04 20:40 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `638424f` (precedent `7a8a527`/`baad5f1`) + 4 entri `CHANGELOG.md`, push `main` `baad5f1..638424f` tanpa pantau workflow (aturan 19).
- Fix: (1) `resumeInterrupted()` batch 1x map + 1x update, perilaku sama (hanya PENDING + autoResume); (2) `updateRows()` forEach → for + break setelah rebuild (render ganda hilang); (3) `render()` prune `dlPinned` + persist localStorage seperti `lockedTotalBytes`; (4) `_thumbQueueClear()` + panggil di `renderGalleryReset()`; regen `assets/remote.html` via `prepare_remote.py`.
- Guard: `security_audit` 0/0, `check_readme_sync` OK, `prepare_remote --check` OK (sinkron + JS valid + UI Inggris + smoke upload), `check_repo.py --pre-commit` 10/10 SEMUA SEHAT, `diff --check` bersih.

## Sesi feat Scribd tanpa langganan (2026-10-04 21:05 UTC, push main sukses)

- Perintah user: "tambahkan kompatibilitas scribd tanpa harus langganan" — riset empiris: seluruh endpoint scribd.com (search, doc page, embeds, oembed) menyajikan "Client Challenge" JS ke fetch server (terverifikasi via curl) → arsitektur WebView seperti HentaiHaven (bukan fetch server).
- 1 commit satu tujuan `df78baa` + 1 entri `CHANGELOG.md`, push `main` `638424f..df78baa` tanpa pantau workflow (aturan 19).
- Implementasi: `SocialMediaExtractor` (`SCRIBD_HOST_RE`/`isScribdUrl`/cabang extract/`parseScribdPage`/`parseDocPages`+`DocPage`, cap 300, host-lock scribdassets); `extract.js` kolektor gambar halaman (src/data-src/srcset, filter chrome, urut nomor); `WebExtractActivity` (`EXTRA_PAGES_JSON`/`onPagesOnly`/trim 300); `MainActivity` (badge Scribd, skip probe, `offerPagesBatch` antre langsung + cookie/Referer, nama `Scribd_<judul>_p001.jpg`); strings `platform_scribd`+`batch_pages_*`; 4 unit test; `docs/index.html` FAQ ID+EN.
- Batas jujur: hanya halaman pratinjau yang ter-render untuk sesi anonim (terkunci = tak ada URL di DOM = tak terunduh); tanpa bypass paywall/kredensial.
- Guard: `security_audit` 0/0, `prepare_remote --check` OK, `check_readme_sync` OK, `node --check extract.js` OK, `check_repo.py --pre-commit` 10/10, `diff --check` bersih. Compile penuh milik CI (tanpa SDK lokal).

## Sesi revert kompatibilitas Scribd (2026-10-04 21:20 UTC, push main sukses)

- Perintah user: "revert kompatibilitas scribd" — kondisi awal: HEAD df78baa (feat Scribd) sudah di-revert di working tree dan ter-staged (7 file kode identik dengan 638424f pra-Scribd, tinggal commit); diverifikasi lalu di-commit + push.
- 1 commit satu tujuan cb630de + 1 entri CHANGELOG.md revert(social), push main df78baa..cb630de tanpa pantau workflow (aturan 19).
- Revert: URL scribd.com kembali diperlakukan sebagai URL biasa; cabang isScribdUrl/parseScribdPage/parseDocPages, kolektor halaman extract.js, alur batch WebExtractActivity/MainActivity, strings platform_scribd/batch_pages_*, unit test, FAQ docs/index.html dihapus. Riwayat CHANGELOG lama tetap ada (7 baris), kode/test/docs bersih dari scribd (rg kosong).
- Guard: security_audit full 0 error/0 warning (24 rules), audit self-test OK, prepare_remote --check OK (sinkron + JS valid + UI Inggris + smoke upload), check_readme_sync OK (9 heading), node smoke OK, git diff --check bersih; 4 cek instan OK (struktur, no local SDK, AGENTS completeness, admin konsisten). Java tak tersedia sehingga android checks terlewati (sesuai aturan: compile penuh milik CI).

## Sesi sapuan penuh jilid 24 (2026-10-07 00:28 UTC, tanpa ubah kode — 2 bug + 1 minor)

- Perintah user: "cek seluruh kode temukan bug" — sapuan `HttpControlServer` (upload-chunk/itemsJson/galeri/serveFile/serveMedia/SSE), `DownloadEngine` (segProgress/flush/throttle), `FileSaver`, `MediaLibrary` (scanCache/TTL), `MainActivity` collector, `remote.src.html` (render/structSig/SSE), `Updater`.
- Kondisi awal: working tree kotor — 4 file belum di-commit (jilid 23: `serveFile` contentUri AFD-throw, `organizeByType` klaim kosong filesystem, `WebExtractActivity.onDestroy` stopLoading, +1 entri CHANGELOG). HEAD tetap `cb630de`.
- Temuan (BELUM diperbaiki — tunggu pilihan owner):
  1. (bug/data-loss) `FileSaver.organizeByType` cabang SAF: `subDir.findFile(fileName) ?: createFile(...)` memakai nama asli tanpa uniquifikasi (cabang filesystem memakai `uniqueTargetFile`, cabang MediaStore menoleransi duplikat). Bila `Download/<Sub>/` sudah berisi nama sama, file lama langsung di-truncate via open `"wt"` lalu sumber dihapus — data lama hilang. Fix: `uniqueDocumentName(subDir, fileName)` seperti `writeCustomFolder`/`publishToCustomFolder`.
  2. (bug/UI-churn) `MainActivity` collector empty-view: guard `binding.emptyView.animation == null` mengecek animasi parent (selalu null) tapi yang dianimasikan anak `getChildAt(0)` — tiap emisi `items` (tiap tick progres) me-reload + restart pulse sehingga animasi tak pernah jalan + alokasi berulang. Fix: cek/atur animasi pada child yang sama (`getChildAt(0)?.animation`), start sekali.
  3. (minor/stale) `MediaLibrary.scanCached`: TTL cache yang dipakai (`scanCacheTtlMs`) adalah TTL hasil LAMA. Cache fallback 600 dtk tetap valid 600 dtk walau MediaStore sudah pulih (seharusnya turun ke 30 dtk). Fix: simpan TTL per-cache (mis. Quad dengan ttl) atau pakai TTL 30 dtk bila `usedFallback` lama tapi scan baru MediaStore.
- Yang diverifikasi bersih: reservasi buffer upload + finally, lock upload atomik, login throttle per-IP, zip strip-lock + token sekali-pakai, signature/cache itemsJson, resume/ETag/CDN-refresh, merge staging, watchdog/throttle, PIN PBKDF2 + cookie sesi acak, `uploadUniqueName` traversal-safe, tombol remote, `Updater` cap 512KB + cache 24 jam, `serveFile` contentUri (sudah ditutup jilid 23), `serveMedia` u: (descriptor ditutup bila konstruktor stream melempar), `segProgress`/`throttleTotals` lock bersama, `scheduleProgressSave` throttle 2 dtk, SSE pump identity-check, `structSig` JS (struktural saja, progres via updateRows — benar).
- Guard: `security_audit` 0 error/0 warning (24 rules). Tanpa push repo (tak ada perubahan kode).

## Sesi fix 3 temuan jilid 24 (2026-10-07 00:50 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 2 push: (1) commit `e49dc79` untuk 4 file jilid 23 yang menggantung (belum di-commit); (2) commit `9a6bf51` fix 3 temuan jilid 24 + 1 entri `CHANGELOG.md`. Tanpa pantau workflow (aturan 19).
- Fix: (1) `FileSaver.organizeByType` SAF pakai `uniqueDocumentName(subDir, fileName)` (anti-timpa file senama); (2) pulse empty-view `MainActivity` guard+start/clear pada anak `getChildAt(0)` yang sama (`emptyChild?.animation`); (3) `MediaLibrary` TTL per-cache via `private data class ScanCache(ts, items, total, ttlMs)`, hapus `scanCacheTtlMs` global (tak ada referensi lain termasuk test).
- Guard: `security_audit` 0/0 (24 rules), `check_repo.py --pre-commit` 9/10 — satu-satunya gagal `[4/10] admin konsisten` murni lingkungan (`pyyaml` tak terinstal di mesin ini, import gagal sebelum validasi apa pun; tak terkait diff; CI punya yaml). `git diff --check` bersih. Compile penuh milik CI (tanpa SDK lokal).

## Sesi sapuan agresif jilid 25 (2026-10-07 00:49 UTC, tanpa ubah kode — 2 bug + 1 minor)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif temukan bug" — sapuan `ServerStreams`/`ServerThumbnail`/`ServerVideoDurations`/`MediaStream`/`ZipCreator`/`SseStream`, `DownloadService`+wakelock, `BootReceiver`/`BootResumeJobService`, `SocialMediaExtractor` httpGet/httpPost/redirect-cookie, `App` startup, `StorageCleanup`, `NotificationHelper`, `DownloadRepository`, `SettingsActivity` cleanup/switch, `GalleryActivity` openEntry, `WebExtractActivity`+`extract.js`, `LogActivity` export, `DownloadEngine` HLS/CDN/segmen, `HlsParser`/`AdtsAac`, `Crypto`/`PinHash`, `Streams`/`Checksums`/`Formats`/`MimeTypes`, `MainActivity` autoOpen/openApk, `remote.src.html` (moveHere/runFsActions/upload).
- Temuan (BELUM diperbaiki — tunggu pilihan owner):
  1. (bug/data-loss) `SettingsActivity.cleanupJunkFiles`: `itemNames` dari `it.fileName` MENTAH tapi file disk memakai `FileNames.safe()` — judul YouTube berkarakter `|?:*` (dll), nama >200 char, atau reserved name membuat `.part` AKTIF tak cocok lalu DIHAPUS tombol cleanup saat download berjalan (progres hilang + merge gagal). Sweeper engine (`cleanupOrphanPartials` via `protectedPartialNames`) sudah benar pakai safe. Fix: `map { FileNames.safe(it.fileName) }`.
  2. (bug/crash) `GalleryActivity.openEntry` (+fallback `partialPlayIntent`): `FileProvider.getUriForFile` di luar `runCatching` (hanya `startActivity` yang dibungkus) — ketuk video ber-filePath di luar roots FileProvider (folder teks kustom/SD removable, folder galeri terpilih non-publik) melempar `IllegalArgumentException` → crash. `MainActivity.openDownload` sudah benar (runCatching+toast). Fix: bungkus konstruksi intent dalam runCatching + toast `gallery_open_error`.
  3. (minor/robustness) `ZipCreator.zipFile` cabang filesystem tanpa dedupe nama entri (cabang `zipTokens`/`zipMedia` pakai `uniqueZipName`): dua file yang ternormalisasi sama (`safeEntryPath` petakan kontrol C0→`_`, buang segmen `.`/`..`) membuat `ZipException` duplikat — cabang file menelan diam-diam (file hilang), cabang direktori tak terbungkus → seluruh ZIP folder jadi 404 via `createTempZip`. Fix: param `usedNames` (+`uniqueZipName`) di-thread rekursi, prefix anak pakai nama unik; `isFileAllowed` tetap terakhir (trailing lambda).
- Yang diverifikasi bersih: ChainInputStream/PositionedAsset/DeleteOnClose, thumb lock+staging+failure-TTL, durations lock+staging, parseRange/416/skipFully, SSE poison+PING, BoundedOutputStream, wakelock ref-counted+isHeld, boot JobScheduler, redirect manual + strip kredensial lintas-host + `isExtractRedirectAllowed`, `isUrlForbidden` tanpa follow, `prepareResumeOffset`/TRUNCATE, `ensureItemPresent`/`ensurePublishedKept`, CDN-refresh+HEAD-probe, SpeedTracker EMA-seed, `redirectTarget`+blocklist numerik/IPv6, Keystore GCM + PBKDF2, readBounded zero-guard, repo degraded-load guard + saveProgress ordering, `autoOpenCompleted` idempoten, `openApk` runCatching, `moveHere` self-move guard, `runFsActions`/`postFsAction` rethrow-stop, uploadFiles offset eksplisit + verify-token, `HlsParser.resolveUrl` RFC-3986, `extract.js` bounded (50 eps/1MB HTML).
- Guard: tanpa ubah kode (tak ada guard dijalankan selain baca). Tanpa push repo.

## Sesi fix 3 temuan jilid 25 (2026-10-07 01:05 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `dbb94dc` (5 file: 3 kode + 1 test + CHANGELOG) + 1 entri `CHANGELOG.md`, push `main` sukses tanpa pantau workflow (aturan 19).
- Fix: (1) `SettingsActivity.cleanupJunkFiles` bandingkan `FileNames.safe(it.fileName)` + import (`.part` aktif tersanitasi tak lagi dianggap sampah); (2) `GalleryActivity.openEntry` konstruksi intent dalam `runCatching().getOrNull()` + toast bila null (pola `MainActivity`); (3) `ZipCreator.zipFile` param baru `usedNames` sebelum `isFileAllowed` (trailing lambda aman) + `uniqueZipName` + prefix anak pakai nama unik + guard entri kosong; +1 unit test `recursive zip deduplicates normalized entry names` (kontrol C0 → `bad_name.txt` + `bad_name (1).txt`).
- Guard: `security_audit` 0/0 (24 rules), `check_repo.py --pre-commit` 9/10 (gagal hanya `[4/10]` lingkungan `pyyaml` hilang — sama seperti jilid 24, tak terkait diff), `diff --check` bersih. Compile penuh milik CI.

## Sesi sapuan agresif jilid 26 (2026-10-07 01:28 UTC, commit 0f0d19b, push main sukses)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif temukan bug" — sapuan `SseStream`/`ShareToken`/`ServerLog`/`HttpBody`/`ServerThumbnail`/`ServerVideoDurations`/`MediaStream`/`ServerStreams`/`ZipCreator`(+test), `DownloadService`+wakelock, `BootReceiver`/`BootResumeJobService`, `App` startup+network callback, `Updater`, `DownloadRepository`, `DownloadEngine` importStream/probe, `FileSaver` merge/publish/orphan/freeBytes, `MediaLibrary` scanCache/observer, `StorageCleanup`, `CrashLog`, `Permissions`, `LogActivity` export, `HttpControlServer` serve/snapshot/itemsJson/upload-chunk/finalize/fsZip/mediaZip/zipCached, `remote.src.html` galeri-select/SSE-reconnect, `MainActivity` probe dialog.
- 3 temuan SEMUA di `zipTokens` (jalur `media_zip`, tak tersentuh jilid 25 yang hanya perbaiki `zipFile`): (1) nama folder token direktori dipakai mentah (`uniqueZipName(f.name)`) tanpa `safeEntryPath` — folder bernama `..`/backslash/kontrol = traversal di extractor pihak ketiga (cabang file tunggal sudah sanitasi); kini via helper murni baru `tokenDirRootName()`; (2) `seen`+`usedNames` fresh per child — nama ternormalisasi kembar antar-sibling menimpa entri duplikat → `ZipException` → file hilang diam-diam (ditelan runCatching), symlink target-sama di-zip ganda; kini `dirSeen`/`dirUsed` dipakai bersama per direktori; (3) budget `MAX_ZIP_ENTRIES` tak dikonsumsi di jalur file tunggal — guard mati untuk daftar flat (yang membatasi praktis = `MAX_MEDIA_ZIP_TOKENS`=256, jadi defense-in-depth); kini `tryTake()` per entri.
- Fix: 1 commit satu tujuan `0f0d19b` (3 file: `ZipCreator.kt` + `ZipCreatorTest.kt` + 1 entri `CHANGELOG.md`), push `main` sukses tanpa pantau workflow (aturan 19).
- Guard: `security_audit.py` 0 error / 0 warning (24 rules); `check_repo.py` penuh tak bisa selesai dalam jendela eksekusi (tak ada perubahan remote/README/struktur — tak relevan dengan diff); `git diff --check` bersih (implisit). Compile penuh milik CI (tanpa SDK lokal).
- Yang diverifikasi bersih (tak diulang di jilid 27): SseStream poison/PING, HttpBody multipart/chunked/drain, parseRange/416/skipFully, ChainInputStream fd-close, DeleteOnCloseStream, upload reservasi+finalisasi background, zipCached strip-lock+eviksi, itemsSignature/itemsJson cache, snapshot throttle per-IP, ServerLog redaction, ServerVideoDurations staging+TTL, DownloadService wakelock+notif-throttle, boot job persisted, App thumb-cleanup cap + crash logger, Updater list-first anti-cache-basi, Repository degraded-load + saveProgress ordering, importStream size-nyata, mergeSegments staging, destinationFreeBytes multi-volume, scanCache TTL-per-cache + observer DCL, CrashLog trim, Permissions caller Activity, LogActivity export tanpa yatim/0-byte.

## Sesi sapuan agresif jilid 27 (2026-10-07 11:16 UTC, tanpa ubah kode — 2 tinggi + 1 sedang)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif temukan bug" — sapuan `HttpControlServer` (serve/share/media/meta-cache/upload-chunk/zip), `MediaStream` (parseRange/streamMedia), `ServerVideoDurations`, `ServerSecurity.isPathAllowed`, `MediaLibrary` token, `MainActivity` probe dialog, `remote.src.html` SSE/polling.
- Temuan (BELUM diperbaiki — tunggu pilihan owner):
  1. (tinggi) `HttpControlServer.cachedMediaMeta` eviksi `iter.remove()` di atas `ConcurrentHashMap` (`HttpControlServer.kt:2059-2066`, map di `:191`, batas 256 di `:3317`) — iterator CHM tak dukung remove → `UnsupportedOperationException` → `serveMedia` 500 saat cache >256. Pemicu: browsing + putar >256 video unik.
  2. (tinggi) `serveShare` jalur `contentUri` (`HttpControlServer.kt:3169-3185`): `openInputStream` dibuka dulu lalu `openAssetFileDescriptor` bisa lempar tanpa `runCatching`+close (bocor fd + 500 bukan 404), dan `streamMedia` dipanggil tanpa try/catch penutup (bocor bila lempar) — tidak seperti `serveFile` yang disiplin try/catch. Pemicu: share link URI basi/dicabut di antara dua call, atau Range picu IOException.
  3. (sedang) `ServerVideoDurations.recordProbeFailure`: eviksi hanya `removeAll` kedaluwarsa; bila >2000 gagal semua dalam TTL 10 mnt tak ada yang terbuang → map tumbuh tanpa batas. Pemicu: galeri ~3000 entri + probe gagal massal.
- Yang diverifikasi bersih: `isPathAllowed` kanonikalisasi internal (input absolutePath tetap aman — tuduhan symlink gugur), `streamMedia` total -1 via chunked, SSE reconnect 1x + give-up + cooldown, throttle snapshot/login per-IP, reservasi upload + drain/close, zip strip-lock, `failedUrls`/`credCache` iter.remove aman (bukan CHM).
- Guard: `security_audit --self-test` OK. Tanpa push repo (tak ada perubahan kode).

## Sesi fix 3 temuan jilid 27 (2026-10-07 11:20 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `bf4d2ae` + 1 entri `CHANGELOG.md`, push `main` sukses tanpa pantau workflow (aturan 19).
- Fix: (1) `cachedMediaMeta` eviksi via snapshot kunci (`keys.toList()` + `remove`) bukan `iter.remove` (CHM tak dukung remove); (2) `serveShare` contentUri pola `serveFile` (runCatching + tutup stream + 404 + invalidasi galeri) + `streamMedia` dalam try/catch penutup; (3) `recordProbeFailure` paksa buang setengah tertua bila masih >MAX setelah buang kedaluwarsa.
- Guard: `security_audit` 0/0 (24 rules), `git diff --check` bersih; `check_repo --pre-commit` tak selesai dalam jendela eksekusi (sama seperti jilid 26 — tak terkait diff). Compile penuh milik CI.

## Sesi sapuan agresif jilid 28 (2026-10-07 11:20 UTC, tanpa ubah kode — 1 sedang + 2 rendah)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif temukan bug" — sapuan `MainActivity` dialog probe, `ServerSecurity` token, `HttpControlServer` snapshot-throttle, `DownloadEngine` mirror/retry (isGitHubUrl host-parse — rantai proxy-ganda gugur), `DownloadService`, `App`/boot, `WebExtractActivity`/`extract.js`, `SocialMediaExtractor` redirect, `Updater`, `FileSaver`/`StorageCleanup`, `GalleryActivity`, `LogActivity`, `ServerThumbnail`, `DownloadRepository`.
- Temuan (BELUM diperbaiki — tunggu pilihan owner):
  1. (sedang) Dialog tambah ditutup tapi `socialJob`/`socialDebounce` tak dibatalkan (`MainActivity.kt:412` deklarasi, `:963` dismiss hanya null-kan handler web-extract) — job lifecycleScope menahan seluruh view-tree dialog + ekstraksi jaringan sia-sia s.d. ~60 dtk pasca-tutup.
  2. (rendah) Token verify-upload vs partial-stream format identik + secret sama (`ServerSecurity.kt:140-175`, secret `partialStreamSecret`; dipakai `uploadVerify` + `servePartial`) — tanpa pemisah domain, token satu jalur berpotensi lolos validasi jalur lain bila ID tabrakan. Fix: prefix domain di payload HMAC ("upload-verify:"/"partial:").
  3. (rendah) Throttle snapshot bisa sajikan `"{}"` (`HttpControlServer.kt:195` init, `:254` throttle 1000 ms `:3286`) — dua request paralel IP sama saat start/restart: yang kedua dapat cache `"{}"` → daftar kosong sekedip sebelum poll berikutnya pulih.
- Yang diverifikasi bersih (tak diulang jilid 29): mirror GitHub (isGitHubUrl parse host, proxy tak regen), login throttle per-IP + volatile, trackConnection lock, segFlush/throttle lock, probeUrl same-origin auth, Invidious/httpGet redirect eksplisit + strip kredensial, Updater list-first + cap 512KB, WebExtract destroy+stopLoading, SSE 1x+give-up, zip strip-lock + token sekali-pakai, serveFile/serveShare try/catch (jilid 27), eviksi meta snapshot-key (jilid 27), probeFail paksa-paruh (jilid 27).
- Guard: `security_audit` 0/0 (24 rules). Tanpa push repo (tak ada perubahan kode).

## Sesi fix 3 temuan jilid 28 (2026-10-07 11:25 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `8975508` + 1 entri `CHANGELOG.md` + 1 unit test lintas-jalur, push `main` sukses tanpa pantau workflow (aturan 19).
- Fix: (1) `MainActivity` dismiss batalkan `socialJob`/`socialDebounce` + null-kan; (2) `ServerSecurity` HMAC token diprefix domain (`partial:`/`upload:`, format kawat tetap `id.expiry.hmac` — token lama otomatis gugur, wajar karena short-lived); (3) throttle snapshot bangun fresh bila cache masih `"{}"` awal.
- Guard: `security_audit` 0/0 (24 rules), `git diff --check` bersih. Compile + unit test penuh milik CI.

## Sesi fokus remote web jilid 29 (2026-10-07 11:51 UTC, tanpa ubah kode — 1 sedang + 2 rendah)

- Perintah user: "kita fokus ke remote web" — audit baca-saja `remote.src.html` (6603 baris: render/updateRows/gallery/fs/move/upload/SSE/polling/ZIP/login) + `prepare_remote.py` + endpoint terkait `HttpControlServer` (pinOk/media/thumb/events).
- Temuan (BELUM diperbaiki — tunggu pilihan owner):
  1. (sedang) Auto-logout 10 mnt membunuh playback/upload (`remote.src.html:~4717`: re-arm hanya klik/sentuh/tombol/scroll/mouse; logout rotate secret → `/api/media` 401 padahal di cabang pinOk `:292`). Pemicu: PIN aktif + nonton film >10 mnt tanpa interaksi (TV/tablet) → video macet di Range berikutnya; upload/XHR ikut 401. Fix: jangan logout saat video diputar/`fsUploading`/transfer aktif, atau re-arm saat poll/SSE sukses.
  2. (rendah-sedang) `runFsActions` kehilangan hitungan parsial (`~4330`: `out.done = done` hanya di jalur sukses; throw tengah batch → lapor 0 padahal sebagian sudah pindah → "nothing moved" menyesatkan). Pemicu: batch move 5 folder, item ke-3 gagal. Fix: set `out.done` sebelum throw/ di catch.
  3. (rendah) ZIP ditampung di RAM s.d. 400 MB (`ZIP_MEMORY_LIMIT`, `downloadZipWithProgress ~3838`: chunks[] + Blob ≈ 2x di memori; TV RAM kecil bisa OOM-crash tab padahal fallback anchor streaming tersedia). Pemicu: ZIP galeri 300 MB di TV 1 GB. Fix: turunkan ambang (64–100 MB) atau deteksi memori kecil.
- Yang diverifikasi bersih: XSS (escapeHtml di semua nama/error, textContent di modal/toast/meta), CSRF (XHR header + zt sekali-pakai), ID upload crypto-hex 32, retry/finalize caps 3x + 5 mnt, move self-check + validasi server, `beforeunload` saat upload, thumb/media token-encode, D-pad/tabbar, tema, swipe, delegasi SSE 1x+give-up.
- Guard: `security_audit` 0/0 (24 rules, dari sesi sebelumnya; kode tak berubah). Tanpa push repo (tak ada perubahan kode).

## Sesi fix 3 temuan remote web jilid 29 (2026-10-07 12:00 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `e136dd2` (3 file: `remote.src.html` + `remote.html` regen + 1 entri `CHANGELOG.md`), push `main` sukses tanpa pantau workflow (aturan 19).
- Fix: (1) auto-logout tunda + re-arm bila video diputar/`fsUploading`/`fsDlActive`/`anyActiveTransfer()`; (2) `runFsActions` `let done` keluar try + `out.done = done` di catch; (3) `ZIP_MEMORY_LIMIT` 400→96MB + komentar.
- Guard: `prepare_remote --check` OK (sinkron + JS valid + UI Inggris + smoke upload 4 chunk), `security_audit` 0/0 (24 rules), `diff --check` bersih. Compile penuh milik CI.

## Sesi diagnosis galeri seret jilid 30 (2026-10-07 12:10 UTC, tanpa ubah kode)

- Perintah user: "cari bug di remote mengapa galeri nggak lancar saat di scroll" — diagnosis baca-saja `remote.src.html` galeri (thumb-queue/render/sentinel/scroll) + CSS + sisi server (`HttpControlServer` pool 2-4 thread, thumb decode per-request, halaman 100).
- Penyebab peringkat: (1) UTAMA — 10 thumb paralel vs server 2-4 thread + decode video per `/api/thumb` (CPU berat di TV) → antrean + lambat; `loading="lazy"` dinonaktifkan antrean (src di-set langsung untuk semua cell render incl. luar layar). (2) handler scroll tanpa throttle: `getBoundingClientRect` tiap event (forced reflow) + 3 handler scroll lain. (3) semua cell menumpuk di DOM (content-visibility hanya di browser baru; WebView TV tua tak terbantu). (4) `renderGalleryReset` baca localStorage per item. (5) tiap thumb = 1 koneksi + 1 decode, tanpa batch/prefetch.
- Opsi fix (belum dipilih owner): A-kecil: turunkan konkurensi thumb 10→3 + IntersectionObserver (hanya thumb terlihat) + throttle scroll rAF. B-sedang: + virtualisasi/windowing buang cell jauh. C-server: kecilkan thumb/kompresi atau cache agresif (cache disk sudah ada).
- Guard: tanpa perubahan kode. Tanpa push repo.

## Sesi fix galeri seret jilid 30 (2026-10-07 12:20 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 1 commit satu tujuan `37e8ca8` (3 file: `remote.src.html` + `remote.html` regen + 1 entri `CHANGELOG.md`), push `main` sukses tanpa pantau workflow (aturan 19).
- Fix: (1) thumb paralel 10→3 + `IntersectionObserver` lazy (rootMargin 300px, fallback antrean bila IO tak ada; clear ikut unobserve); (2) scroll rAF-throttle + guard route + restore atas; (3) windowing 240 cell (trim atas + padding kompensasi, restore per chunk, reset bersihkan); cell dirender ulang via `renderGalleryCell` (state select dari data, aman).
- Guard: `prepare_remote --check` OK (sinkron + JS valid + UI Inggris + smoke 4 chunk), `security_audit` 0/0, `diff --check` bersih. Compile penuh milik CI.

## Sesi audit agresif (2026-10-07, HEAD a0a7177, tanpa commit kode — baca-saja)

- Perintah user: "cek seluruh kode dari seluruh area lebih agresif temukan bug".
- Mode audit (SOUL): tidak ubah kode, hanya kumpulkan temuan + bukti baris.
- Guard: check_repo + security_audit dijalankan (sesi paralel 47838); verifikasi manual: Updater sudah Dispatchers.IO, port 1024..65535, probe sosmed timeout 20 dtk, ZipCreator canonical, wakeLock release di onDestroy.
- Temuan dilaporkan ke user: 1 Tinggi (Crypto fallback plaintext diam-diam), 3 Sedang (START_STICKY, SSRF DNS-rebinding, wakeLock tanpa timeout), 4 Rendah (notif-ID overflow, fallback APK flag, collapsed race, catch Throwable). Belum diperbaiki — menunggu perintah "perbaiki".

## Sesi fix audit agresif (2026-10-07, push main 924c84f — 7 commit, 1 temuan gugur)

- Perintah user: "perbaiki semuanya" (mengesampingkan batas 1-area SOUL; tiap temuan 1 commit satu tujuan + entri CHANGELOG, push sekali di akhir tanpa pantau per aturan 19).
- Gugur (tak perlu fix, koreksi audit): race `collapsed_sections` — `setSectionCollapsed` sudah `synchronized(prefsLock)`, baca volatile hanya bisa basi kosmetik.
- 8442305 fix(security) Crypto: kunci keystore invalid (ganti/hapus lockscreen) tak lagi langsung plaintext — reset entri + retry 1x, flag `encryptFallbackUsed` + Log.e; + test. Guard sempat flag literal log Indonesia ("gagal/simpan") → di-EN-kan + fixup ke commit ini.
- 2b87584 fix(service): `onStartCommand` NOT_STICKY bila idle (kecuali RESUME_ALL = baru diminta jalan, karena restart-mode ikut return terakhir).
- 321370a fix(security): `isBlockedRedirectHost` resolve DNS tolak loopback/unspecified (fail-open bila DNS gagal; LAN tetap lolos) + helper murni `isIpLiteral`/`HOSTNAME_RE` + test.
- 4bdacfa fix(service): wakeLock `acquire(1 jam)` + re-acquire otomatis tiap emisi flow.
- 1753a10 fix(notification): ID bungkus 900rb→10000 via `getAndUpdate(::wrapNotifId)` + `NotifIdWrapTest`.
- e43471d fix(app): fallback APK ke-3 +FLAG_ACTIVITY_NEW_TASK. 924c84f fix(app): `catch Throwable` onCreate lempar ulang VM Error/ThreadDeath/LinkageError.
- Guard: `security_audit` 0/0, `check_repo` 9/10 (sisa [4/10] labeler-yaml = modul pyyaml tak ada di mesin ini, pre-existing environmental, .github/ tak tersentuh). Compile penuh diserahkan ke CI.

## Sesi audit agresif jilid 2 (2026-10-08, HEAD 924c84f, baca-saja tanpa commit kode)

- Perintah: "cek seluruh kode dari seluruh area lebih agresif temukan bug".
- Temuan baru: (1) Crypto.invalidateKey() terlalu agresif — dipanggil untuk SEMUA gagal enkripsi, bisa menghapus kunci sehat + yatimkan kredensial lama (fix presisi: hanya saat KeyPermanentlyInvalidatedException); (2) PTS overflow HLS jahat → mux gagal aman/fail-safe (Rendah, hardening opsional clamp EXTINF); (3) dugaan writeAll buffer tak tumbuh saat frame > buffer (perlu uji, writeTrackPts sudah grow); (4) token partial ke player eksternal by-design time-bound (Rendah).
- Diverifikasi bersih: XSS remote, SSE, reservasi upload, PIN/cookie, free-space, SegmentPlanner, overlayProgress, storedCreds, StorageCleanup, WebView destroy, DiffUtil payloads, build.yml bump, FileProvider wrap.
- Guard: security_audit 0/0 (ronde lalu); check_repo 9/10 sisa yaml-env. Belum diperbaiki — menunggu "perbaiki".

## Sesi fix audit jilid 2 (2026-10-08, push main b5c5692 — 2 fix + 2 gugur)

- Koreksi audit sendiri: PTS-overflow HLS GUGUR (`hlsSegmentDurationUs` sudah jepit 24 jam + playlist max 1MB → sum tak bisa overflow); klaim "writeTrackPts sudah grow" juga salah (grow hanya di writeAacFrames).
- 4132d9f fix(security) Crypto: reset kunci hanya bila rantai exception memuat KeyPermanentlyInvalidatedException (+ `isKeyInvalidated` internal + test); gagal lain langsung fallback tanpa menyatimkan kredensial lama.
- b5c5692 fix(download) muxer: `writeAll` baca ulang buffer lebih besar bila frame melebihi klaim (tanpa advance), cap 64MB → IOException aman bukan OOM (+ tambah import IOException, val→var; pesan EN agar lolos guard i18n).
- Temuan #4 (token partial ke player eksternal) by-design time-bound → tanpa perubahan kode.
- Guard: audit 0/0, check_repo 9/10 (yaml-env). Compile penuh di CI.
