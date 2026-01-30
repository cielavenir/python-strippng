#!/usr/bin/env python3

__version__ = '0.0.0.1'

from struct import unpack
from typing import BinaryIO

def StripPNG(fin: BinaryIO, fout: BinaryIO) -> None:
    head = fin.read(8)
    assert head == b"\x89PNG\x0d\x0a\x1a\x0a"
    fout.write(head)
    while True:
        head = fin.read(8)
        if len(head) < 8:
            break
        size, typ = unpack(">I4s", head)
        data = fin.read(size + 4)  # footer CRC
        if typ in (b"IHDR", b"PLTE", b"tRNS", b"IDAT", b"IEND"):
            fout.write(head)
            fout.write(data)

if __name__ == '__main__':
    import sys
    StripPNG(sys.stdin.buffer, sys.stdout.buffer)
