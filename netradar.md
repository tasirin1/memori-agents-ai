# Memori Sesi — NetRadar

> Memori terpusat antar-sesi dan antar-mesin. Update tiap akhir sesi, commit + push. Dibaca tiap awal sesi, di-update tiap akhir sesi.

## Proyek

- Repo: `tasirin1/netradar` — radar jaringan Android, Jetpack Compose (minSdk 29, targetSdk 36).
- Aturan main (ringkas dari `AGENTS.md`): build resmi HANYA via CI; semua Bahasa Indonesia; commit `type: deskripsi` (`feat`/`fix`/`refactor`/`test`/`perf`/`docs`); `versionName` tetap `"2.0"`, `versionCode` otomatis; guard changelog di CI (perubahan `app/src`, `scripts/`, `.github/workflows/`, `app/build.gradle.kts` wajib sertakan `CHANGELOG.md`); unit test logika murni tanpa Robolectric.
- Workflow Build docs-only skip (`**.md`, `LICENSE`, `.gitignore`) — selaras repo Tasirin lain.

## Status terakhir (2026-10-03)

- Onboarding ke mesin: clone + pointer `MEMORY.md` di `AGENTS.md` + docs-only skip CI.

## Tugas terbuka

- (belum ada)

## Cara pakai file ini

- Awal sesi: baca file ini, lalu `git status --short` + `git log --oneline -5`.
- Akhir sesi: update tanggal, status terakhir, dan tugas terbuka.

## Audit bug 2026-10-03
- Audit statis seluruh kode (tanpa perubahan file): ditemukan ~14 bug/kandidat, dilaporkan ke user, belum diperbaiki.
- Fokus berikutnya bila user setuju: DNS di main thread, Semaphore blokir, UdpScanner tanpa semaphore, mergeHost tak pernah lupa port, retry double-count, subList resume crash.

## Perbaikan audit 2026-10-03 (belum push — perubahan di working tree /root/netradar)
- Perbaiki 15 temuan audit: race ScannerManager (jobLock + null identitas), DNS di
  main thread (startScan/startSingleMonitor/refreshNetworkInfo ke IO), Semaphore
  blokir → kotlinx.coroutines.sync di 4 scanner + semaphore baru UdpScanner,
  retry double-count + missed cap 2000 + clamp checkpoint di ScanLoop, RTSP 25 baris,
  mergeHost otoritatif (ganti union/OR), uptime/ping append + throttle 10 dtk,
  cap CustomPortParser 1000, tolak IPv6, IP penuh → sisa /24 sendiri, PingUtil
  waitFor budget + PingSweep pakai speed.timeoutMs, traceroute IPv6 + selesai longgar.
- Test: NetworkUtilsTest (IP-/24, IPv6, IP:port) + CustomPortParserTest (cap).
  CHANGELOG [Unreleased] + README lintas-subnet diperbarui. AGENTS.md sudah
  M sebelum sesi (tidak disentuh).
- Verifikasi: tanpa JDK lokal; kompilasi + unit test diserahkan ke CI
  (`testDebugUnitTest` via workflow Build). Belum commit/push repo netradar.

## Rilis 2026-10-03 12:20 UTC — sukses
- Push master 6 commit (fix audit + test + docs): Build 37122297630 success
  semua 13 step (guard changelog, keystore, test, lint, R8, apksigner,
  VirusTotal, artifact, cek 5MB). Release v2.0 terbit.
- Sempat gagal 1× (return eksplisit probe kamera/router), +1× guard changelog
  pada push uji — diatasi via commit susulan + uji ScanLoopTest.

## Audit bug 2026-10-03 (sesi sore, read-only, belum diperbaiki)
- Minta user: "cek seluruh kode temukan bug". Audit statis ~8.300 baris, tanpa ubah file repo.
- Temuan: 11 bug/kandidat (3 tinggi, 5 sedang, 3+ rendah). Rincian lengkap di laporan chat sesi ini.
- Sorotan: (1) scan PING/TRACE menghapus openPorts via mergeHost otoritatif — regresi; (2) Traceroute probeHop waitFor() tanpa timeout → gantung; (3) rescanHost hilangkan osGuess + reset lastSeenScan; (4) probe kamera/RTSP baca 25 baris tanpa stop di baris kosong → tahan thread IO; (5) notif favorit offline timestamp global tunggal; (6) diff antar-mode menyesatkan; (7) deep scan abaikan pause; (8) onCleared tulis prefs di main thread; (9) notif ID hashCode tabrakan; (10) label terhapus hidup lagi; (11) kandidat regex traceroute EXCEEDED butuh ":" (format-dependent) + UDP SSDP/mDNS unicast false-negative + scanIps await berurutan.
- Belum ada perbaikan/push repo netradar sesi ini (murni audit).
