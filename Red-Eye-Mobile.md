# Memori Sesi — Red Eye Mobile

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/Red-Eye-Mobile` — aplikasi Android (build SELALU di GitHub Actions; lokal hanya edit + cek sintaks ringan + validasi XML).
- Aturan main (ringkas dari `AGENTS.md`): jangan install SDK lokal; jangan commit secret (bot token/chat ID); changelog Keep a Changelog untuk perubahan perilaku/build/workflow; rilis via bump `versionCode`/`versionName` + tag `vX.Y.Z`.

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
