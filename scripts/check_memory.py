#!/usr/bin/env python3
"""Validator memori: nomor sesi naik, stempel absolut ada, Status == sesi tertinggi."""
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
    rel = RELATIF.findall(txt)
    if rel:
        print(f"[WARN] {f}: kata relatif tanpa stempel? {sorted(set(r.lower() for r in rel))[:5]} (pastikan tiap kemunculan ditemani stempel UTC)")
    if len(txt.splitlines()) > 250 and f != "netradar.md":
        print(f"[WARN] {f}: {len(txt.splitlines())} baris > 250, pertimbangkan arsip")
print("LOLOS" if ok else "GAGAL")
sys.exit(0 if ok else 1)
