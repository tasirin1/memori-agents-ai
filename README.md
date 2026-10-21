# Memori Agents AI

Memori terpusat antar-sesi dan antar-mesin untuk agen AI yang mengelola repo Tasirin.
Optimal untuk **OpenCode**: entrypoint `AGENTS.md` (auto-load), identitas `SOUL.md`, indeks file ini.

## Status repo (baca ini dulu, bukan arsip)

| Memori aktif | Repo + branch | Status terakhir |
|---|---|---|
| `Red-Eye-Mobile.md` | `tasirin1/Red-Eye-Mobile` (`main`) | 2026-10-21 14:20 UTC = sesi #298 — `v1.6.445` (`2d557f5`), 3 tag + Release sukses |
| `tasirin-download-manager.md` | `tasirin1/tasirin-download-manager` (`main`) | 2026-10-17 12:31 UTC — aturan maraton + sub-agen di `AGENTS.md`; jilid 27 (2026-10-13) bersih |
| `tasirin-vaultwarden-host.md` | `tasirin1/tasirin-vaultwarden-host` (`main`) | 2026-10-17 12:31 UTC = sesi #71 — aturan maraton + sub-agen |
| `netradar.md` | `tasirin1/netradar` (`master`) | 2026-10-17 12:31 UTC = sesi #18 — master HIJAU, aturan maraton + sub-agen |

Arsip dingin (jangan dibaca tiap sesi): `archive/` — Red-Eye #2–#288, download-manager jilid lama, vaultwarden #1–66.

## Soul

- `SOUL.md` — identitas tetap agen (1 soul untuk semua repo). Dibaca tiap awal sesi sebelum file memori.

## Skill (OpenCode, on-demand)

- `.opencode/skills/bug-bounty/SKILL.md` — workflow bug-bounty. Load via skill tool hanya bila perlu, tidak auto-load.

## Alur pakai (detail di `AGENTS.md`)

1. Awal sesi: `git pull --ff-only` repo ini, lalu baca `SOUL.md` + **1 file memori yang dikerjakan**.
2. Akhir sesi: update file memori, `python3 scripts/check_memory.py`, commit + push.

Gaya commit: `memory: <nama-repo> - <ringkasan singkat>`.
