#!/usr/bin/env python3
# Based on WessellUrdata/vbmeta-disable-verification (MIT).
# Patches AVB flags to disable dm-verity and verification.
import os
import sys

AVB_MAGIC = b"AVB0"
FLAGS_OFFSET = 123
FLAGS_TO_SET = b"\x03"

def main(path: str) -> None:
    try:
        with open(path, "r+b") as f:
            magic = f.read(4)
            if magic != AVB_MAGIC:
                raise SystemExit(
                    "ERROR: input does not start with AVB0; refusing to modify it."
                )
            f.seek(FLAGS_OFFSET)
            current = f.read(1)
            if len(current) != 1:
                raise SystemExit("ERROR: vbmeta header is truncated.")
            f.seek(FLAGS_OFFSET)
            f.write(FLAGS_TO_SET)
            f.flush()
            os.fsync(f.fileno())
        print(f"Patched {path}: AVB flags 0x{current[0]:02x} -> 0x03")
    except OSError as exc:
        raise SystemExit(f"ERROR: {exc}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: patch-vbmeta.py vbmeta.img")
    main(sys.argv[1])
