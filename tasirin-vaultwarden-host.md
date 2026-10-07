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

## Sesi #13 — 2026-10-07 03:05 UTC (selesai)
- Perbaiki gagal build atas perintah user (2 run merah, 1 run hijau):
  - Run `37564259631` (head `e4a6486`) gagal 1 test: `symlinkIndukBersihDiJvm` — fail-closed baru menganggap stub `android.system.Os` di JVM sebagai perangkat.
  - Coba 1 `0d566a6` (deteksi pesan "Stub!") tetap merah: stub AGP di CI tak selalu melempar (bisa pulang null → NPE tanpa pesan).
  - Coba 2 `da4fab5` hijau: `diJvmUnitTest()` via `java.vm.name` (Dalvik = perangkat) + uji `jvmUnitTestTerdeteksi`; run `37565963777` success, rilis `v1.37.4` 7 aset lengkap.
- Pelajaran: jangan deteksi stub Android via pesan exception; pakai nama VM yang deterministik.
- Verifikasi: pantau CI atas perintah eksplisit user (pengecualian aturan #13).

## Sesi #14 — 2026-10-07 03:38 UTC (selesai)
- Audit agresif lanjutan atas perintah user (baca-saja): 6 temuan baru (3 sedang + 3 rendah). Offset bot, redirect host, zip-slip, provider, PIN sudah terverifikasi bersih.
- Perbaiki semuanya atas perintah user, 3 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `ee4c9f6 fix: peringatan chat grup Telegram dan ID berawalan plus` (Util.cocokChat strip `+`, Util.chatAdalahGrup + peringatan sekali per proses di TgBot.pollOnce + 2 uji).
  - `115c48d fix: throttle spoof siaran tanggal dan boot` (AlarmReceiver DATE_CHANGED throttle 60 dtk; BootReceiver throttle 60 dtk via bolehAlarmJalan).
  - `498ce9a fix: ambang jam clipboard dan batas tumpukan export` (LogActivity BATAS_CLIP_WALL_MS 4e11 + clipPakaiWallClock + uji; SettingsActivity pilihHapusBatasExport cap 3 + 2 uji).
- Pelajaran: siaran sistem (BOOT/DATE_CHANGED) tak bisa disyaratkan rahasia (legit pun tak membawanya) — throttle adalah pertahanan yang tepat, bukan secret-check.
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.

## Sesi #15 — 2026-10-07 03:45 UTC (selesai)
- User lapor gagal build run `37567656916` (head `498ce9a`): 1 test merah `SettingsActivityTest.batasExportPertahankanPendingSegar` (340 tests, 1 failed).
- Akar: ekspektasi test benar, kode produksi salah — nama dikecualikan tak memakan jatah batas sehingga pending basi + 3 file lolos cap.
- Fix `99b4e9c` + push (tanpa build lokal / tanpa pantau): `simpan++` dipindah sebelum cek kecualikan.
- Pelajaran: pengecualian dari batas harus tetap dihitung dalam budget, bila tidak cap bocor +1 tiap siklus.

## Sesi #16 — 2026-10-07 03:52 UTC (selesai)
- User lapor gagal build lagi run `37568189123` (head `99b4e9c`): test yang sama merah. Coba 1 salah: `simpan++` sebelum skip tak berpengaruh karena nama dikecualikan paling tua (diurut terakhir).
- Akar benar: pengecualian harus mengurangi jatah (`jatah = batas-1`), bukan dihitung di urutan. Disimulasikan murni via python (2 skenario PASS) sebelum push.
- Fix + push (tanpa build lokal / tanpa pantau): `fix: jatah batas dikurangi pengecualian agar cap tepat`.
- Pelajaran: exclusion-from-cap = kurangi budget, bukan hitung-di-urutan — beda hasil bila item dikecualikan bukan yang terbaru.
- Build sesi #16 user konfirmasi hijau (fix jatah cap lolos CI).

## Sesi #17 — 2026-10-07 (selesai)
- Audit agresif lanjutan: tanpa kritikal/tinggi/sedang; 3 rendah + 1 info. Area sensitif (crypto, restore, provider, redirect, PIN) terverifikasi bersih.
- Perbaiki 2 yang beneran bug (2 commit + 1x push, tanpa build lokal / tanpa pantau):
  - `b2cd06e fix: dialog izin tampil sekali per proses walau baru boot` (StoragePerm.bolehTampilDialogKelola + uji).
  - `6af3b50 fix: cache IP atomik agar pembaca lintas thread tak dapat versi campur` (ServerService IP_LOCK + ipCacheSegar + uji).
- Sengaja tak diubah: polling bot 20 dtk (trade-off remote-control by-design) dan `/ca` tanpa PIN (materi publik).

## Sesi #18 — 2026-10-07 (selesai)
- Audit agresif putaran ke-9: tanpa kritikal/tinggi/sedang; 1 rendah (pasangan cache lintas-thread tak atomik).
- Verifikasi: wall-clock bot tak perlu dikunci (thread poll tunggal serial); scope fix hanya Updater.latestVersion + readBundledVersionRaw.
- Fix `68130f9` + push (tanpa build lokal / tanpa pantau): `fix: kunci pasangan cache versi agar baca tulis atomik` (KUNCI_VERSI; fetch network tetap di luar kunci; bundled first-writer menang).

## Sesi #19 — 2026-10-07 04:39 UTC (selesai)
- Audit agresif putaran ke-10 (baca-saja): 3 temuan baru (2 sedang + 1 rendah). Area lama (redirect, zip-slip, provider, PIN-bruteforce, port, thread-cache, crypto, samaran-log) terverifikasi bersih; tmp impor terenkripsi sudah dibersihkan (Batal/dismiss/5x).
- Perbaiki semuanya atas perintah user, 3 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `c8ff07e fix: alarm_secret tak ikut export config agar rahasia alarm tak bocor` (SECRET_PREF_KEYS + KEY_ALARM_SECRET; import allowlist sudah abaikan + uji).
  - `aaab46e fix: kunci grace PIN terpisah agar commit disk tak blokir cek grace` (KUNCI_GRACE; catatHasil tetap synchronized, perilaku atomik sama).
  - `7b8274c fix: samaran tg_pass berhenti sebelum kunci berikut agar konteks tak hilang` (lookahead tanpa menelan; simulasi python 4 skenario PASS + uji).
- Pelajaran: secret per-perangkat wajib masuk daftar kecualikan export sejak lahir; monitor kelas jangan dibagi antara I/O disk dan cek UI cepat; pola samaran rakus butuh lookahead agar tak menelan konteks.
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.

## Sesi #20 — 2026-10-07 05:15 UTC (selesai)
- Audit agresif putaran ke-11 (baca-saja, tanpa ubah kode): sisir seluruh modul (~23rb baris). Tanpa kritikal/tinggi/sedang; 3 rendah + 1 info.
- Temuan baru: (1) Rendah — `tanyaPasswordImpor` 5x per-dialog bisa di-reset buka-ulang (counter lokal `SettingsActivity.java:2143`); mitigasi: password terlihat di Settings bagi pemegang HP, file .enc bisa brute-force offline. (2) Rendah — plaintext sementara export terenkripsi (`SettingsActivity.java:1940`) bertahan bila kill -9 di jendela tulis; sweeper hanya jalan di onCreate + lewati file <TTL. (3) Rendah — `AutoUpdate.java:86` `sp.getLong` mentah (ClassCastException → retry unduh makan kuota sekali; heal race vs onCreate). (4) Info — `binaryAssetUrl` strip satu 'v' tak terjangkau (pin divalidasi `normalisasiPinVersi`).
- Terverifikasi bersih: handler-leak MainActivity (`onDestroy:279`), orphan pending LogExport (`:93-103`), cap iterasi PBKDF2 anti-DoS (`PinCrypto.java:141`), `normalisasiPort` total, TOCTOU provider, `TUGAS_BERAT` queue-full (`TgBot.java:1357`), `DEFAULT_DATA_DIR` tinggal deklarasi, `stempelUnik` 48-bit, allowlist import + SECRET_KEYS, split pesan 4000, `authDangerous` fail-closed, decrypt VWB2 SHA256-dulu, `restoreFromZip` allowlist+zip-slip+aturan WAL.
- Belum diperbaiki (tunggu perintah "perbaiki"): 3 rendah di atas.

## Sesi #21 — 2026-10-07 05:30 UTC (selesai)
- Perintah user "perbaiki semuanya": 3 temuan sesi #20 + 1 temuan baru, 3 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau).
- `c4a7b86 fix: baca aman gagalAt auto-update` (`AutoUpdate.java:86` getLong mentah → `amanLong`; prefs korup tak bakar kuota tiap buka).
- `0950fc5 fix: plaintext sementara export terenkripsi selalu disapu` (prefix khusus `app-config-enctmp-` tak pernah dibagikan + sapu tanpa pandang umur; tak makan jatah cap + uji `sisaEnkripTmp`).
- `771c25f fix: dialog password import di UI thread + budget lintas dialog` (temuan baru saat bedah: `tanyaPasswordImpor` dibuat di worker runBusy = crash ViewRoot tanpa Looper; seluruh dialog pindah `ui.post`, dekrip PBKDF2 di worker `vw-import-dec` + tombol dikunci, budget 5x kumulatif per sidik SHA-256 berkas + gerbang di `importConfig` + 3 uji baru).
- Pelajaran: tiap `AlertDialog.Builder`/`EditText` baru wajib cek thread pemanggil (importConfig = worker); counter keamanan wajib kunci identitas objek (sidik isi) bukan identitas sementara (path tmp unik).
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.

## Sesi #8 — 2026-10-07 (selesai)
- Verifikasi agresif atas 20 temuan audit lalu (baca kode + rg, tanpa build lokal): kutipRocket, TOCTOU resume, battery-perm, SECURE_RANDOM, race process, healthTick/onDestroy, TgBotReceiver wakelock, PinGate async, clipboard kill-window, port UI, sleep worker, alarm-exact fallback, FileShareProvider scope, trim log, null-guard import, zip-slip, workflow anchor, tungguBootStabil, loop unduh binary (kandidat sesi #6).
- Vonis: semua sudah aman — dataDirAman tolak kutip/newline/kontrol/koma-kurawal; SHA akhir fail-closed; battery-perm dipakai Settings; onDestroy removeCallbacks; receiver wakelock finally; port dinormalisasi (sesi #5); unzip cek leksikal+kanonis+cap; workflow assert anchor; tungguBootStabil selalu di worker; tryUpdateVersi prioritaskan versi file + tulis marker (kandidat sesi #6 sudah masuk).
- Tidak ada patch/commit ke repo app (hindari churn + CI sia-sia). Sisa residual risiko rendah by-design: granularity lastModified FAT, kill-window ms PinGate, clipboard antar-kill (dibersihkan saat buka berikut).

## Sesi #9 — 2026-10-07 (selesai)
- Fitur baru atas saran user: halaman login PIN layar penuh (`PinActivity`) pengganti popup dialog — brand + kolom PIN + Buka/Keluar, D-pad, portrait+landscape ID sama, FLAG_SECURE.
- `6176fca feat:` 9 file (PinActivity, 2 layout, test, Main/Settings/manifest/strings/CHANGELOG), push ke `main`. Grace/lockout/upgrade-hash tetap via PinGate/PinCrypto; batal/Back = finish agar tak fail-open.
- Verifikasi milik CI (tidak pantau build sesuai aturan).
- `14008a7 fix:` kurung tutup `onActivityResult` Settings hilang saat pasang cabang REQ_PIN (gagal compile CI `illegal start of expression`); tambah `}` + push. Verifikasi milik CI.
- `8499e0a fix:` ceiling menit lockout (+59999) — 1 uji `PinActivityTest` gagal di CI; push + pantau sampai `37580084500 completed/success`. Halaman login PIN hijau.
