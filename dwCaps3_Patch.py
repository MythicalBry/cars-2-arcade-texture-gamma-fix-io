import struct
import os
import sys
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Patch .dds files at 0x74 from 00 to 01, making them gamma correct in Cars 2 Arcade.",
        usage="<script_file> -i <folder_path>",
        epilog="""
Examples:
<script_file> -i textures
<script_file> --input "C:\\Documents\\Games\\Cars 2 Arcade\\textures"
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-i",
        "--input", 
        required=True, 
        metavar="FOLDER", 
        help="Path to the folder containing .dds images"
    )
    
    args = parser.parse_args()
    target_dir = Path(args.input)

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

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

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No arguments provided.\n")
        print("Use -h or --help to see usage.\n")
        sys.exit(1)

    main()