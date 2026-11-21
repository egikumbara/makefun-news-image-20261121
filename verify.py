#!/usr/bin/env python3
"""Verify the news-image-20261121 entry.

Runs main.py twice into two separate dirs, compares the PNGs byte for
byte, and checks the image is exactly 1024x1024 and at most 1 MiB.
Prints PASS/FAIL plus the SHA-256 of the output.
"""
import hashlib
import os
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576


def png_size(path):
    with open(path, "rb") as f:
        data = f.read(33)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def main():
    ok = True
    dirs = []
    try:
        for name in ("verify_out1", "verify_out2"):
            d = os.path.join(HERE, name)
            shutil.rmtree(d, ignore_errors=True)
            os.makedirs(d, exist_ok=True)
            dirs.append(d)
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=d)
            r = subprocess.run([sys.executable, os.path.join(HERE, "main.py")],
                               env=env, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"FAIL: main.py run into {name} exited {r.returncode}")
                print(r.stdout)
                print(r.stderr)
                return 1
        p1 = os.path.join(dirs[0], "entry.png")
        p2 = os.path.join(dirs[1], "entry.png")
        with open(p1, "rb") as f:
            b1 = f.read()
        with open(p2, "rb") as f:
            b2 = f.read()
        sha = hashlib.sha256(b1).hexdigest()
        print(f"SHA-256: {sha}")
        print(f"Size: {len(b1)} bytes (limit {MAX_BYTES})")
        if b1 != b2:
            print("FAIL: two runs differ")
            ok = False
        else:
            print("Determinism: identical bytes across two runs")
        size = png_size(p1)
        print(f"Dimensions: {size[0]}x{size[1]}" if size else "FAIL: not a PNG")
        if size != (1024, 1024):
            print("FAIL: dimensions are not 1024x1024")
            ok = False
        if len(b1) > MAX_BYTES:
            print("FAIL: PNG exceeds 1 MiB")
            ok = False
    finally:
        for d in dirs:
            shutil.rmtree(d, ignore_errors=True)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
