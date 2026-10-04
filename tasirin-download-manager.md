# Memori Sesi — Tasirin Download Manager

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-download-manager` — download manager Android (Kotlin, minSdk 21, targetSdk 36).
- Aturan main (ringkas dari `AGENTS.md`): build resmi HANYA via CI, DILARANG install SDK lokal; UI Inggris, komentar Indonesia; commit `type(scope): deskripsi`; jangan ubah `versionName`/`versionCode` manual (CI bump per run); sumber remote web = `remote.src.html` + `python3 scripts/prepare_remote.py` (jangan edit `assets/remote.html` manual); guard `scripts/check_repo.py` + `scripts/security_audit.py`; perubahan kode wajib entri `CHANGELOG.md`; setelah fix langsung push tanpa pantau workflow (aturan 19).

## Status terakhir (2026-10-03 15:15 UTC, HEAD 004f63c)

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

## Sesi tombol remote lanjutan (2026-10-04 00:06 UTC, push main sukses)

- Perintah user: "lanjutkan" — audit saudara bug `moveHere` (commit 96b8c0a) di `remote.src.html`: semua situs `disabled = true` dicek satu per satu.
- 1 bug sekeluarga ditemukan & diperbaiki (commit 005f1c8): `fsLoadMore()` hanya mengaktifkan lagi tombol di jalur error — load-more sukses yang masih menyisakan halaman, dan respons basi (`seq !== fsLoadSeq` saat navigasi di tengah fetch), membuat tombol "Load more" lumpuh sampai reload. Kini tombol dipulihkan di `finally` selama masih menempel di DOM (`isConnected`; tombol yang di-remove karena tak ada sisa dilewati).
- Yang dicek dan aman: `runFsActions`/`fsTaskCancelBtn` (diaktifkan lagi tiap `showFsTask`), tombol upload (callback + catch), `moveYes` (sudah `finally` di 96b8c0a).
- Guard: `prepare_remote --check` OK (sinkron + JS valid + UI Inggris + smoke upload), `security_audit` 0/0, `check_readme_sync` sinkron, `diff --check` bersih. Push main sukses tanpa pantau workflow (aturan 19).

## Sesi fix 3 temuan minor (2026-10-04 00:05 UTC, push main sukses)

- Perintah user: "perbaiki semuanya" — 3 commit terpisah (satu tujuan per commit) + entri `CHANGELOG.md` tiap commit, push `main` `004f63c..00a903f` tanpa pantau workflow (aturan 19).
- Commit: `0bace1c` fix(download) ukuran importStream dari stat file asli; `dd5acde` fix(server) tolak `chunk < -1`; `00a903f` fix(app) cap thumb-cleanup hanya bila sukses.
- Guard: `security_audit` 0/0, `check_repo.py` 10/10 SEMUA SEHAT.
