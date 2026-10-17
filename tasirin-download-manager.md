# Memori Sesi — Tasirin Download Manager

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-download-manager` — download manager Android (Kotlin, minSdk 21, targetSdk 36).
- Aturan main (ringkas dari `AGENTS.md`): build resmi HANYA via CI, DILARANG install SDK lokal; UI Inggris, komentar Indonesia; commit `type(scope): deskripsi`; jangan ubah `versionName`/`versionCode` manual (CI bump per run); sumber remote web = `remote.src.html` + `python3 scripts/prepare_remote.py` (jangan edit `assets/remote.html` manual); guard `scripts/check_repo.py` + `scripts/security_audit.py`; perubahan kode wajib entri `CHANGELOG.md`; setelah fix langsung push tanpa pantau workflow (aturan 19).

## Sapuan Android 8+ jilid 3 (2026-10-13, tanpa commit — bersih)

- Perintah user (ulangan ke-2): sapuan teliti seluruh kode, sikat inefisien/sampah/bug Android 8+.
- Area disisir (fokus lapis server/engine/remote): monitorLoop 30 mnt + probe HEAD 8 dtk + fallback Range 0-0 (anti lapor 1-byte), globalRateLimiter setLimit tanpa restart, snapshotJson cache + itemsSignature 64-bit + rebuild tanpa keys() + publikasi atomik, ServerLog cap 300x400 + snapshot revisi, DownloadRepository satu-parse + credCache + lock monitor tunggal + degraded-guard, autoOpen map in-place + prune ambang, SSE client + polling adaptif 2s/10s + reconnect counter, Updater 512KB-cap + cache-hanya-saat-exception, checkUpdate/about di IO, SocialMediaExtractor timeout 4-6 dtk + total-timeout.
- Hasil: tidak ada sampah/bocor/bug Android 8+ baru yang layak dihapus — tanpa perubahan kode.
- Guard: `verifikasi-path` LOLOS, `security_audit` 0/0, `prepare_remote --check` OK + smoke OK, `check_readme_sync` OK, tree bersih.

## Sapuan Android 8+ jilid 2 (2026-10-13, tanpa commit — bersih)

- Perintah user (ulangan): sapuan teliti seluruh kode, sikat inefisien/sampah/bug Android 8+.
- Area disisir ulang: SSRF guard DNS (worker-thread, fail-open), dialog probe sosmed (Dispatchers.IO + debounce 450ms + guard basi), StorageCleanup (hanya saat start, throttle monotonik), FileSaver StatFs multi-volume (per-start bukan per-tick), adapter payload progres + grouping satu-pass + DIFF field-by-field, progressSig/toolbar sig, StoragePrefs cache (prefs instance + collapsed set), thumbnail lock-per-media + failure TTL + staging, SseStream antrean 32 + poison + heartbeat, HttpBody/Streams zero-read guard, Gallery scope.release di onDestroy + trimMemory, LogActivity poll start/stop + export, Settings renderServer cache-first + refresh async TTL 10 dtk, remote fmtDate tunggal + tanpa alert/debug, Updater satu-parse + cache hanya saat exception.
- Hasil: tidak ada sampah/bocor/bug Android 8+ baru yang layak dihapus — tanpa perubahan kode.
- Guard: `verifikasi-path` LOLOS, `security_audit` 0/0, `prepare_remote --check` OK + smoke OK, `check_readme_sync` OK, tree bersih.

## Sapuan Android 8+ (2026-10-13, commit 241c661, push main sukses)

- Perintah user: sapuan teliti seluruh kode, sikat inefisien/sampah/bug Android 8+, plus tanya versi Android perubahan drastis.
- Area diverifikasi bersih: regex hoist semua (HlsParser/Engine/ServerSecurity/SocialMediaExtractor top-level), TlsCompat cache, SpeedTracker EMA, tick MainActivity 400ms+sig, adapter payload+cache warna/tint, statPool auto-heal 2-4 thread, snapshot throttle, upload lock per-ID, galeri token/diff, WebView destroy+removeCallbacks, PendingIntent IMMUTABLE, channel notif, JobScheduler boot, FGS dataSync+startForegroundCompat, izin POST_NOTIF/WRITE_23-28/AllFiles, desugaring aman.
- 1 fix: `HttpControlServer.ipv4Addresses()` memuat semua interface apa adanya (VPN putus/P2P idle/IMS, link-local 169.254.x.x, hostAddress kosong jadi `http://:port/`, urutan acak bikin firstOrNull lotre) — kini skip interface mati (`isUp` fail-open), saring link-local, `mapNotNull` buang kosong, `distinct+sorted` deterministik. 4 pemanggil (Settings x3, MainActivity openRemote) ikut sembuh tanpa ubah signature.
- Guard: `git diff --check` bersih, `verifikasi-path` LOLOS, `prepare_remote --check` OK, `security_audit --self-test` OK, `check_readme_sync` OK. Push main sukses tanpa pantau workflow (aturan 19).

## Status terakhir (2026-10-17 12:31 UTC — aturan maraton + sub-agen lintas repo)

- Permintaan owner: "terapkan aturan maraton perbaikan dan subagest ini ke semua repo yang di kelola memori ai" → `AGENTS.md` repo ini +aturan 21 (**mode perbaiki = maraton**, tetap patuh aturan 19: tanpa memantau workflow) +aturan 22 (**audit menyeluruh = 2–5 sub-agen paralel per area + verifikasi mandiri** tiap klaim berat ke kode sebelum masuk laporan/patch). Versi kanonik di `SOUL.md` memori agen.
- Commit docs-only `e51da4b` (push `main`, tanpa build/release — `paths-ignore`); guard lokal `check_repo.py` 11/12 (hanya "admin konsisten" gagal karena modul `yaml` tak tersedia — pra-ada, dibuktikan dengan `git stash`), `git diff --check` bersih.
- Sebelumnya (2026-10-13 07:15 UTC): HEAD `1837c2a` (Android 15 `onTimeout` + battery-exemption + `READ_EXTERNAL_STORAGE` API 29); sapuan jilid 22–27 bersih berturut-turut.

## Tugas terbuka

- Pantau CI pasca-`1837c2a`. Pola langganan: `Collections.newSetFromMap` (bukan `newKeySet`, minSdk 21); pesan commit ASCII murni; no force-push di `main` protected.

## Cara pakai file ini

- Awal sesi: baca file ini saja. Arsip: `archive/tasirin-download-manager-arsip.md`.
- Akhir sesi: tambah seksi `## YYYY-MM-DD HH:MM UTC — ...`, update Status terakhir, commit + push.

## 2026-10-13 01:10 UTC — percobaan betulkan pesan commit 0d8366e (GAGAL, dibiarkan)
- User setuju pesan commit diperbaiki → amend lokal sukses (`43e9b5a`, pesan ASCII bersih), tapi `push --force-with-lease` DITOLAK (`protected branch hook declined`): branch `main` protekted, rewrite history tak diizinkan.
- Tindakan: lokal di-`reset --hard origin/main` (kembali 0d8366e, tree bersih) agar tak divergen. Pesan cacat tetap di history; kode + CHANGELOG benar. Pelajaran: (1) cek pesan `git log` sebelum push; (2) jangan janjikan amend di branch protected — verifikasi proteksi dulu.

## 2026-10-13 01:20 UTC — fokus D-pad oranye ala vault (push da3e265)
- Perintah user: fokus D-pad kadang biru tua (salah pilih) — buat selalu oranye tebal mirip vaultwarden-host.
- Acuan vault: ring fokus SELALU aksen `#F57C00` 3dp + isi tekan tint oranye (`item_focus_bg`, `bg_btn_tv`, `bg_input_tv`, `bg_btn_primary`, `bg_btn_stop`, `bg_chip`); `state_focused` selalu item pertama.
- Native (9 drawable): `bg_btn_tv`/`bg_input_tv` ring biru→aksen 3dp; `bg_btn_accent` ring `primary_dark`→oranye tua `#8A3D00` 3dp (kontras di atas isi oranye); `item_focus_bg`/`bg_section_header` tint tekan biru→`#33F57C00` + stroke 2dp→3dp; `bg_chip` tint `#14`→`#33` + 3dp; `bg_btn_filled`/`bg_fab_pill` 2dp→3dp; `bg_ripple_item` (foreground row) biru→oranye agar tekan OK tak kilat biru. Biru tersisa hanya isi tombol (paritas vault).
- Remote: `--accent-soft` baru (terang+gelap); `input/select/textarea:focus` biru→aksen; semua `:focus-visible` 2px→3px (daftar, galeri, player; player tetap putih di atas video hitam).
- Guard: prepare_remote --check + smoke OK, verifikasi LOLOS (12 berkas), cek-cepat 0, audit 0/0, diff--check bersih. Pesan commit ASCII terverifikasi dulu (pelajaran 0d8366e). Push tanpa pantau; compile/lint ikut CI.

## 2026-10-13 01:42 UTC — sapuan penuh + 2 fix (push 1ae27db, db83cbe)
- Perintah user: scan seluruh kode semua area teliti (abaikan hemat token), hapus tak-efisien/sampah/bug Android 6+.
- FIX 1 KRITIKAL (download): `pendingRetries = ConcurrentHashMap.newKeySet()` butuh API 24 — di Android 5-6 (minSdk 21) lempar NoSuchMethodError saat DownloadEngine dibangun (= crash tiap startup, Error tak tertangkap catch Exception di App). Kini `Collections.newSetFromMap` seperti `failedHlsUrls` di sebelahnya (semantik thread-safe identik); komentar digabung. Ironis: file ini sudah mendokumentasikan larangan newKeySet untuk failedHlsUrls tapi pendingRetries lolos.
- FIX 2 (remote): 2 `alert()` blokir di form tambah (`No valid URLs found`, `Failed to add download`) — susah ditutup di TV box/D-pad, blokir halaman; kini `showToast(..., 3000, 'error')` non-blokir. `remote.html` diregenerasi (`289549 -> 250687` bytes).
- Diverifikasi bersih tanpa perubahan (lampaui 21 sapuan lama): desugaring aktif (desugar_jdk_libs 2.1.5) sehingga `removeIf`/`getOrDefault`/`withInitial` aman Android 6; `MediaStore.Downloads.*` hanya konstanta inline atau di balik guard SDK>=29; manifest (BOOT/BIND_JOB/DATA_SYNC/POST_NOTIF) lengkap; `fmtDate` tunggal; `extract.js` readable; SpeedTracker/QueueOrder/SegmentPlanner/ShareToken bersih; Updater IO-background; WebExtract onDestroy sudah ada.
- Pelajaran: `pgrep -f <nama>` menipu diri (cocok string perintah pgrep itu sendiri) — saring dengan `ps aux | rg` pola ganda atau `pgrep -f "[c]heck_repo"`.
- Guard: diff--check bersih, verifikasi-path LOLOS, prepare_remote --check + smoke OK, audit 0/0, readme sync OK. check_repo.py penuh tak selesai di container (menggantung tanpa output, kemungkinan sub-step lambat; guard individualnya semua hijau). 2 commit satu-tujuan + CHANGELOG per commit. Push main tanpa pantau (aturan 19); compile/lint/unit-test ikut CI.

## 2026-10-13 01:54 UTC — sapuan penuh jilid 22 (tanpa ubah kode, bersih)
- Perintah user: scan seluruh kode semua area teliti (abaikan hemat token), hapus tak-efisien/sampah/bug Android 6+.
- Hasil: TIDAK ADA temuan baru yang layak patch. Area yang disapu ulang: DownloadRepository/codec (satu-parse + credCache), HlsParser (contains-guard), AdtsAac/Muxer (lazy frame + buffer klaim), ServerLog/MediaStream/SseStream/ServerStreams (snapshot cache, parse sekali, POISON/PING), ServerThumbnail/Durations (strip-lock, failure TTL, prune-on-write), MediaLibrary scan (SQL prefilter + alias Android 5-6), Settings/Main lan IP (IO + cache 10 dtk + gen), Gallery (release scope, LRU cap 24MB), StorageCleanup/CrashLog/Permissions (monotonik, ThreadLocal, NEW_TASK guard), koneksi engine (timeout semua jalur via openAuthenticatedConnection), ekstraktor (PAGE_TIMEOUT + total 60 dtk), remote render/patchRow (guard DOM per tick, favicon hanya saat rebuild), extract.js readable, tanpa AsyncTask/Timer/JS-bridge/WebView-file-access.
- Guard: diff--check bersih, verifikasi-path LOLOS. Tanpa push (tak ada perubahan kode); compile/lint/unit-test tetap milik CI.


## 2026-10-13 06:49 UTC — sapuan penuh jilid 23 (tanpa ubah kode, bersih)
- Perintah user: periksa seluruh kode semua area, hapus inefisiensi/sampah/bug Android 6+.
- Status awal repo target bersih; HEAD `241c661`. Sapuan ulang daftar sumber, area API Android (SDK guards, MediaStore 29+, PackageInfo, Crypto API 23, Notification API 26/33), service/boot job, engine, server, UI, storage, resources, remote scripts. `pendingRetries` sudah memakai `Collections.newSetFromMap`; desugaring aktif untuk default method Java seperti `removeIf`/`getOrDefault`. Tidak ditemukan bug atau kode mati baru yang cukup terbukti untuk patch; tidak ada perubahan kode.
- Guard: `verifikasi-path.py`, `cek-cepat.sh`, `security_audit.py --self-test`, `check_readme_sync.py`, `prepare_remote.py --check` (via `check_repo.py`), dan `git diff --check` lolos. `check_repo.py` 11/12: gagal hanya validasi labeler karena modul Python `yaml` tidak tersedia. Tidak menjalankan build/test/lint Android.


## 2026-10-13 06:57 UTC — sapuan Android 10+ jilid 24 (commit dbbae9f, push main sukses)
- Perintah user: scan teliti semua area, bersihkan inefisiensi/sampah/bug Android 10+.
- Temuan: API 29 memakai scoped storage karena targetSdk 36; galeri query MediaStore video pihak ketiga, tetapi `READ_EXTERNAL_STORAGE` tidak dideklarasikan dan `Permissions.missingRuntime()` tidak pernah meminta izin itu. Query bisa kosong/ditolak meski tidak ada masalah di Android 11+ yang meminta All files access. Fix satu area storage: permission `READ_EXTERNAL_STORAGE` dibatasi `maxSdkVersion=29`, diminta runtime hanya API 29 melalui alur Main yang sudah ada; README.id/en dan CHANGELOG disinkronkan. Android official docs terverifikasi: media milik aplikasi tanpa izin saja yang terlihat di scoped storage; akses media lain memerlukan READ_EXTERNAL_STORAGE.
- Area lain yang ditinjau: penyimpanan/izin, FileSaver, MediaLibrary/MediaStore, ZIP MediaStore, boot/service foreground, manifest, lifecycle dan izin media. Tidak ada temuan lain yang cukup terbukti untuk patch.
- Guard: prepare_remote --check, readme-sync, security-audit self-test, cek-cepat, diff--check lolos; verifikasi-path lolos dengan peringatan statis umum soal permission baru walau alasan sudah terdokumentasi README. `check_repo.py` 11/12; gagal hanya admin konsisten karena modul Python `yaml` tidak tersedia. Tidak menjalankan build/test/lint Android. Commit `dbbae9f` di-push ke main; CI tidak dipantau (sesuai aturan repo).


## 2026-10-13 07:02 UTC — sapuan Android 12+ jilid 25 (commit 71fbfb0, push main sukses)
- Perintah user: scan seluruh area untuk performa/stabilitas Android 12+.
- Area audit: target/manifest, foreground service + boot JobScheduler, notification channel/runtime permission, semua PendingIntent, baterai, network callback, storage, MediaStore, updater/intent compat. Tidak ditemukan PendingIntent mutable yang tak perlu, alarm exact, atau API barunya tanpa guard.
- Fix: `SettingsActivity.requestBatteryExemption()` memakai `Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`; tanpa `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` di manifest Android menolak intent. Deklarasi permission ditambahkan, README id/en menjelaskan pengecualian baterai opsional, CHANGELOG ditambah. Docs resmi Android mengonfirmasi izin manifest diperlukan.
- Guard: prepare_remote --check, readme-sync, security-audit self-test, cek-cepat, verifikasi-path (lolos dengan peringatan umum permission baru), diff--check lolos. `check_repo.py` 11/12: hanya admin konsisten gagal karena modul Python `yaml` tidak ada. Tidak menjalankan build/test/lint Android. Commit `71fbfb0` di-push ke main; tidak memantau CI.


## 2026-10-13 07:10 UTC — sapuan Android 14+ jilid 26 (commit 1837c2a, push main sukses)
- Perintah user: audit kinerja/stabilitas semua area untuk Android 14+.
- Area ditinjau: FGS permission/type, NotificationChannel & POST_NOTIFICATIONS, semua PendingIntent immutable, boot JobScheduler, battery exemption, storage/media permission, service starts/network callbacks, manifest API checks. FGS `dataSync` type/permission sudah lengkap untuk Android 14; `onTimeout` tidak dibutuhkan di Android 14.
- Temuan untuk Android 15+ (termasuk targetSdk 36): tipe `dataSync` dibatasi 6 jam kumulatif saat aplikasi di latar. `DownloadService` tidak override `Service.onTimeout(startId, fgsType)`, sehingga sistem dapat melempar `RemoteServiceException` dan kerja download/server tidak dihentikan dengan tertib. Fix: callback API 35 menjeda semua download, memakai save debounce antrean (agar callback segera kembali), menghentikan HTTP server, remove notification, stopSelf. README id/en dan CHANGELOG menyebut limit dan progres parsial terjaga. Tidak memigrasikan ke user-initiated job/WorkManager karena perubahan arsitektur besar di luar patch audit minimal.
- Guard: `check_repo.py` 11/12; hanya admin konsisten gagal karena modul `yaml` tidak tersedia. `verifikasi-path.py`, cek-cepat, `prepare_remote --check`, readme-sync, security audit self-test, parse XML dan diff-check lolos; verifikasi-path memberi warning satu callback platform `onTimeout` tanpa test. Tidak menambah/menjalankan test atau build Android sesuai aturan. Commit `1837c2a` di-push ke main; CI tidak dipantau.


## 2026-10-13 07:15 UTC — sapuan Android 6+ jilid 27 (tanpa ubah kode, bersih)
- Perintah user: audit seluruh area untuk kinerja/stabilitas Android 6+. HEAD target `1837c2a`, working tree bersih.
- Sapuan API compatibility ulang: helper minSdk paths/SDK guards, Crypto/KeyStore API 23 fallback, NetworkCallback API 24 fallback, NotificationChannel API 26 guard, MediaStore/RELATIVE_PATH API 29 guard, all-files API30, notification permission API33, PendingIntent immutable, FGS type permission, boot JobScheduler dan callback Android 15 `onTimeout`. Modern default methods (`removeIf`, `getOrDefault`) dilindungi core library desugaring. Tak ada temuan baru atau kode tak efisien yang cukup terbukti untuk dihapus.
- Guard `check_repo.py` 11/12: semua guard termasuk remote, path, cek-cepat, smoke, readme, audit keamanan dan whitespace lolos; gagal hanya admin konsisten karena modul Python `yaml` tak tersedia. `git diff --check` bersih, working tree tetap bersih. Tidak menjalankan build/test/lint Android.

## 2026-10-17 12:31 UTC — aturan maraton + sub-agen ditulis ke AGENTS.md (docs-only, push)
- Permintaan owner: "terapkan aturan maraton perbaikan dan subagest ini ke semua repo yang di kelola memori ai".
- Perubahan (`e51da4b`, push `main`, docs-only → `paths-ignore` jadi tanpa build/release): `AGENTS.md` +aturan 21 (**mode perbaiki = maraton** — kerjakan temuan audit sampai habis, satu temuan satu perbaikan akar, langsung commit + push, build gagal didahulukan; tetap patuh aturan 19 = tanpa memantau workflow) +aturan 22 (**audit menyeluruh = 2–5 sub-agen paralel per area + verifikasi mandiri** tiap klaim berat ke kode `rg`/`sed`; temuan wajib `file:baris` + dampak + skenario pemicu + level bahaya).
- Kanonik lintas repo: `SOUL.md` (memori agen) seksi "Aturan maraton perbaikan & sub-agen"; salinan juga di `AGENTS.md` Red-Eye-Mobile §5, netradar 14–15, tasirin-vaultwarden-host 17–18.
- Guard: `check_repo.py` 11/12 — "AGENTS.md completeness" OK, gagal hanya "admin konsisten" karena modul Python `yaml` tak tersedia (pra-ada: diuji ulang dengan perubahan di-`stash`, tetap sama). `git diff --check` bersih.
