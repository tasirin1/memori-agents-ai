# Memori Sesi — Tasirin Vaultwarden Host

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-vaultwarden-host` — host Vaultwarden Android (minSdk 21, targetSdk 28).
- Aturan main (ringkas dari `AGENTS.md`): DILARANG KERAS build/test/lint lokal dalam bentuk apa pun; verifikasi lokal hanya baca kode, `grep`/`rg`, `git diff`/`log`, parse XML; satu-satunya build/test/rilis via push ke `main` + GitHub Actions; semua Bahasa Indonesia; commit `feat:`/`fix:`/`docs:`/`chore:`/`perf:`; tiap selesai perbaikan langsung commit + push.

## Status terakhir (2026-10-23 04:29 UTC = sesi #72)

- Sesi #72: maraton perbaikan temuan audit (lanjutan) sampai daftar temuan konkret habis. HEAD app `4599631`, `main` sinkron `origin/main`, working tree bersih.
- Fix utama (semua sudah commit + push `main`, build tidak dipantau sesuai aturan #14): anti-loop restart, rollback restore via `TgBackup.pulihkanDbLama`, serialisasi backup via `TgBackup.kunciBackup`, lifecycle dialog web-vault, web-vault "false latest" (`wvPayloadAda`), START_STICKY via `server_diminta`, penolakan antrean pool melempar `RejectedExecutionException` + helper boolean melepas flag, retry checksum (408/429/5xx), `clearLog` menghapus `logFileBuf` + `.log.1`, auto-backup hanya setelah Start diterima, izin storage legacy Android 11+, target terkunci tak memanggil `latestVersion()`, sinkron checkbox PIN.
- Guard/verifikator: `tools/verifikasi-patch.py` menormalkan rentang di dispatch/schedule/push pertama (`rentang_normal`).
- Kebersihan: `AutoUpdate.cek` mencatat kegagalan (tak telan sunyi), throttle smoke test mati dihapus, memo versi binary atomis (`MemoVersi`), overload/konstanta mati `TgBackup`/`TlsCert` dihapus, cap versi web-vault hanya tag Vaultwarden (bukan versi Bitwarden dari `vw-version.json`), `Updater.detectVersion` satu pintu pembersihan proses (finally), teks UI PIN Indonesia hardcode jadi `R.string.pin_proses_gagal`.
- Verifikasi lokal: `python3 tools/verifikasi-patch.py --semua` LOLOS (38 berkas), `bash scripts/cek-cepat.sh` exit 0, `git diff --check` bersih. Status CI tidak dipantau (aturan #14).
- Sebelumnya (sesi #71, 2026-10-17 12:31 UTC): aturan maraton + sub-agen ditulis ke `AGENTS.md` (`744ffd0`).

## Tugas terbuka

- Refactor sisa teks UI berbahasa Inggris yang masih hardcode di `SettingsActivity`/`MainActivity`/`LogActivity` jadi resource (butuh harness pembuktian setara sesuai `SOUL.md`; bukan bug, murni i18n). Tidak dikerjakan pada sesi #72 karena risiko/churn besar tanpa compile lokal.

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
