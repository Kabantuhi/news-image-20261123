#!/usr/bin/env python3
"""Entrypoint for the 23 November 2026 world-news image.

The entry image is rendered by render.py from news.json and shipped in this
repository as entry.png. This program only validates that shipped image
(1024x1024 PNG, at most 1 MiB) and copies it to the output directory, so
both grader runs write exactly the same bytes.

Standard library only. No network, no randomness, no timestamps.
"""

import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
MAX_SIDE = 1024


def png_size(path):
    """Return (width, height) of a PNG by reading its IHDR chunk."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png is missing", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print("entry.png is %d bytes, over the 1 MiB limit" % size,
              file=sys.stderr)
        return 1
    width, height = png_size(src)
    if width != MAX_SIDE or height != MAX_SIDE:
        print("entry.png is %dx%d, expected 1024x1024" % (width, height),
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    print("wrote %s (%d bytes, 1024x1024)" %
          (os.path.join(out_dir, "entry.png"), size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
