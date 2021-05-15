#!/usr/bin/env python3
from update_metadata_pb2 import DeltaArchiveManifest 
import sys, os, struct, bz2

BLOCK_SIZE = 4096
def extract(img, outname):
    with open(outname,'wb') as out:
        with open(img,'rb') as f:
            magic = f.read(4)
            if magic != b'CrAU':
                raise "Wrong header"
            major = struct.unpack('>Q',f.read(8))[0]
            if major != 1:
                raise "Unsupported version"
            size = struct.unpack('>Q', f.read(8))[0]
            manifest = f.read(size)
            msg = DeltaArchiveManifest.FromString(manifest)
            pos = f.tell()
            written=0
            for chunk in msg.install_operations:
                f.seek(pos + chunk.data_offset)
                data  = f.read(chunk.data_length)
                dst_offset = chunk.dst_extents[0].start_block * BLOCK_SIZE
                dst_length  = chunk.dst_extents[0].num_blocks * BLOCK_SIZE
                if chunk.type == 1:
                    data = bz2.decompress(data)
                elif chunk.type == 0:
                    print("offset:{}".format(dst_offset))
                else:
                    raise "Unsupported type " + chunk.type

                padding = dst_length - len(data)
                if (padding < 0):
                    raise "Wrong length"
                out.seek(dst_offset)
                out.write(data)
                out.write(b'\x00'*padding)
                written += len(data)
                print("\r{}".format(written), end="")

            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extractor.py updatefile [rawimage]")
        sys.exit(1)
    img = sys.argv[1]
    outname = 'out'
    if len(sys.argv) > 2:
        outname = sys.argv[2]
    extract(img,outname)
    print("Wrote rawimage file: {}".format(outname))

