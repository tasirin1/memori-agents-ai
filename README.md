# Memori Agents AI

Memori terpusat antar-sesi dan antar-mesin untuk agen AI yang mengelola repo Tasirin.
Optimal untuk **OpenCode**: entrypoint `AGENTS.md` (auto-load), identitas `SOUL.md`, indeks file ini.

## Status repo (baca ini dulu, bukan arsip)

| Memori aktif | Repo + branch | Status terakhir |
|---|---|---|
| `Red-Eye-Mobile.md` | `tasirin1/Red-Eye-Mobile` (`main`) | 2026-10-15 02:57 UTC = sesi #176 — `v1.6.222` (`806cf80`), menunggu CI |
| `tasirin-download-manager.md` | `tasirin1/tasirin-download-manager` (`main`) | 2026-10-13 07:15 UTC — sapuan jilid 27 bersih, HEAD `1837c2a` |
| `tasirin-vaultwarden-host.md` | `tasirin1/tasirin-vaultwarden-host` (`main`) | 2026-10-15 03:20 UTC = sesi #70 + lanjutan — workflow gabungan `a2f3b35` |
| `netradar.md` | `tasirin1/netradar` (`master`) | 2026-10-15 05:14 UTC = sesi #17 — master HIJAU semua |

Arsip dingin (jangan dibaca tiap sesi): `archive/` — Red-Eye #2–156, download-manager jilid lama, vaultwarden #1–66.

## Soul

- `SOUL.md` — identitas tetap agen (1 soul untuk semua repo). Dibaca tiap awal sesi sebelum file memori.

## Skill (OpenCode, on-demand)

- `.opencode/skills/bug-bounty/SKILL.md` — workflow bug-bounty. Load via skill tool hanya bila perlu, tidak auto-load.

## Alur pakai (detail di `AGENTS.md`)

1. Awal sesi: `git pull --ff-only` repo ini, lalu baca `SOUL.md` + **1 file memori yang dikerjakan**.
2. Akhir sesi: update file memori, `python3 scripts/check_memory.py`, commit + push.

Gaya commit: `memory: <nama-repo> - <ringkasan singkat>`.
