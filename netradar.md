# Memori Sesi — NetRadar

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Konvensi waktu (wajib —(generator kebingungan 2026-10-03)

Semua sesi repo ini pernah terjadi dalam SATU hari (2026-10-03, 11:00–13:35 UTC),
tapi dulu dilabeli "pagi/sore/malam/kemarin" sehingga agen mengira aksi
barusan adalah aksi kemarin. Aturan perbaikan:

- Setiap entri memakai stempel absolut `YYYY-MM-DD HH:MM UTC` (zona UTC; ambil
  via `date -u`, JANGAN pakai jam lokal mesin).
- DILARANG kata waktu relatif tanpa stempel absolut: kemarin, tadi, barusan,
  pagi/sore/malam, "sesi sebelumnya", "yang baru saja".
- Sesi diberi nomor urut (#1, #2, …); tiap sesi berstatus jelas
  (`selesai` / `dilanjutkan sesi #N`). Entri lama yang statusnya berubah
  (mis. "belum push" lalu sudah push) wajib ditandai, jangan dibiarkan menggantung.
- "Status terakhir" selalu = ringkasan sesi bernomor tertinggi.

## Proyek

- Repo: `tasirin1/netradar` — radar jaringan Android, Jetpack Compose (minSdk 29, targetSdk 36).
- Aturan main (ringkas dari `AGENTS.md`): build resmi HANYA via CI; semua Bahasa Indonesia; commit `type: deskripsi` (`feat`/`fix`/`refactor`/`test`/`perf`/`docs`); `versionName` tetap `"2.0"`, `versionCode` otomatis; guard changelog di CI (perubahan `app/src`, `scripts/`, `.github/workflows/`, `app/build.gradle.kts` wajib sertakan `CHANGELOG.md`); unit test logika murni tanpa Robolectric.
- Workflow Build docs-only skip (`**.md`, `LICENSE`, `.gitignore`) — selaras repo Tasirin lain.

## Status terakhir (2026-10-03 13:35 UTC = sesi #7)

- HEAD master `bc81098`; working tree bersih; CI Build berjalan pasca-push.
- Memori ini baru ditulis ulang dengan stempel absolut (sesi #7).

## Tugas terbuka

- (belum ada)

## Cara pakai file ini

- Awal sesi: baca file ini, lalu `git status --short` + `git log --oneline -5`.
- Akhir sesi: tambah sesi bernomor baru + update "Status terakhir", commit + push.

## Riwayat sesi

### Sesi #1 — 2026-10-03 ~11:00–12:10 UTC — selesai (dilanjutkan sesi #2)
- Audit statis + perbaiki 15 temuan: race ScannerManager (jobLock), DNS di main
  thread ke IO, Semaphore blokir → `kotlinx.coroutines.sync` (4 scanner + baru di
  UdpScanner), retry double-count + cap 2000 + clamp checkpoint, RTSP 25 baris,
  mergeHost otoritatif, uptime/ping append + throttle 10 dtk, cap CustomPortParser
  1000, tolak IPv6, IP penuh → sisa /24, PingUtil waitFor + PingSweep timeout,
  traceroute IPv6 + selesai longgar.
- Test: NetworkUtilsTest + CustomPortParserTest; CHANGELOG + README diperbarui.
- Status akhir sesi: perubahan di working tree, BELUM push (didorong di sesi #2).

### Sesi #2 — 2026-10-03 12:11–12:20 UTC — selesai
- Push master 6 commit; Build `37122297630` success 13 step
  (guard changelog, keystore, test, lint, R8, apksigner, VirusTotal, artifact,
  cek 5MB); Release `v2.0` terbit. Sempat gagal 1× (return eksplisit probe
  kamera/router) + 1× guard changelog — diatasi via commit susulan + ScanLoopTest.
- Onboarding mesin ini: clone + pointer `MEMORY.md` + docs-only skip CI.

### Sesi #3 — 2026-10-03 ~12:30–12:54 UTC — selesai (dilanjutkan sesi #4)
- Audit statis read-only ~8.300 baris, tanpa ubah file: 11 temuan
  (PING/TRACE hapus port; traceroute gantung; rescan hilangkan osGuess;
  RTSP 25 baris; timestamp favorit global; diff antar-mode; deep scan abaikan
  pause; onCleared di main thread; ID notif tabrakan; label hidup lagi;
  regex traceroute + UDP multicast + await berurutan).

### Sesi #4 — 2026-10-03 ~13:00–13:15 UTC — selesai
- Perbaiki 11 temuan sesi #3, commit `657eb63` (8 file, +99/-34), push master:
  waris port PING/TRACE, label pengguna, rescan osGuess+lastSeenScan, alert
  per-IP, onCleared di IO, scanHost isi osGuess, deepScan cek pause, banner stop
  di baris kosong, traceroute timeout 5 dtk + regex longgar, progres urutan
  selesai via Channel, blank-break kamera, skip UDP 1900/5353, stableId,
  CHANGELOG [Unreleased].

### Sesi #5 — 2026-10-03 ~13:15–13:23 UTC — selesai (dilanjutkan sesi #6)
- Audit ulang read-only pasca-`657eb63` (area belum tersentuh: RouterScanner,
  CIDR, SSDP, gateway/monitor, backup, widget, manifest, UI): 10 temuan
  (SSDP mati total via `pkt.port`; Router lolos blank-break; TCP ke 161/1900;
  CIDR invalid jadi /24; widget hitung unknown online; tanpa negative caching;
  checkInternet tiap 5 dtk; label panel router generik; checkpoint abadi;
  lastPtr lintas section). Perbaikan sesi #4 terverifikasi utuh.

### Sesi #6 — 2026-10-03 ~13:23–13:26 UTC — selesai
- Perbaiki 10 temuan sesi #5, commit `bc81098` (9 file, +90/-24), push master:
  SSDP dari isi paket + negative caching + reset lastPtr; Router blank-break +
  buang TCP 161/1900 + filter host mirip router; Discover buang TCP 161/1900;
  CIDR invalid ditolak + uji; widget online eksplisit; internet ~30 dtk paralel
  + skip bila gateway offline; checkpoint kedaluwarsa 48 jam; 2 uji baru;
  CHANGELOG [Unreleased].

### Sesi #7 — 2026-10-03 13:35 UTC — selesai
- Perbaiki SEMUA file memori: tulis ulang `netradar.md` ini dengan stempel
  absolut + nomor sesi (masalah: label relatif "pagi/sore/malam/kemarin" untuk
  kejadian satu hari yang sama); tambah aturan anti-bingung waktu di `SOUL.md`.
