#!/usr/bin/env python3
"""Validator memori: nomor sesi naik, stempel absolut ada, Status == sesi tertinggi, README sinkron."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = ["Red-Eye-Mobile.md", "netradar.md", "tasirin-download-manager.md", "tasirin-vaultwarden-host.md"]
STAMP = re.compile(r"20\d\d-\d\d-\d\d \d\d:\d\d UTC")
SESI = re.compile(r"^#{2,3} Sesi #(\d+)\b", re.M)
STATUS = re.compile(r"## Status terakhir \((\d{4}-\d\d-\d\d \d\d:\d\d UTC).*?sesi #(\d+)", re.I | re.S)
RELATIF = re.compile(r"(kemarin|barusan|tadi pagi|tadi sore|tadi malam|sesi sebelumnya|yang baru saja)", re.I)

ok = True
for f in FILES:
    p = ROOT / f
    if not p.exists():
        print(f"[MISS] {f} tidak ada"); ok = False; continue
    txt = p.read_text()
    nums = [int(m.group(1)) for m in SESI.finditer(txt)]
    if nums:
        if nums != sorted(nums):
            print(f"[FAIL] {f}: nomor sesi tidak urut: {nums[:8]}...{nums[-5:]}"); ok = False
        else:
            print(f"[OK] {f}: {len(nums)} sesi, #{nums[0]}..#{nums[-1]}")
        no_stamp = []
        for m in SESI.finditer(txt):
            line_end = txt.find("\n", m.start())
            head = txt[m.start():line_end if line_end != -1 else m.start()+200]
            if not STAMP.search(head):
                no_stamp.append(int(m.group(1)))
        if no_stamp:
            print(f"[FAIL] {f}: sesi tanpa stempel absolut di judul: {no_stamp}"); ok = False
        m = STATUS.search(txt)
        if m and nums and int(m.group(2)) != max(nums):
            print(f"[FAIL] {f}: Status terakhir sesi #{m.group(2)} != max #{max(nums)}"); ok = False
    else:
        # file jilid-based (download-manager): cek stempel di heading
        heads = re.findall(r"^## .+", txt, re.M)
        print(f"[OK] {f}: {len(heads)} seksi (mode jilid, tanpa nomor)")
    hits = set()
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith(">") or "DILARANG" in s:
            continue  # kutipan / definisi aturan, bukan pemakaian waktu relatif
        s = re.sub(r"`[^`]*`", "", s)
        hits.update(r.lower() for r in RELATIF.findall(s))
    if hits:
        print(f"[WARN] {f}: kata relatif tanpa stempel? {sorted(hits)[:5]} (pastikan tiap kemunculan ditemani stempel UTC)")
    if len(txt.splitlines()) > 250 and f != "netradar.md":
        print(f"[WARN] {f}: {len(txt.splitlines())} baris > 250, pertimbangkan arsip")

# --- konsistensi tabel status di README (indeks utama) ---
readme = ROOT / "README.md"
if not readme.exists():
    print("[FAIL] README.md tidak ada"); ok = False
else:
    rows = {}
    for line in readme.read_text().splitlines():
        m = re.match(r"\|\s*`([^`]+\.md)`\s*\|", line)
        if m:
            rows[m.group(1)] = line
    for f in FILES:
        p = ROOT / f
        if not p.exists():
            continue
        m = STATUS.search(p.read_text())
        if not m:
            continue
        date, sesi = m.group(1), m.group(2)
        row = rows.get(f)
        if row is None:
            print(f"[FAIL] README.md: baris {f} tidak ada di tabel status"); ok = False; continue
        if date not in row:
            print(f"[FAIL] README.md: {f} tanggal basi (memori {date})"); ok = False
        if f"sesi #{sesi}" not in row:
            print(f"[FAIL] README.md: {f} sesi basi (memori sesi #{sesi})"); ok = False
print("LOLOS" if ok else "GAGAL")
sys.exit(0 if ok else 1)
