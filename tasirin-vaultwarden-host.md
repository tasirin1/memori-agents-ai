# Memori Sesi — Tasirin Vaultwarden Host

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-vaultwarden-host` — host Vaultwarden Android (minSdk 21, targetSdk 28).
- Aturan main (ringkas dari `AGENTS.md`): DILARANG KERAS build/test/lint lokal dalam bentuk apa pun; verifikasi lokal hanya baca kode, `grep`/`rg`, `git diff`/`log`, parse XML; satu-satunya build/test/rilis via push ke `main` + GitHub Actions; semua Bahasa Indonesia; commit `feat:`/`fix:`/`docs:`/`chore:`/`perf:`; tiap selesai perbaikan langsung commit + push.

## Status terakhir (2026-10-24 = sesi #77) — audit menyeluruh baca-saja (belum ada perubahan kode)

- Permintaan owner: "cek seluruh area secara menyeluruh pelan-pelan teliti, temukan bug, kode tidak efisien, kode sampah, kode tidak rapi". Mode audit baca-saja (SOUL.md): tidak ada berkas aplikasi diubah, tidak ada build lokal. HEAD `0bf6b29`, `main` sinkron `origin/main`, working tree bersih.
- Metode: 5 sub-agen per area (ServerService; Updater/AutoUpdate/TLS/kernel; Telegram+backup+receiver; activity UI; Util/PinCrypto/storage/manifest/res/build) + verifikasi mandiri tiap klaim ke baris kode via `rg`/`sed` (aturan #18). Workflow, shim, skrip, dan verifikator diperiksa sendiri.
- Verifikasi lokal: `python3 tools/verifikasi-patch.py --semua` LOLOS (38 berkas), `bash scripts/cek-cepat.sh` exit 0, `git status --short` bersih. Build/test/lint penuh tidak dijalankan.
- Temuan terverifikasi (semua `file:baris` ada di laporan sesi; belum diperbaiki):
  - **Tinggi (4):** (1) `TlsCert.caOk/leafCukup` menerima cert `sisa == -2` (belum valid) sementara `ServerService.startServer` fail-closed pada `certDays == -2` → server mustahil start sampai jam melewati `notBefore` bila jam pernah diset ke depan lalu dibetulkan; (2) restore DB menulis `db.sqlite3` langsung (bukan tmp+rename) di `SettingsActivity:1997/2047` dan `TgBackup:2834` → kill di tengah = DB rusak, rollback hanya jalan bila proses masih hidup; (3) restore hanya percaya `ServerService.process` statis (`isProcessAlive`), proses vaultwarden yatim tak terlihat (pemindai `/proc` hanya dipakai saat Start) → restore bisa menimpa DB yang sedang dipegang proses yatim (status orphan = dugaan); (4) `PinCrypto.sisaKunciMs` mengembalikan selisih wall-clock tanpa batas atas + `PinGate` memakai `max(wall, elapsed)` → 5 PIN salah saat jam maju/1970 lalu jam dibetulkan/mundur = terkunci praktis permanen (pemulihan hanya hapus data app).
  - **Sedang (~11):** fallback marker `Updater:1166-1196` (checksum diambil dari URL fallback saat unduhan dari `assetUrl`); `Util.jalankanLama` diabaikan pada `ACTION_RESTART` (`ServerService:987`) dan `ACTION_TG_BACKUP` (`1056`) saat pool penuh (tugas hilang, foreground menggantung, jadwal backup bisa mati); `KUNCI_DATA` dipegang selama unduh 20–35 MB (`1504-1535`); `healthActive` tak dimatikan saat start gagal (tick tiap 2 menit selamanya + notifikasi "Server aktif" basi); binary manual tak menulis `KEY_BIN_PATCH` (salin 20 MB + hash + smoke test tiap Start); `fetchChecksum` 403/429 dianggap "checksum tidak ada" + tmp lengkap kena 416 → unduh ulang penuh; tanda air jam `TgBot` membisukan bot untuk koreksi 5 menit–30 hari; backup DB manual melabeli `SIBUK:` sebagai "Corrupt database"; Start tidak dikunci saat tugas busy (prefs ditulis dari form pra-restore); `configChanges` tanpa `onConfigurationChanged` membuat `layout-land`/dimens land tak terpakai setelah rotasi; `BootReceiver` exported menerima `QUICKBOOT_POWERON` non-protected.
  - **Rendah (~10) + kode mati/duplikasi:** `tailLog` dibaca sebelum `pumpOutput` selesai; crash path lupa `resetPenandaJalan`; `.tmp` nama tetap lintas versi (resume campur byte); `KEY_WV_FROM` tak dicap saat `latest == null` (unduh ulang 35 MB); `LogActivity` gerbang PIN fail-open; `StoragePerm.siapStart` toast "belum diberi" bersamaan dialog izin; koneksi `bukaFileTelegram` bocor + `catch (Throwable)` menelan Error; `KEY_TG_LAST` ditulis walau sebagian chat gagal; wakelock backup/bot terlalu pendek (dugaan runtime); PIN bisa diganti tanpa konfirmasi (ambang 4 karakter) + checkbox desync.
  - **Kode sampah/rapi:** 3 overload mati di `Updater` (`downloadBinaryInner(ctx,out)`, `updateWebVaultInner(ctx)`, `detectVersion(File)`); duplikasi `ServerService.detectBinaryVersion`/`isValidBinary`/`HttpsCompat.capOverride`; import `SecureRandom` mati (pemakaian fully-qualified, lolos `cek_import_mati` — celah gate); parameter `httpsAktif` tak dipakai; cabang `portButuhRoot` tak terjangkau; tombol "Ubah"/ringkasan `visibility=gone` tapi `nextFocusUp/Down` menunjuk ke sana + `secExpanded` write-only; Javadoc ganda + klausa `vwtg-restore` tersubsumsi di `FileShareProvider`; cabang `//host` redundan di `Util`; komentar manifest salah (QUICKBOOT protected) + `MANAGE_EXTERNAL_STORAGE` tak pernah diminta; `about_rows` tanpa `values-in`; `build-binary.yml` hardcode repo `tasirin1/...`.
- Klaim "Activity ditahan worker panjang" tidak dilaporkan ulang: sudah diverifikasi dan ditolak pada sesi #76 (lambda memang menangkap `this` lewat helper; ganti ke app context tak melepasnya).
- Tindak lanjut: menunggu perintah owner untuk mulai maraton perbaikan (aturan #17), prioritas Tinggi dulu. Belum ada push kode aplikasi pada sesi ini.

## Status sebelumnya (2026-10-23 = sesi #76) — maraton perbaikan audit (6 Tinggi + 6 Sedang/Rendah)

- Permintaan owner: "mau" — mulai maraton perbaikan temuan audit (aturan #13/#17): satu temuan satu perbaikan akar, langsung commit + push `main`, tanpa memantau build (aturan #14). HEAD akhir `0bf6b29`, `main` sinkron `origin/main`, working tree bersih.
- Audit awal sesi (5 sub-agen + verifikasi mandiri) melaporkan 6 Tinggi / 22 Sedang / ~18 Rendah; tidak ada Kritikal. Sesi ini menutup 6 Tinggi + 6 temuan lanjutan:
  - `1845c3e` (Tinggi): `ServerService.watchProcess` cabang stop-disengaja kini membersihkan SEMUA state (`process`, `running`, penanda, wakelock, flush log, status "Stopped"); dulu watcher menang balapan → `running=true` menggantung.
  - `e845bb4` (Tinggi): restart karena IP LAN berubah memakai `restart()`/`ACTION_RESTART` (hentikan proses lalu start), bukan `scheduleRestart()` yang no-op saat proses hidup; `runningLanHost` langsung diperbarui agar tick berikut tak memicu restart kedua.
  - `b8ac6ea` (Tinggi): zip backup yang memuat `tls/ca-key.pem`+`tls/key.pem` dibangun di cache privat app saat akan dienkripsi (dulu plaintext sempat di `/sdcard/.../backups`, dan tertinggal bila enkripsi gagal); `.enc` tetap di folder backups + retensi.
  - `101a8e9` (Tinggi): `SettingsActivity.refreshRingkasan` mem-posting dirinya ke UI thread bila dipanggil dari worker (dua `catch` di `runBusy` dulu menyentuh View dari worker → `CalledFromWrongThreadException`).
  - `b368db0` (Tinggi): lockout PIN berlaku saat jam masih 1970 — stempel kecil tak lagi dianggap sisa era elapsed (dulu 5 PIN salah tidak dikunci); test `PinCryptoTest.kunciJam1970TetapMengunci`.
  - `d2f3d0d` (Tinggi): `TgBot.httpPostForm` mencatat ringkasan galat Telegram (401/409/429 + kelas exception) sekali per jenis; `ringkasGalatTelegram` murni (tanpa `org.json`) hanya mengambil `error_code`+`description` agar token di URL tak bocor ke log.
  - `d7243b9`: tanda air jam Telegram tak bisa "diracuni" lompatan ke masa depan (dulu bot bisu sampai tahun itu tiba); `wallBolehMaju` + pembersihan nilai racun di `muatWallMaks`/`pollOnce`; test `wallBolehMaju_tolakJam1970DanLompatanRaksasa`.
  - `9742599`: Start saat restore memegang `KUNCI_DATA` diulang tiap 5 dtk (maks 60x) lewat `restartTunda`, bukan hilang diam-diam; Stop tetap membatalkan.
  - `37e02c5`: `.enc` yang gagal round-trip dihapus di `finally` (dulu menumpuk & mengusir backup sah lewat retensi).
  - `f73d386`: retensi backup hanya jalan setelah zip lolos verifikasi (dulu backup korup tetap mengusir backup lama).
  - `59f0602`: `maybeAutoBackup` melewati cepat bila `tugasDataJalan()` (dulu menunggu DB 30 dtk lalu pesan "gagal + saran koneksi" menyesatkan & menahan 1 slot `BG_LAMA`).
  - `0bf6b29`: `KEY_START_TERTUNDA` dihapus begitu `ServerService.start()` diterima (dulu menunggu `running` yang asinkron → flag awet → server menyala sendiri tiap app dibuka setelah Stop). `b431e80`: sidik menu bot memakai `responsOk` (toleran spasi).
- Klaim sub-agen yang SAYA TOLAK setelah verifikasi: (a) "Activity context ditahan worker panjang" — lambda `runBusy` sudah menangkap `this` lewat `appendUiLog`/`toast`, jadi mengganti argumen ke `getApplicationContext()` tidak melepas Activity; (b) "admin token <8 hanya di Settings" — sudah ditutup sesi #73 (`inputStartValid` + cek defensif `saveAndStart`).
- Verifikasi lokal tiap commit: `python3 tools/verifikasi-patch.py` LOLOS, `bash scripts/cek-cepat.sh` exit 0, `git diff --check` bersih. Build/test/lint penuh hanya di CI dan tidak dipantau.
- Sisa terbuka: temuan Sedang/Rendah lain dari laporan audit sesi ini (yang belum tersentuh) + refactor i18n teks Inggris hardcode (bukan bug).

## Status sebelumnya (2026-10-23 = sesi #75)

- Sesi #75: menutup peringatan gerbang Verifikasi Patch pada sesi #74. HEAD app `9abad46` (`test: uji editMessageKb abaikan masukan tak sah`), `main` sinkron `origin/main`, working tree bersih.
- Akar: `TgBackup.editMessageKb()` (statis baru, glue Android) belum disebut di `app/src/test`, jadi `cek_uji_baru` memberi peringatan "metode statis baru tanpa jejak di app/src/test". Peringatan hanya muncul pada cek berbasis diff push, bukan `--semua`.
- Perbaikan: tes JVM `editMessageKb_abaikanMasukanTakSah` memanggil `editMessageKb(null, ...)` dan ID 0 — membuktikan guard fail-safe (Context hilang / ID tak sah tidak melempar ke pemanggil bot). Tanpa perubahan kode produksi.
- Verifikasi lokal: `verifikasi-patch --rentang HEAD~1...HEAD` LOLOS tanpa peringatan, `cek-cepat.sh` exit 0, `git diff --check` bersih. Build/test penuh di CI, tidak dipantau (aturan #14).

## Status sebelumnya (2026-10-23 = sesi #74)

- Sesi #74: kontrol Telegram jadi menu tombol berjenjang (mirip Red-Eye). HEAD app `f651695`, `main` sinkron `origin/main`, working tree bersih.
- `TgBot`: `/help` membuka panel tombol (Status, Kontrol, Backup, Update, Sertifikat, Info) dengan callback navigasi `m:<panel>` + tombol Kembali; panel diedit di tempat (`TgBackup.editMessageKb` → `editMessageText`, fallback kirim baru). Keyboard lama (callback `/perintah`) tetap jalan.
- Tombol ber-PIN meminta PIN lewat balasan chat 5 menit (`KEY_TG_PENDING_PREFIX` per chat, `pendingMasihBerlaku` fail-closed saat jam mundur, sesi dihapus sebelum eksekusi). Grup tak pernah membuat sesi PIN. `/ca`+`/cabackup` masuk `perintahPerluPin` (hapus pesan ber-PIN + prompt tombol).
- `keyboardPerintah` + 2 tes lamanya dihapus dan dicatat di `tools/bekas-hapusan.txt`; tes baru `rakitKeyboard`, `panelMenuValid`, `keyboardMenu`, `perintahPerluPin`, `pendingMasihBerlaku`, `bangunParamEdit`. README EN/ID/RU + CHANGELOG diperbarui.
- Verifikasi lokal: `verifikasi-patch --semua` LOLOS (38 berkas; 1 peringatan non-fatal `editMessageKb` tanpa tes JVM karena butuh Context), `cek-cepat.sh` 0, `git diff --check` bersih. Build/test penuh di CI, tidak dipantau (aturan #14).

## Status sebelumnya (2026-10-23 06:31 UTC = sesi #73)

- Sesi #73: maraton perbaikan temuan audit sampai daftar konkret habis (aturan #17). HEAD app `e1ff2cd`, `main` sinkron `origin/main`, working tree bersih.
- Perbaikan keamanan/stabilitas (semua sudah commit + push `main`): PIN pendek tak mematikan proteksi, snapshot password backup, hapus WAL/SHM per berkas, urutan penanda stop, `stopSelf(startId)`, kunci data Start vs restore, pool tugas paralel, validasi tag upstream, symlink kanonis, hash ulang di dalam kunci unduh, semua baris `--version`, `stopAndWait` menunggu `starting`, fallback binary 6 jam, validasi admin token + setelan tersimpan saat `onPause`, guard lifecycle dialog, reset TLS serial dengan Start, PIN bot hanya dari chat pribadi (deteksi per chat, bukan seluruh config), cek ruang sebelum restore.
- CI: workflow APK tanpa job `perlu`/`assembleDebug`, `cancel-in-progress` dimatikan, unggah `--clobber` + verifikasi ukuran; gate `cek-cepat` memeriksa staged + tracked (tak buta di runner); `.gitignore` aset CI; verifikator melewati `build/` dan mengabaikan komentar/Javadoc; `cacert.pem` dipin SHA-256; `restore-keys` cache cargo diperbaiki.
- Commit penting: `b7aa881` (#18/#19), `3c8f9f9` (#20), `1fc7b55` (#21), `7b2033e` (#22), `1683e59` (#23), `9edcbaf` (#24/#25), `14332fb` (#26), `a73fbae` (#21 lanjutan: deteksi grup per chat), `e1ff2cd` (judul dialog restore). Rentang #1–#17 ada di `git log` sejak `8d731c0`.
- Verifikasi lokal: `verifikasi-patch --semua` LOLOS (38 berkas), `cek-cepat.sh` exit 0, `git diff --check` bersih. Build/test penuh di CI, tidak dipantau (aturan #14).
- Catatan: pin SHA-256 `cacert.pem` sengaja menggagalkan build bila curl.se merilis bundel baru — perbarui hash setelah memeriksa perubahan. Grup Telegram kini hanya menerima notifikasi/backup + perintah tanpa PIN; PIN-gated commands wajib dari chat pribadi (README EN/ID/RU sudah diperbarui).

## Tugas terbuka

- Temuan audit sesi #77 (4 Tinggi / ~11 Sedang / ~10 Rendah + kode mati) belum diperbaiki — mulai dari Tinggi sesuai aturan #17 bila owner menyuruh "perbaiki/lanjutkan".
- Refactor sisa teks UI berbahasa Inggris yang masih hardcode di `SettingsActivity`/`MainActivity`/`LogActivity` jadi resource (butuh harness pembuktian setara sesuai `SOUL.md`; bukan bug, murni i18n). Belum dikerjakan karena risiko/churn besar tanpa compile lokal.
- `build-binary.yml` masih memakai helper unggah aset inline (satu-satunya; workflow APK sudah `--clobber`). Tidak dijadikan skrip bersama agar tak menambah run binary berat tanpa perlu.

## Cara pakai file ini

- Awal sesi: baca file ini, lalu `git status --short` + `git log --oneline -5`.
- Akhir sesi: update tanggal, status terakhir, dan tugas terbuka.

> Memori aktif. Arsip lama: `archive/tasirin-vaultwarden-host-arsip.md` (Sesi #1–#66).

## Sesi #67 — 2026-10-13 07:18 UTC (audit ulang seluruh area, selesai)
- Permintaan: sapu semua area dan buang kode tak efisien/sampah/bug Android 5+. Repo aplikasi bersih di awal (`main`, HEAD `083df6e`).
- Audit baca-saja 21 Java (24.288 baris), manifest, seluruh resource, 3 workflow, shim C, skrip, dan verifikator. Cek pola API Android, lifecycle callback, jaringan, logging, dan regresi temuan audit-64/65/TLS.
- `python3 tools/verifikasi-patch.py --semua` LOLOS (38 berkas); `bash scripts/cek-cepat.sh` LOLOS; `git diff --check` bersih. Tidak menjalankan build/test/lint lokal.
- Tidak ditemukan masalah baru yang bisa dibuktikan aman untuk dihapus atau diperbaiki; tidak ada perubahan/commit aplikasi. Temuan spekulatif ditahan karena butuh runtime/CI untuk membuktikannya.
- Status: audit selesai, repo aplikasi tetap bersih, belum ada tugas terbuka.


## Sesi #68 — 2026-10-13 07:21 UTC (audit fokus Android 8+, selesai)
- Permintaan: audit seluruh area, fokus bug/performa/stabilitas Android 8+. Repo aplikasi bersih di awal; HEAD `083df6e`.
- Telusur 21 Java, manifest, seluruh resource, workflow, shim, dan skrip. Fokus API Oreo+: startForegroundService/startForeground, channel, status foreground untuk semua action service, jalur start dari AlarmReceiver/BootReceiver/bot/activity, exact alarm, callback lifecycle, serta guard API lintas versi.
- Jalur service konsisten: helper start memakai startForegroundService pada O+, tiap action yang sah mengaktifkan foreground sebelum kerja latar, notification channel dibuat sebelum notifikasi, alarm menangani izin exact dan fallback. Tidak ditemukan bug Android 8+ baru yang dapat dibuktikan.
- `python3 tools/verifikasi-patch.py --semua` LOLOS (38 berkas); `bash scripts/cek-cepat.sh` LOLOS; `git diff --check` bersih. Build/test/lint Android lokal tidak dijalankan.
- Tidak ada perubahan kode aplikasi atau push app; audit selesai tanpa temuan.


## Sesi #69 — 2026-10-13 07:24 UTC (audit fokus Android 10+, selesai)
- Permintaan: audit seluruh area untuk stabilitas/kinerja Android 10+. Repo aplikasi bersih; HEAD `083df6e`.
- Telusur source Java, manifest, resource, workflow, shim, skrip, khususnya targetSdk, eksekusi binary, penyimpanan eksternal, MediaStore, dan service/alarm lintas versi. Dokumentasi Android Developers resmi dicek untuk W^X API 29+ dan scoped storage.
- Binary dipasang di internal app storage; targetSdk tetap 28 karena kebutuhan execve; akses eksternal default masih memakai model legacy target 28, permission sesuai, dan log ekspor memakai MediaStore mulai API 29. Tidak ditemukan bug Android 10+ baru yang dapat dibuktikan.
- `python3 tools/verifikasi-patch.py --semua` LOLOS (38 berkas); `bash scripts/cek-cepat.sh` LOLOS; `git diff --check` bersih. Build/test/lint Android lokal tidak dijalankan.
- Tidak ada perubahan kode aplikasi atau push app; audit selesai tanpa temuan.


## Sesi #70 — 2026-10-13 07:26 UTC (audit fokus Android 14+, selesai)
- Permintaan: audit semua area untuk Android 14+. Repo bersih; HEAD `083df6e`.
- Audit source Java, manifest/resource, workflow, shim dan skrip; telusur perubahan API 34: foreground service type/permission, dynamic receiver export, DCL read-only, exact alarm, notification, implicit intent, ZIP path, OpenJDK behavior. Dokumentasi resmi Android Developers dipakai untuk memilah perubahan target 34 vs semua aplikasi.
- Target app tetap 28; service mendeklarasikan dataSync + permission, alarm memeriksa canScheduleExactAlarms dan fallback, tidak ada registerReceiver dinamis, ZIP extract punya validasi jalur, komponen manifest exported terdefinisi. Tidak ditemukan regresi Android 14+ baru yang terbukti.
- `python3 tools/verifikasi-patch.py --semua` LOLOS (38 berkas); `bash scripts/cek-cepat.sh` LOLOS; `git diff --check` bersih. Build/test/lint Android lokal tidak dijalankan.
- Tidak ada perubahan kode aplikasi atau push app; audit selesai tanpa temuan.

## Sesi lanjutan (2026-10-15 03:20 UTC) — selesai
- Permintaan: terapkan penyederhanaan workflow ke semua proyek kelolaan.
- Perubahan: `verifikasi-patch.yml` digabung jadi job pertama di `build-apk.yml` DAN `build-binary.yml` (`needs` + delete berkas); daftar struktur di AGENTS.md diselaraskan. Tanpa bump versi/tag (versionCode epoch-otomatis, preseden chore langsung push).
- Validasi: YAML valid kedua berkas, `tools/verifikasi-patch.py` LOLOS, `scripts/cek-cepat.sh` exit 0, `git diff --check` bersih.
- Commit `a2f3b35`, push `origin main` sukses.

## Sesi #71 — 2026-10-17 12:31 UTC (aturan maraton + sub-agen ditulis ke AGENTS.md, selesai)
- Permintaan owner: "terapkan aturan maraton perbaikan dan subagest ini ke semua repo yang di kelola memori ai".
- Perubahan (`744ffd0`, push `origin main`, docs-only tanpa bump/tag): `AGENTS.md` +aturan 17 (**mode perbaiki = maraton** — kerjakan temuan audit sampai habis, satu temuan satu perbaikan akar, langsung commit + push `main` per aturan #13, tanpa memantau build per #14, build gagal didahulukan) +aturan 18 (**audit menyeluruh = 2–5 sub-agen paralel per area + verifikasi mandiri** tiap klaim berat ke kode `rg`/`sed` sebelum masuk laporan/patch; temuan wajib `file:baris` + dampak + skenario pemicu + level bahaya).
- Kanonik lintas repo: `SOUL.md` (memori agen) seksi "Aturan maraton perbaikan & sub-agen"; salinan di `AGENTS.md` Red-Eye-Mobile §5, netradar 14–15, tasirin-download-manager 21–22.
- Validasi tanpa toolchain Android: `python3 tools/verifikasi-patch.py` LOLOS (1 berkas), `bash scripts/cek-cepat.sh` exit 0, `git diff --check` bersih.

## Sesi #72 — 2026-10-23 04:29 UTC (maraton perbaikan temuan audit, selesai)
- Permintaan owner: "lanjut" — meneruskan maraton perbaikan temuan audit (aturan 13/17): satu temuan satu perbaikan akar, langsung commit + push, tanpa memantau build (aturan 14).
- Basis awal sesi: HEAD `2078c70`; temuan konkret tersisa: `AutoUpdate` gagal sunyi, throttle smoke test mati, balapan memo versi, kode mati (`extensionsBlock`/`deriveKey`/`TG_INTERVAL_MS`), teks UI PIN hardcode Indonesia, blok destroy ganda, namespace `KEY_WV_FROM`.
- Commit sesi ini: `6c47f9e` (AutoUpdate catat gagal), `34def45` (hapus throttle smoke mati), `2078c70` (memo atomis `MemoVersi` + uji antar-thread), `5ca9e59` (hapus overload/konstanta mati), `3d41b37` (cap web-vault hanya tag Vaultwarden), `2740d7b` (satu pintu pembersihan `detectVersion`), `4599631` (teks PIN → resource).
- Bukti namespace: `versiWvUntukCap` dulu menulis versi web-vault Bitwarden (`vw-version.json`) ke `KEY_WV_FROM` saat `latest == null`, padahal perbandingan "sudah terbaru" memakai tag Vaultwarden — namespace tercampur dan UI menampilkan versi salah. Kini cap hanya tag Vaultwarden; cek `latest == null` tetap memakai keberadaan payload (`wvPayloadAda`) sehingga tidak ada unduhan ulang 35 MB tambahan. Test `capWvHanyaTagVaultwarden` (nama lama `capWvRedirectDariJson` dicatat di `tools/bekas-hapusan.txt`).
- Kode mati: `TlsCert.extensionsBlock(List)` satu-argumen, `TgBackup.deriveKey` 2-/3-argumen, `TgBackup.TG_INTERVAL_MS` dihapus; nama `deriveKey`/`extensionsBlock` TIDAK masuk `bekas-hapusan.txt` karena masih ada overload (pindah, bukan hapus total).
- Verifikasi: `verifikasi-patch.py --semua` LOLOS (38 berkas), `cek-cepat.sh` exit 0, `git diff --check` bersih. Build/test/lint penuh diserahkan ke CI; run tidak dipantau sesuai aturan #14.
- Sisa: hanya refactor i18n teks Inggris hardcode (dibutuhkan harness bukti setara; dicatat sebagai tugas terbuka, bukan bug).

## Sesi #73 — 2026-10-23 06:31 UTC (maraton audit #18–#26 + lanjutan, selesai)
- Permintaan owner: lanjutkan maraton perbaikan temuan audit (aturan #13/#17) — satu temuan satu perbaikan akar, langsung commit + push `main`, tanpa memantau build (aturan #14).
- Basis awal: lanjutan sesi #72 (`4599631`); sesi ini menutup temuan #18–#26 plus dua temuan susulan. HEAD akhir `e1ff2cd`, `main` sinkron `origin/main`, working tree bersih.
- Temuan & akar perbaikan:
  - #18/#19 (`b7aa881`): admin token <8 tak lagi bisa Start (validasi di `inputStartValid` + cek defensif `saveAndStart`); folder/port/token valid disimpan saat `onPause` (bukan hanya saat Start), ditunda bila backup/restore jalan (`TgBackup.tugasDataJalan()` + test). `SettingsActivity` mengabaikan tulis saat `tugasBerjalan`.
  - #20 (`3c8f9f9`): `TgBackup.resetSertifikat` memegang `ServerService.KUNCI_DATA` yang sama dengan Start/restore dan memeriksa ulang status di dalam kunci; `TlsCert.resetTls` mengunci `KUNCI_ENSURE`. Start yang ditunda kini berpesan "restore/reset sedang berjalan".
  - #21 (`1fc7b55`): perintah ber-PIN dari grup/username ditolak (PIN di grup terbaca anggota; `PinGate` bersama bisa dikunci orang lain). Grup tetap menerima notifikasi/backup + perintah tanpa PIN. README EN/ID/RU diperbarui.
  - #22 (`7b2033e`): workflow APK — job `perlu` selalu-yes dihapus, `assembleDebug` mubazir dihapus, `cancel-in-progress:false` agar publish tak terpotong, unggah `gh release upload --clobber` + retry + verifikasi ukuran aset.
  - #23 (`1683e59`): gate `cek-cepat` memeriksa staged + semua tracked (dulu `git diff --cached` kosong di CI), pola `.aab`/`.so`/`.a`/`.dex`/`assets/bin`/`vw_version.txt`/`.env.*`; `.gitignore` aset CI; verifikator melewati `build`/`.gradle`, ABI hanya `abiFilters`, komentar/Javadoc tak dihitung sebagai pemanggil hidup.
  - #24/#25 (`9edcbaf`): `cacert.pem` curl.se dipin SHA-256 `796f1389...e3cbe` sebelum `include_str!`; `restore-keys` cargo diganti prefiks `vw-cargo-armv7-` (dulu tak pernah cocok).
  - #26 (`14332fb`): restore cek ruang sebelum server dihentikan — total isi zip tak terkompresi + salinan pengaman DB + 5 MB; tolak isi > `BATAS_UNZIP_RESTORE` lebih awal. Helper `ukuranIsiZip` + test.
  - #21 lanjutan (`a73fbae`): `authDangerous` menerima ID chat; grup dideteksi per chat (ID negatif), bukan `chatResmiAdalahGrup(ctx)` seluruh config — config campuran (pribadi + grup) tetap bisa memerintah dari chat pribadi. `pengirimId`→`idRuang`.
  - #112 (`e1ff2cd`): judul dialog `"Restore dari Telegram"` → `"Restore from Telegram"` (satu-satunya teks UI Indonesia).
- Klaim audit yang diverifikasi ulang: `Updater.sha256Hex` **dipakai** (3 referensi), tak ada metode privat/field privat tanpa rujukan, dan tak ada overload mati di `Updater` — klaim "dead overloads/sha256Hex" tidak terbukti; tidak ada perubahan kode untuk itu.
- Verifikasi lokal tiap commit: `python3 tools/verifikasi-patch.py` (+ `--semua` LOLOS 38 berkas), `bash scripts/cek-cepat.sh` exit 0, `git diff --check` bersih. Build/test/lint penuh hanya di CI dan tidak dipantau.
- Catatan operasional: push `.github/workflows/build-binary.yml` (Audit 109) memicu build binary berat ~15 menit; pin CA akan sengaja gagal bila curl.se merilis bundel baru (perbarui hash setelah memeriksa). Sisa tugas terbuka tetap refactor i18n teks Inggris hardcode (bukan bug; ditunda karena churn besar tanpa compile lokal).
