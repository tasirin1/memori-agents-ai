# Memori Sesi — Tasirin Vaultwarden Host

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/tasirin-vaultwarden-host` — host Vaultwarden Android (minSdk 21, targetSdk 28).
- Aturan main (ringkas dari `AGENTS.md`): DILARANG KERAS build/test/lint lokal dalam bentuk apa pun; verifikasi lokal hanya baca kode, `grep`/`rg`, `git diff`/`log`, parse XML; satu-satunya build/test/rilis via push ke `main` + GitHub Actions; semua Bahasa Indonesia; commit `feat:`/`fix:`/`docs:`/`chore:`/`perf:`; tiap selesai perbaikan langsung commit + push.

## Status terakhir (2026-10-17 12:31 UTC = sesi #71)

- Sesi #71: aturan maraton perbaikan + audit sub-agen ditulis ke `AGENTS.md` repo ini (aturan 17–18) atas permintaan owner; tetap terikat aturan #13 (langsung push) & #14 (dilarang memantau build). Versi kanonik di `SOUL.md` memori agen.
- Commit docs-only `744ffd0` (push `origin main`, tanpa bump versi/tag — `versionCode` epoch-otomatis, commit `*.md` dilewati CI).
- Guard: `python3 tools/verifikasi-patch.py` LOLOS (1 berkas) + `bash scripts/cek-cepat.sh` exit 0 + `git diff --check` bersih.
- Sebelumnya (sesi #70 + lanjutan, 2026-10-15 03:20 UTC): workflow `verifikasi-patch.yml` digabung jadi job pertama `build-apk.yml` + `build-binary.yml` (`a2f3b35`).

## Tugas terbuka

- (belum ada)

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
