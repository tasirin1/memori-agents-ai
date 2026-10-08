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
- `0c8b8f2 fix:` ellipsis `...` jadi `…` di `pin_memeriksa` (anotasi lint Ellipsis). Verifikasi milik CI.
- Audit kode baru PIN (PinActivity, 2 layout, test, wiring Main/Settings, manifest, strings): tak ada bug fungsional — grace tak bisa diperpanjang tanpa PIN (launch hanya bila grace habis; early-OK hanya ms setelah unlock sah), Back/Keluar fail-closed via finish pemanggil, ID layout sama, REQ unik, rotation aman via configChanges, worker vs hash segar + upgrade aman.
- `d78aa04 chore:` buang 2 import tak terpakai (EditText/InputType) di MainActivity. Verifikasi milik CI.

## Sesi #21 — 2026-10-07 06:33 UTC (selesai)
- Audit putaran ke-11 atas perintah "cek seluruh kode": 5 temuan baru (semua rendah), area lama bersih (redirect, zip-slip, provider, PIN-bruteforce, port, crypto, samaran-log, export-secret).
- Perbaiki semuanya, 3 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `f765eef fix: grace PIN tak diperpanjang ganda dan hash hilang lanjut OK` (catatPinDibuka guard dalamGrace di Main+Settings; PinActivity hash-hilang RESULT_OK; bersihkanInput langsung usai salin).
  - `ebfbd57 fix: kandidat PIN bot bertitik/garis-miring bukan PIN implisit` (TgBot.pisahkanPin tolak `.`/`/`/`\` implisit + 4 uji baru; simulasi python 14 skenario PASS).
  - `21242c8 fix: layar PIN dikecualikan dari recents` (manifest PinActivity excludeFromRecents; ID layout portrait/landskap sama persis).
- Pelajaran: callback sukses berlapis (activity + onActivityResult) wajib idempoten tanpa perpanjang jendela; fallback PIN implisit wajib tolak pola mirip-file/versi agar typo tak bakar lockout.
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.

## Sesi #22 — 2026-10-07 (selesai)
- Pasang deskripsi repo GitHub (sebelumnya kosong): satu baris Indonesia sesuai tagline README. Via `gh repo edit`, tanpa commit/CI.

## Sesi #23 — 2026-10-07 (selesai)
- User: deskripsi repo Inggris + README default Inggris + README Rusia + bahasa default app Inggris.
- Deskripsi repo via `gh repo edit` (EN, tanpa commit/CI).
- Docs `9da4697`: README.md=EN (dari en), README.id.md=ID, README.ru.md baru (RU, 2 selip bahasa diperbaiki), switcher 3 bahasa, AGENTS.md (aturan bahasa + ref README + values-in), CHANGELOG, cek-cepat.sh cek 3 README. CI skip (docs-only).
- Code `ffcbec1` + push (build APK jalan di CI, tanpa pantau): values/strings.xml EN (147 key, placeholder cocok), values-in/strings.xml ID; literal UI EN di Main/Settings/Log/LogExport/Pin/AutoUpdate-notif; PinActivityTest ikut EN. Guard lokal hijau (cek-cepat.sh exit 0, diff-check bersih).
- Batasan sadar: log diagnostik `[app]/[tg]` + pesan bot Telegram tetap Indonesia (test-anchored, mis. webVaultBerubah); tes lain pakai placeholder netral-bahasa sehingga aman.
- Pelajaran: literal pendek ("Ya", "v", "terbaru") wajib ganti via konteks baris-penuh; escape Java `\n`/`\u` di python butuh backslash ganda; cek-cepat.sh wajib ikut rename file.
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.

## Sesi #24 — 2026-10-07 (audit agresif, baca-saja)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug". Mode baca-saja (tanpa ubah kode app), cek-cepat.sh exit 0.
- Area disisir: ServerService start/stop/watch/restart/health/ensureBinary/gantiAtomik/detectBinaryVersion, Updater kunciUnduh/redirect/SHA, TgBot auth/pisahkanPin/restore, TgBackup restore/zip-slip/checkpointWal, Settings runBusy/export-TTL, LogActivity clipboard, Boot/AlarmReceiver, TgBotReceiver, PinActivity/Gate/Crypto, TlsCert, FileShareProvider, Util, AutoUpdate.
- Bersih (dugaan gugur): kunciUnduh pakai ConcurrentHashMap (bukan String-lock), LOG_TS selalu synchronized, readAllBytes dibatasi, tambahUkuranUnzip tanpa overflow, restore stop-server dulu (UI+bot), detectBinaryVersion ada watchdog 10 dtk + batas 50 baris, lockout PIN dual-clock wall+elapsed, FileShareProvider sudah anti-oracle, redirect https+GitHub-only.
- Temuan baru dilapor ke user: 2 sedang (export-TTL wall-clock; doRestore pegang kunci data selama unduh) + 2 rendah (throttle log wall-clock bikin refresh macet saat jam mundur; tebakan PIN pendek burns lockout = lockout-DoS kecil, by-design).
- Pelajaran: pola `currentTimeMillis - terakhir > X` selalu curigai jam-mundur; kunci global jangan dipegang selama I/O jaringan.

## Sesi #25 — 2026-10-07 (fix temuan audit #24, selesai)
- User: "perbaiki semuanya". 3 commit + push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `2f18d5d fix: TTL export dan throttle log pakai jam elapsed` (exportPlainPada + sapu basi + throttle appendUiLog di Settings/Main → elapsedRealtime; umur mtime negatif dijepit 0 agar file segar tak terhapus saat jam mundur).
  - `f9cb432 fix: kunci restore bot baru dipegang saat eksekusi` (doRestore: unduh+dekrip tanpa kunci, kunciRestore tepat sebelum restoreFromZip; finally lepas hanya bila dikunci).
  - `713774d fix: tebakan PIN pendek tak bakar lockout` (authDangerous: PIN <4 char ditolak tanpa catatHasil — tak mungkin benar sehingga hanya membuka lockout-DoS; sempat 1 commit gabung lalu dipecah via reset+apply-hunk agar satu commit satu tujuan).
- Guard: `git diff --check` bersih + cek-cepat.sh exit 0. Tidak ada test yang mengunci perilaku lama (TgBotTest hanya pisahkanPin murni).
- Pelajaran: jam dinding vs elapsed — pola `now - terakhir > X` selalu ganti elapsed bila untuk umur/TTL/throttle; kunci global jangan dipegang selama I/O jaringan; hunk terpisah satu file bisa dipecah via header-diff + apply --cached.
- Verifikasi milik CI (build-apk ringan); tidak memantau build sesuai aturan.

## Sesi #26 — 2026-10-07 (audit agresif #2, baca-saja)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug". Mode baca-saja, working tree bersih, cek-cepat.sh exit 0.
- Area disisir baru: pollOnce/offset/freshness/callback-PIN, MainActivity PIN-grace + refresh 1-detik, web-vault extract+swap, amanEntriZip/expectedHexEquals, LogExport SAF, enkripsi AES-GCM/PBKDF2 + zeroing, AutoUpdate, AlarmReceiver secret/throttle, rahasiaAlarm, redirect/hostGithubAman/hostTelegramAman, copyBinary, pingRinci/hostname-verifier, loopbackSslFactory cap, collectIps/formatHost, prepareTls/migrasi/bersihKunci, import-allowlist, kirimSinkron queue, healthTick worker, chatIdAman, PinCrypto iter-cap, tryUpdateVersi pin-restore, reset/revert guard, tukarPasanganAtomik, backup-integrity+retry.
- Bersih: semua jalur di atas sudah hardened (fail-closed + komentar desain konsisten).
- 1 temuan Sedang baru: regen TLS destruktif — ensureCertWithIps (ServerService.java:3053) hapus cert/key/ipFile DULU lalu panggil TlsCert.ensure yang sebenarnya atomik (.baru→swap, leaf lama dipertahankan bila gagal); hapus-dulu meniadakan jaring itu (IP berubah + storage penuh = cert bagus hilang, server mati total). Akar: ensure early-return leaf valid-waktu tanpa cek SAN, sehingga pemanggil terpaksa hapus dulu. Fix benar: flag paksa-regen-leaf di TlsCert.ensure, bukan hapus-dulu.
- Dilapor ke user, belum diperbaiki (tunggu perintah).

## Sesi #27 — 2026-10-07 (fix TLS destruktif, selesai)
- User: "perbaiki semuanya" (temuan audit #26). 1 commit + push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `e39deb2 fix: regen TLS atomik tanpa hapus-dulu` (TlsCert.ensure overload paksaLeaf; ServerService.ensureCertWithIps oper flag ipBerubah, hapus 3x delete-dulu; ips.txt ditulis hanya saat sukses seperti semula; TlsCertTest baru paksaLeafRegenerasiWalauLeafMasihValid — cabang tanpa-paksa adaptif bila DER tak terparse JVM agar tak flaky di CI).
- Akar: ensure early-return leaf valid-waktu tanpa cek SAN → pemanggil terpaksa hapus dulu. Kini regen lewat jalur .baru→swap yang sudah atomik; gagal generate = leaf lama tetap dipakai.
- Guard: `git diff --check` bersih + cek-cepat.sh exit 0. Kompilasi + unit test penuh milik CI (build-apk ringan).
- Verifikasi milik CI; tidak memantau build sesuai aturan.

## Sesi #28 — 2026-10-07 (build gagal → fix, selesai)
- CI gagal di commit e39deb2: `TlsCertTest.paksaLeafRegenerasiWalauLeafMasihValid` AssertionError (baris 234, ensure pertama null).
- Akar: TlsCert.ensure tak bisa jalan di JVM unit test — jalur buatLeaf memuat kunci CA via android.util.Base64 yang stub di unit test (melempar) → buatLeaf false → ensure null. Makanya dulu tak ada test yang memanggil ensure.
- Fix `16437ea`: buang test + 2 import tambahannya; overload paksaLeaf tetap делivered tanpa test (cabang satu-boolean, risiko rendah; verifikasi via CI + manual).
- Pelajaran: jangan tambah unit test untuk fungsi yang menyentuh API Android (Base64, dsb.) walau file-nya 99% murni — cek import dulu; stub android.jar melempar, bukan mengembalikan default.
- Push ke main; verifikasi milik CI, tidak memantau build sesuai aturan.

## Sesi #29 — 2026-10-07 (audit agresif #3, baca-saja)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug". Mode baca-saja, tree bersih, cek-cepat.sh exit 0.
- Area disisir baru: catatLog/tailLog/flush/rotasi, cleanupTempFiles vs staging konkuren, dataDirAman segmen/case, kutipRocket, migrasiPort, recordRestart window, isKernelRandomPanic, samarkanLog + semua pemakai, TgBot schedule/pendingIntent/jawabCallback, bukaIkutiRedirect/resume-reset, bolehIkutiRedirectGithub/sambungRedirect, provider query/getType/openFile, HttpsCompat cap, PinGate grace/lockout/catatHasilAsync, kunciBerikutnyaMs flat-5mnt, TgBackup.schedule exact/inexact + cancel lawas, Main Start/Stop flows.
- Bersih: semua di atas hardened/fail-closed.
- 1 temuan Sedang baru: Start saat update web-vault berjalan menghapus staging AKTIF — sisaStagingWebVault (Updater.java:640) cocok ke `web-vault.new-<cap>` unik, meniadakan klaim komentar stagingWebVault bahwa cleanup tak bisa membuang staging aktif; update gugur (versi lama aman, tinggal retry). Fix benar: registry staging aktif yang dilewati cleanup.
- Dilapor ke user, belum diperbaiki (tunggu perintah).

## Sesi #30 — 2026-10-07 (fix race staging web-vault, selesai)
- User: "perbaiki semuanya" (temuan audit #29). 1 commit + push ke `main` (`41ed89d`, tanpa build lokal / tanpa pantau CI):
  - `fix: lindungi staging web-vault aktif dari sapu cleanup Start` — registry STAGING_AKTIF (Set nama tersinkron, murni-JVM) + tandaiStagingAktif/lepasStagingAktif/stagingAktif di Updater; tandai sesudah mkdirs, lepas di 7 jalur gagal + 1 jalur sukses; cleanupTempFilesTerkunci lewati nama aktif; komentar basi stagingWebVault/KUNCI_WEBVAULT/cleanup diluruskan; test baru stagingAktif_lindungiDariSapuLaluLepas (murni, aman JVM).
- Guard: `git diff --check` bersih + cek-cepat.sh exit 0. Verifikasi milik CI.

## Sesi #31 — 2026-10-07 09:23 UTC (audit agresif #4 + fix semua, selesai)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug" lalu "perbaiki semuanya". Audit baca-saja dulu, lalu 3 commit + 1x push ke `main` (`606349e`, `7f26f13`, `029767d`, tanpa build lokal / tanpa pantau CI).
- Area disisir baru: manifest exported/receiver, build.gradle resConfigs, network_security_config, ProGuard, Util hostSama/kupasHostPort/sambungRedirect/hostGithubAman/hostTelegramAman, PinCrypto verify/unhex/derive, PinGate catatHasil/commit, ServerService ensureBinary/isValidBinary/copyBinary/gantiAtomik/healthTick worker/sendMessage worker, Updater checksum/resume, TgBot offset/pisahkanPin/lockout, TgBackup rahasiaAlarm/pendingIntent/sendMessage thread, FileShareProvider, TlsCert, StoragePerm throttle, LogExport SAF+legacy, Main/Settings lifecycle/removeCallbacks/pinExec shutdown, Alarm/BootReceiver, AutoUpdate.
- Bersih (fail-closed, tak dipatch): redirect https-only + host allowlist, iter-cap PBKDF2 (120k, sudah ada), lockout wall+elapsed ganda, rahasiaAlarm constant-time, health di worker + sendMessage di thread sendiri, pinExec.shutdownNow + cancel Future, removeCallbacksAndMessages di onDestroy, gantiAtomik .bak-restore.
- 4 temuan audit: (1 Sedang) unhex tanpa cap panjang → alokasi besar via pin_hash raksasa (prefs utak-atik/import jahat, pin_hash ikut export/import); (2 Rendah) komentar resConfigs basi (klaim default values/=Indonesia, padahal EN sejak sesi #23); (3 Rendah) LogExport pre-29 break saat I/O transient → gagal-simpan palsu; (4 Rendah, BATAL patch) export-plaintext: verifikasi ulang menunjukkan sudah termitigasi (TTL 2 mnt elapsed, sapu onResume/onDestroy/chooser-return/export, cache-internal, cap jumlah) — jendela sisa by-design untuk target async, hanya terbaca bila rooted. Tak patch yang tak rusak.
- Fix: `606349e fix: tolak heks raksasa di verify PIN sebelum unhex alokasi` (HEKS_MAKSIMAL=128 dua cabang + test heksRaksasaDitolak murni-JVM, aman CI); `7f26f13 fix: coba nama log baru saat I/O transient di Android pra-29` (break→continue, tetap 5x); `029767d chore: betulkan komentar bahasa default di build.gradle.kts`.
- 1 push sekaligus (bukan 3x) agar CI build-apk jalan sekali — kompromi sadar antara aturan #12 (jangan tunda push) dan #3 (hemat CI); tiap fix tetap commit terpisah agar mudah rollback.
- Guard: `git diff --check` bersih tiap commit. Verifikasi milik CI.

## Sesi #32 — 2026-10-07 (audit agresif #5, baca-saja)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug". Mode baca-saja, tree bersih, tanpa patch.
- Area disisir baru (belum disentuh sesi #29/#31): kutipRocket/ROCKET_TLS, dataDirAman per-segmen + kanonis, normalisasiPort/effectivePort, lanHost/formatHost/collectIps (zona kupas, fe80 ditolak, sort stabil), stopper thread + watchProcess (getrandom/port-direbut), TgBackup restore allowlist (normalisasiEntriZip/bolehTulisRestore/diterimaEntriZip), readAllBytes/bacaTerbatas cap 1MB, importConfig 512KB + tanyaPasswordImpor budget sidik, applyPrefsFromJson allowlist + keep perangkat, encrypt AES-GCM random salt/IV + cleanup parsial, maybeAutoBackup dedup harian, TgBot callback auth ruang + umur 24 jam + pesan-null fail-closed + daftar berbahaya tunggal, workflows permissions contents:write + concurrency grup, AutoUpdate notifikasi (immutable, private, try/catch), MainActivity refresh guard + restartHint sidik, PinActivity penuh (grace/hash-hilang/Back-finish/worker-verify), layout ID parity (script: sama persis), strings parity 147/147, volatile semua state lintas-thread, stempelUnik SecureRandom 48-bit.
- Bersih: semua di atas hardened/fail-closed. Tidak ada temuan Kritikal/Tinggi/Sedang.
- 3 temuan Rendah baru (dilapor, belum diperbaiki): (1) TgBot.java:495 `if (pesan != null)` mati setelah early-return null — hygiene; (2) PinActivity `entered` String PIN plaintext mengendap di heap selama PBKDF2 (immutable, tak bisa di-wipe; residual forensik, tanpa patch murah); (3) dataDirAman cek segmen >255 pakai char bukan byte — nama 200 emoji lolos cek lalu gagal mkdirs ENAMETOOLONG (pesan&Bingung saja).

## Sesi #33 — 2026-10-07 09:31 UTC (fix 3 temuan rendah audit #5, selesai)
- User: "Mau" (setuju bersihkan ketiganya). 3 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `7714b67 chore: buang cek null mati di tanganiCallback` (dedent programatik + verifikasi balance kurung, TgBot).
  - `3136e5c chore: dokumentasikan residu String PIN sebagai risiko diterima` (PinActivity; tanpa patch murah — String immutable, Editable sumber memang sudah dibersihkan).
  - `93181c4 fix: cek panjang segmen folder data dalam byte UTF-8` (ServerService + test dataDirAmanTolakSegmenMultibyte255Byte; fully-qualified StandardCharsets agar tak tergantung import).
- 1 push sekaligus agar CI jalan sekali; tiap fix commit terpisah. Guard `git diff --check` bersih. Verifikasi milik CI.

## Sesi #34 — 2026-10-08 01:49 UTC (audit agresif #6 + fix semua, selesai)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug" lalu "perbaiki semuanya". Audit baca-saja dulu (tanpa build lokal, Aturan No.1), lalu fix semua temuan.
- 4 temuan audit: (1 Tinggi) LogActivity.bersihkanBilaIsiKita finally baca ulang prefs sehingga timer basi menghapus penanda salinan baru (auto-hapus 30 dtk gugur, rahasia menempel); (2 Sedang) ServerService.killStaleVaultwarden bunuh via PID tanpa verifikasi ulang (start konkuren/PID-reuse bisa membunuh server fresh); (3 Rendah) throttle Alarm/BootReceiver statik saja, reset tiap proses mati; (4 Rendah, dugaan) TgBot.catatWall read-modify-write non-atomik.
- Bersih terverifikasi: PinCrypto.verify (try luar + cap iterasi/heks), Updater resume (perluResetResume + rangeCocok), TgBot callback auth + umur tombol, restore allowlist + kanonis, restartAttempt batas array, pinExec shutdown, FileShareProvider TOCTOU.
- Fix 4 commit + docs + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `d1c002c fix: timer basi clipboard tak hapus penanda salinan baru` (LogActivity: sidik asal ditangkap, finally pakai sidikKita).
  - `d0d46be fix: verifikasi ulang sebelum bunuh proses basi agar server fresh selamat` (ServerService: cek runningChildPid + pidMilikiServer ulang sebelum killProcess).
  - `ba68744 fix: throttle alarm dan boot tahan mati proses via prefs` (AlarmReceiver + BootReceiver + test throttleTersimpanMenutupResetProses).
  - `515258f fix: kunci tanda air wall-clock agar maksimum tak hilang saat poll tumpang tindih` (TgBot KUNCI_WALL di catatWall + muatWallMaks).
  - `882e9c2 docs: changelog audit clipboard kill throttle wall-clock` (md saja, CI dilewati).
- Guard `git diff --check` bersih tiap commit. Verifikasi milik CI (build-apk ringan).

## Sesi #35 — 2026-10-08 06:07 UTC (audit baca-saja, tanpa patch)
- User: "cek seluruh kode dan temukan bug". Mode audit baca-saja (SOUL: cek=kumpulkan temuan, jangan ubah kode). Tanpa build lokal (Aturan No.1), tanpa push app.
- Area disisir: Util/PinCrypto/PinGate/PinActivity, KernelCompat/StoragePerm/HttpsCompat, FileShareProvider (TOCTOU+symlink), TlsCert, ServerService (health/restart/stopAndWait/ensureBinary/cleanup), Updater (redirect+resume+hash), TgBot (auth grup/PIN/hapus pesan), TgBackup (zip-slip/allowlist/enkripsi/restore), LogActivity/LogExport (samarkan/clipboard), Main/Settings (clipboard/export), Alarm/BootReceiver (throttle), manifest.
- Temuan baru dilapor ke user (2 Tinggi: hapusPesan grup chatId<=0 blokir ID negatif; grup via @username fail-open; sisanya Rendah: Handler clipboard tanpa guard, toast salin bohong, throttle bypass sekali selepas reboot). Detail + level di chat sesi ini.
- Bersih terverifikasi: resume-hash prefix digest, stopAndWait dicek pemanggil, formatHost IPv6, redirect fail-closed + hostBerubah, restore allowlist + kanonis, PBKDF2 cap, clipboard sidik + penanda cocok.

## Sesi #36 — 2026-10-08 06:20 UTC (fix audit sesi #35, selesai)
- User: "perbaiki semuanya". 3 fix commit + 1 docs + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `0065ffe fix:` hapus pesan ber-PIN di grup (TgBot guard `<=0`→`==0`; ID grup negatif ikut dihapus).
  - `9794de6 fix:` username fail-closed (Util.chatPerluAnggapGrup baru + TgBot gate/warning + catch prefs→true; chatAdalahGrup tak berubah; uji baru).
  - `bc4e106 fix:` clipboard guard Looper null + boolean jujur (Log/Main/Settings; tanpa string baru, pakai galat_awalan).
  - `fb11e29 docs:` changelog.
- Temuan throttle-reboot dinilai by-design tanpa patch (sekali-lolos wajib pasca-reboot + jalur ber-rahasia/dedup).
- Guard: `git diff --check` bersih tiap commit; cek bare-return method boolean bersih. Verifikasi milik CI.

## Sesi #37 — 2026-10-08 (audit baca-saja #7, tanpa patch)
- User: "cek seluruh kode dan temukan bug". Mode audit baca-saja, tree bersih, tanpa patch app.
- Area disisir baru/ulang: PinGate dual-clock + catatHasil, pisahkanPin/authDangerous, start env (kutipRocket/tokenAdmin/TOCTOU/batalStart), port+dataDir, Updater pin/norm/banding, build-apk.yml, layout ID parity (main+pin OK), strings 147/147 + placeholder, colors 30/30, vektor 0.x, drawable refs, PIN wiring Main/Settings, TgBotReceiver wakelock, AutoUpdate kuota, rahasiaAlarm, HttpsCompat cap, LogExport orphan, healkanStringPrefs, schedule exact + cancel legacy, import 512KB + allowlist, wakeLock 12 jam, downloadStatus volatile.
- Hasil: tanpa Kritikal/Tinggi/Sedang. 3 Rendah baru (dilapor, belum diperbaiki): (1) ServerService ACTION_RESTART Handler MainLooper tanpa guard (pola clipboard #35, praktis tak terpicu di perangkat); (2) TgBot.refreshMenuAsync getApplicationContext tanpa guard null; (3) indentasi terapkanImporJson menyesatkan (kosmetik).

## Sesi #38 — 2026-10-08 (fix 3 rendah audit #37, selesai)
- User: "perbaiki semuanya". 3 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `e393714 fix:` restart Telegram guard Looper null + fallback panggil start langsung (thread-safe).
  - `e08b8de fix:` refreshMenuAsync guard ctx null + applicationContext null.
  - `a8f4882 chore:` indentasi isi try terapkanImporJson (+4 spasi, balance kurawal 0).
- Guard `git diff --check` bersih. Tanpa CHANGELOG (minor rendah). Verifikasi milik CI.

## Sesi #39 — 2026-10-08 (audit baca-saja #8, tanpa patch)
- User: "cek seluruh kode dan temukan bug". Mode audit baca-saja, tree bersih, tanpa patch app.
- Area disisir: alur perintah bot (/restore konfirmasi+lock, /ca//cabackup//status//log PIN-gate, /versi//alive tanpa PIN), pecahPesan 4000 + antrean prioritas, TUGAS_BERAT + pool BG.ParseResult, swap web-vault staging unik, buffer log 300KB, README trio sinkron, /ca-vs-docs, doRestore decrypt+lock+cleanup, batas unduh 20MB.
- Hasil: tanpa Kritikal/Tinggi/Sedang. 1 Rendah baru (docs): README trio (EN/ID/RU) menyebut /ca cukup auth chat, padahal kode mewajibkan PIN saat PIN aktif (/ca + /cabackup tak disebut di kalimat PIN). Belum diperbaiki.

## Sesi #40 — 2026-10-08 (fix docs audit #39, selesai)
- User: "perbaiki semuanya". 1 commit docs + push (CI dilewati, docs-only):
  - `docs:` /ca + /cabackup masuk kelompok wajib PIN di README.md/id/ru (selaras kode).
- Verifikasi: diff sebaris per bahasa, `git diff --check` bersih.

## Sesi #41 — 2026-10-08 07:20 UTC (audit baca-saja #9, tanpa patch)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug". Mode audit baca-saja (SOUL: cek=kumpulkan temuan, jangan ubah kode). Tanpa build lokal (Aturan No.1), tree bersih, tanpa push app.
- Area disisir: Util/redirect/normalisasiHost, ServerService dataDirAman/kutipRocket/tokenAdmin/stopAndWait/RESTART_TIMES/logBuffer sync, Updater URL/normalisasiPinVersi, TgBot pisahkanPin/authDangerous/doRestore/TUGAS_BERAT, TgBackup restore allowlist+kanonis/bacaResponsBatas/downloadLastBackup, PinCrypto verify caps/isEqual, PinGate grace/lockout, Settings PIN min-4 atomic, LogActivity samarkanLog/clipboard, FileShareProvider TOCTOU, TlsCert, HttpsCompat cap, Boot/Alarm/TgBotReceiver wakelock+throttle, manifest.
- Temuan baru (dilapor, belum diperbaiki): 1 Sedang (refreshLog 1-dtk samarkanLog 14-regex di UI thread atas 300KB → jank/ANR STB) + 1 Rendah (timer clipboard basi hapus salinan baru lebih awal). Bersih: RESTART_TIMES/logBuffer sync, doRestore kunci, PIN atomic, verify caps, allowlist+kanonis restore, redirect fail-closed, wakelock finally.

## Sesi #42 — 2026-10-08 07:35 UTC (fix 2 temuan audit #41, selesai)
- User: "perbaiki semuanya". 1 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `45da597 fix:` LogActivity: refresh tampil ekor 100KB (BATAS_TAMPIL_LOG + potongEkorBaris, di bawah cap sorot 150KB; salin/bagi/simpan tetap buffer penuh) + timer clipboard bawa sidik tangkapan (bersihkanBilaIsiKita banding isi vs sidik timer, bukan prefs terkini) + 3 uji potongEkorBaris.
- Guard `git diff --check` bersih. Verifikasi milik CI (build-apk ringan).
- Pelajaran: timer yang menjadwalkan aksi atas "isi saat ini" wajib membawa identitas yang ditangkap saat jadwal (bukan baca ulang saat eksekusi), kalau tidak timer basi membunuh data baru.

## Sesi #43 — 2026-10-08 07:50 UTC (audit baca-saja #10, tanpa patch)
- User: "cek seluruh kode dari seluruh area lebih agresif temukan bug". Mode audit baca-saja, tree bersih, tanpa patch app.
- Area disisir: self-review patch #42, Settings import allowlist/terapkanImporJson/tanyaPasswordImpor/sapuSisaImpor, TgBackup crypto stream/VWB1-VWB2/deriveKey-100k, export sweep mtime+cap, Updater resume/SHA/buangParsialRusak, ServerService ensureBinary/detectBinaryVersion-watchdog/health-pingRinci, PinActivity, AutoUpdate tanpaKuota/notif, LogExport MediaStore+legacy TOCTOU, Main susulan START_TERTUNDA, Boot/AlarmReceiver, HttpsCompat union-trust, KernelCompat, grace PIN, vektor 0.x, workflow APK.
- Temuan baru: 1 Rendah (residu kosmetik patch #42: logCount hitung buffer penuh sedang tampil ekor; potongEkorBaris fallback tengah-baris bila newline tepat di batas — keduanya kosmetik langka).
- Bersih: import allowlist+keep-rahasia, crypto stream tanpa OOM, sweep sisa kill, resume+SHA fail-closed, watchdog 10dtk+cap 50 baris, health TCP-lolos anti-bunuh-sia-sia, susulan flag hapus-tepat (retry hingga observed-running), trust union bukan ganti, pesan basi 5mnt+offset maju.
- Alur START_TERTUNDA sempat dicurigai flag tak terhapus, ternyata benar: retry tiap buka hingga server observed-running lalu dibuang (by-design, idempoten).

## Sesi #44 — 2026-10-08 08:05 UTC (fix residu audit #43, selesai)
- User: "perbaiki semuanya". 1 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `ed5c0b7 fix:` label baris dihitung dari teks tampil (ekor) agar cocok layar; lastLogLen tetap panjang penuh untuk deteksi trim. potongEkorBaris sadar-newline-ujung (tak ada ekor kosong/tengah-baris; tetap terbatas maks) + 1 uji baru (3 kasus); 3 uji lama tetap lolos (simulasi manual).
- Guard `git diff --check` bersih. Verifikasi milik CI (build-apk ringan).

## Sesi #45 — 2026-10-08 08:15 UTC (audit baca-saja #11, tanpa patch)
- User: "cek seluruh kode temukan kode yang rusak". Mode audit baca-saja, tree bersih, tanpa patch app.
- Area disisir: switch perintah bot (break+default lengkap), `==` string (nihil), killProcess (uid+cmdline+verifikasi-ulang), format-string vs argumen (cocok semua, 2 bahasa), referensi test→main (7 nama dicek langsung, semua ada — false-positive regex), kelas manifest (9/9 ada), R.id Pin/Log (15/15 ada), vektor 0.x (nihil), private mati (semua hidup via method-ref kecuali wizard), refresh Main (keyed + murah), webVaultFromVersion (prefs, murah).
- Temuan baru: 1 Rendah (kode mati: subtree wizard SettingsActivity maybeShowWizard/tampilWizardGabungan/inputWizard/wizardSelesai + string wiz_* tak pernah dipanggil — sengaja dipensiunkan per komentar; hanya perluWizard dipakai test). Bukan perilaku rusak; saran biarkan/hapus di sesi khusus.
- Info: 2 TODO lama TlsCert (regen saat jam pulih) masih by-design (dipakai sementara + logged).

## Sesi #46 — 2026-10-08 08:30 UTC (hapus wizard mati audit #45, selesai)
- User: "perbaiki semuanya". 1 commit + 1x push ke `main` (tanpa build lokal / tanpa pantau CI):
  - `ecbc00d chore:` hapus 82 baris (maybeShowWizard/tampilWizardGabungan/inputWizard/wizardSelesai) + 5 string wiz_* di 2 bahasa (142/142 sinkron). Sengaja dipertahankan: perluWizard (dipakai unit test), KEY_WIZARD_DONE + tulisnya (preferensi lama tetap terbaca), validator galat* (dipakai form + test).
- Guard `git diff --check` bersih; tanpa referensi sisa (rg nihil). Verifikasi milik CI.
- Pelajaran: guard hapus-kode wajib cek definisi (bukan sekadar nama) — pemanggil validator hidup di dalam kode mati sempat memicu false-positive guard lalu diperketat.
