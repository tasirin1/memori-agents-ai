# Bootstrap — pindah device baru

Tujuan: dari mesin kosong sampai agen bisa pakai memori, tanpa ingat-ingat path.

## Langkah 1 (sekali per device): clone repo memori

```bash
git clone https://github.com/tasirin1/memori-agents-ai ~/memori-agents-ai
```

## Langkah 2 (sekali per repo app): tempel 1 blok ini di ATAS `AGENTS.md` repo tersebut

Ganti `<FILE>` dengan file memorinya. Daftar file:

| Repo app | `<FILE>` |
|---|---|
| `tasirin1/Red-Eye-Mobile` (`main`) | `Red-Eye-Mobile.md` |
| `tasirin1/tasirin-download-manager` (`main`) | `tasirin-download-manager.md` |
| `tasirin1/tasirin-vaultwarden-host` (`main`) | `tasirin-vaultwarden-host.md` |
| `tasirin1/netradar` (`master`) | `netradar.md` |

```md
## Memori lintas-sesi (wajib tiap sesi)

- Repo memori: `~/memori-agents-ai` (`tasirin1/memori-agents-ai`). Bila folder belum ada di mesin ini, clone dulu (lihat `BOOTSTRAP.md` di repo itu).
- Awal sesi: `git -C ~/memori-agents-ai pull --ff-only`, lalu baca `~/memori-agents-ai/SOUL.md` + `~/memori-agents-ai/<FILE>`. Jangan baca `archive/` kecuali perlu forensik.
- Akhir sesi: update `<FILE>` (seksi sesi baru + "Status terakhir"), `python3 ~/memori-agents-ai/scripts/check_memory.py`, commit + push (`memory: <repo> - <ringkasan>`).
- Stempel waktu: `YYYY-MM-DD HH:MM UTC` via `date -u`. Dilarang kata relatif tanpa stempel.
```

## Kenapa begini (bukan submodule)

Submodule ikut ke-clone tapi bikin tiap repo app berat + gampang konflik saat push memori dari mesin lain. Pointer + clone-sekali lebih tahan untuk ganti-ganti device: repo app tetap ringan, memori tetap 1 sumber.
