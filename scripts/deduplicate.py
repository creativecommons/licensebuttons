import sys
import traceback
import os
from pathlib import Path
import hashlib
from shutil import copyfile

EURO = [
    "b9f4175382a404007e19d3566061e36c", 
    "9076ddd6ddf0bffc24e6ac71c1353d33", 
    "1d7fb4e154e7198dfb39d16d9800844d"
]

def main():
    # Gets the full path of the www/l directory.
    path = Path().resolve().parent.joinpath("www", "l")
    # Stores the original files
    original_files = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            # Join the file name with the current folder.
            # www/l/by-nc/1.0  +  80x15.png  -->  www/l/by-nc/1.0/80x15.png
            f = Path(root).joinpath(file)

            # Calculate the MD5 of the file by opening the file in the
            # binary mode and using hashlib.
            digest = hashlib.md5(open(str(f), "rb").read()).hexdigest()

            # Check if MD5 already contains in the list.
            if digest in original_files:

                # Save it in the dictionary for creating symbolic link later.
                original_files[digest]["symlinks"].append(str(f))
            else:
                # Gets the relative path of the file,
                # www/l/by-nc/1.0/80x15.png   -->   by-nc/1.0/80x15.png
                relative = Path(f).relative_to(path)

                # Joins the first and last part of the file parts
                # so it can be used moving the file to the parent license folder
                # because some files are under 2 sub-directories.
                # by-nc/1.0/80x15.png  -->  by-nc       - first
                #                       x   1.0
                #                      -->  80x15.png   - last
                parent = Path(path).joinpath(os.path.join(Path(relative).parts[0], Path(relative).parts[-1]))

                # If the file contains an euro symbol, add -e tag to the end of file
                # to avoid the overwriting.
                if digest in EURO:
                    parent = Path(str(parent).replace(".png", "-e.png"))

                symlinks = []
                
                # If the file path is NOT same as with the parent folder,
                # - Copy the file to the parent folder.
                #   by-nc/1.0/80x15.png  -->  by-nc/80x15.png
                #
                # - And save the file path in the symlinks list,
                #   so the old file will be deleted and used as
                #   symbolic link.
                #
                #   "by-nc/1.0/80x15.png"
                #   Will be deleted and replaced with symbolic link
                #   that points to "by-nc/80x15.png"                      
                if str(parent) != str(f):
                    symlinks = [ str(f) ]
                    if not os.path.exists(str(parent)):
                        copyfile(str(f), str(parent))

                original_files[digest] = {
                    "base": str(parent),
                    "symlinks": symlinks
                }
    # Start deleting the duplicated files and create
    # symbolic links instead.
    for value in original_files.values():
        for link in value["symlinks"]:
            os.remove(link)
            os.symlink(value["base"], link)


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