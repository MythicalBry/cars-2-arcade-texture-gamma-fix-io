import struct
import os
import sys
from pathlib import Path

# Change this path to your target directory
target_dir = Path(sys.argv[1])

for name in os.listdir(target_dir):
    if name.lower().endswith(".dds"):
        file_path = os.path.join(target_dir, name)

        if not os.path.isfile(file_path):
            continue

        if os.path.getsize(file_path) < 0x78:
            print(f"Skipping (too small to patch): {name}")
            continue

        with open(file_path, "r+b") as f:
            f.seek(0x74)
            dwCaps3 = struct.unpack("<I", f.read(4))[0]

            # Patch only if 0x1 flag is missing
            if not (dwCaps3 & 0x1):
                new_dwCaps3 = dwCaps3 | 0x1
                f.seek(0x74)
                f.write(struct.pack("<I", new_dwCaps3))
                print(f"Patched: {name}")
            else:
                print(f"Already patched: {name}")
