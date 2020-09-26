# Replaces duplicate files with symlinks
import sys
import traceback
import os
from pathlib import Path
import hashlib
import json
from shutil import copyfile

EURO = [
    "b9f4175382a404007e19d3566061e36c", 
    "9076ddd6ddf0bffc24e6ac71c1353d33", 
    "1d7fb4e154e7198dfb39d16d9800844d"
]

def count(path):
    count = {
        "files": 0,
        "links": 0,
        "unique": 0,
        "hashes": []
    }
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.islink(os.path.join(root, file)):
                count["links"] = count["links"] + 1
            elif os.path.isfile(os.path.join(root, file)):
                count["files"] = count["files"] + 1
                h = hashlib.md5(open(os.path.join(root, file), "rb").read()).hexdigest()
                count["hashes"].append(h)
    count["hashes"] = list(set(count["hashes"]))
    count["unique"] = len(count["hashes"])
    return count


def main():
    # Gets the full path of the www/l directory.
    path = Path().resolve().parent.joinpath("www", "l")
    hashes = set(count(str(path))["hashes"])
    print(count(str(path)))
    # Stores the original files
    original_files = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            f = Path(root).joinpath(file)
            digest = hashlib.md5(open(str(f), "rb").read()).hexdigest()
            # Check if MD5 already contains in the list.
            if digest in original_files:
                # Save
                original_files[digest]["symlinks"].append(str(f))
            else:
                # Gets the relative path of the file,
                # www/l/by-nc/1.0/80x15.png   -->   by-nc/1.0/80x15.png
                relative = Path(f).relative_to(path)

                # Joins the first and last part of the file
                # for moving the file to the parent license folder
                # because some files are under 2 sub-directories.
                # by-nc/1.0/80x15.png  -->  by-nc + 80x15.png
                parent = Path(path).joinpath(os.path.join(Path(relative).parts[0], Path(relative).parts[-1]))

                if digest in EURO:
                    parent = Path(str(parent).replace(".png", "-e.png"))

                original_files[digest] = {
                    "base": str(parent),
                    "symlinks": [
                        str(f)
                    ]
                }
    for value in original_files.values():
        # Copy one of the duplicated files to the parent folder
        # for creating symbolic link.
        if value["symlinks"][0] != value["base"]:
            copyfile(value["symlinks"][0], value["base"])
        # Delete all duplicated files and replace them with
        # symbolic link.
        for link in value["symlinks"]:
            if link != value["base"]:
                os.remove(link)
                os.symlink(value["base"], link)
    hashes2 = set(count(str(path))["hashes"])
    print(list(hashes - hashes2))
    print(count(str(path)))
    open("output.json", "w+").write(json.dumps(original_files, indent = 4))


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code)
    except KeyboardInterrupt:
        print("INFO (130) Halted via KeyboardInterrupt.", file=sys.stderr)
        sys.exit(130)
    except Exception:
        print("ERROR (1) Unhandled exception:", file=sys.stderr)
        print(traceback.print_exc(), file=sys.stderr)
        sys.exit(1)