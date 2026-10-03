# Memori Agents AI

Memori terpusat antar-sesi dan antar-mesin untuk agen AI yang mengelola repo Tasirin.

## Soul

- `SOUL.md` — identitas tetap agen (1 soul untuk semua repo). Dibaca tiap awal sesi sebelum file memori.

## File

- `tasirin-download-manager.md` — memori repo download manager.
- `tasirin-vaultwarden-host.md` — memori repo vaultwarden host.
- `Red-Eye-Mobile.md` — memori repo Red Eye Mobile.
- `netradar.md` — memori repo NetRadar.

## Alur pakai (wajib, lihat pointer di `AGENTS.md` tiap repo)

1. Awal sesi: `git pull --ff-only` repo ini, lalu baca file memori repo yang dikerjakan.
2. Akhir sesi: update file memori, commit + push ke repo ini.

Gaya commit: `memory: <nama-repo> - <ringkasan singkat>`.
