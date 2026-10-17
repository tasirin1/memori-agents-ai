# AGENTS.md — Memori Agents AI (OpenCode entrypoint)

> File ini auto-load oleh OpenCode tiap sesi. Jaga tetap < 100 baris.

## Apa ini

Repo memori terpusat antar-sesi dan antar-mesin untuk repo Tasirin.
Identitas agen: `SOUL.md`. Indeks status: `README.md`.

## Aturan sesi (wajib)

1. Awal sesi: `git pull --ff-only`, lalu baca `SOUL.md` + **1 file memori yang dikerjakan saja**. Jangan baca arsip (`archive/`) kecuali perlu forensik.
2. Akhir sesi: tambah 1 seksi sesi baru + update "Status terakhir", jalankan `python3 scripts/check_memory.py`, lalu commit + push.
3. Stempel waktu: `YYYY-MM-DD HH:MM UTC` via `date -u`. DILARANG kata relatif tanpa stempel (kemarin, tadi, pagi/sore/malam).
4. Bahasa: Indonesia di memori. Gaya commit: `memory: <nama-repo> - <ringkasan>`.
5. Aturan kerja lintas repo — **mode perbaiki = maraton** + **audit sub-agen paralel dengan verifikasi mandiri** — ada di `SOUL.md` (seksi "Aturan maraton perbaikan & sub-agen"); salinannya di `AGENTS.md` tiap repo. Baca sebelum kerja perbaikan/audit.

## File memori aktif (baca salah satu saja)

- `Red-Eye-Mobile.md` — repo `tasirin1/Red-Eye-Mobile`, branch `main`, max 20 sesi terakhir.
- `tasirin-download-manager.md` — repo `tasirin1/tasirin-download-manager`, branch `main`.
- `tasirin-vaultwarden-host.md` — repo `tasirin1/tasirin-vaultwarden-host`, branch `main`.
- `netradar.md` — repo `tasirin1/netradar`, branch `master` (bukan main).

Arsip dingin: `archive/*-arsip.md`. Skill bug-bounty: `.opencode/skills/bug-bounty/SKILL.md` (load via skill tool bila perlu, tidak auto-load).
Pindah device baru: lihat `BOOTSTRAP.md` (clone sekali + 1 blok tempel per repo app).

## Batas ukuran

- File aktif target < 250 baris. Bila sesi > 20, pindahkan sesi tertua ke `archive/` (copy body apa adanya + update daftar isi arsip).
- Jangan commit secret/keystore. `git diff --check` harus bersih.
