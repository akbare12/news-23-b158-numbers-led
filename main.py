#!/usr/bin/env python3
"""Entry-point for THE WORLD TODAY — Monday 23 November 2026 (31 stories).

Stdlib only (no image library): parses the PNG header and chunk stream of
entry.png with struct/zlib, verifies size, dimensions and checksums, then
copies the bytes to MAKEFUN_OUTPUT_DIR/entry.png. Writes ONLY to the output
directory, never next to this file.
"""
import hashlib
import os
import struct
import sys
import zlib

# Filled in after the first render (second write of this file).
# NOTE: expected values are refreshed on every re-render; the final values
# below match the entry.png committed with this file.
EXPECTED_SHA256 = "f19d19e842843c032c01e7f9efaae822bc95e1c391b26ab7bb0ae6120beaa8f4"
EXPECTED_SIZE = 158463

MIN_SIZE = 10_000
MAX_SIZE = 1_048_576


def fail(msg):
    print("main.py: " + msg, file=sys.stderr)
    return 1


def check_png(data):
    """Validate a PNG byte string. Returns (width, height) or raises."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("bad PNG signature")
    if len(data) < MIN_SIZE:
        raise ValueError("too small: %d bytes" % len(data))
    if len(data) > MAX_SIZE:
        raise ValueError("too large: %d bytes" % len(data))
    # First chunk must be a 13-byte IHDR.
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR")
    ihdr = data[16:29]
    w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (1024, 1024):
        raise ValueError("bad dimensions %dx%d" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        raise ValueError("bad bit depth %d / colour type %d" % (depth, ctype))
    if comp != 0 or filt != 0 or inter != 0:
        raise ValueError("bad compression/filter/interlace flags")
    (crc_stored,) = struct.unpack(">I", data[29:33])
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != crc_stored:
        raise ValueError("CRC mismatch in chunk b'IHDR'")
    # Walk the remaining chunks: CRC each one, require non-empty IDATs and
    # a final zero-length IEND with no trailing data.
    pos, idat_total, saw_iend = 33, 0, False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype_b = data[pos + 4:pos + 8]
        end = pos + 8 + clen + 4
        if end > len(data):
            raise ValueError("truncated chunk %r" % ctype_b)
        (crc_stored,) = struct.unpack(">I", data[pos + 8 + clen:end])
        if zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != crc_stored:
            raise ValueError("CRC mismatch in chunk %r" % ctype_b)
        if ctype_b == b"IDAT":
            if clen == 0:
                raise ValueError("empty IDAT chunk")
            idat_total += clen
        if ctype_b == b"IEND":
            if clen != 0:
                raise ValueError("IEND must be empty")
            if end != len(data):
                raise ValueError("trailing data after IEND")
            saw_iend = True
            break
        pos = end
    if not saw_iend:
        raise ValueError("missing IEND")
    if idat_total < 1000:
        raise ValueError("IDAT payload too small: %d" % idat_total)
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.commonpath([out_dir_abs, here]) == here:
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if os.path.isfile(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source image")
    with open(src, "rb") as f:
        data = f.read()
    try:
        w, h = check_png(data)
    except ValueError as e:
        return fail("invalid entry.png: %s" % e)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and sha != EXPECTED_SHA256:
        return fail("sha256 mismatch: got %s" % sha)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        return fail("size mismatch: got %d" % len(data))
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output re-read does not match source")
    print("main.py: wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dst, w, h, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
