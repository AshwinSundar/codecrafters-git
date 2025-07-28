import sys
import os
import zlib
from hashlib import sha1


def extract_content(obj: bytes) -> str:
    null_byte_loc = obj.find(b'\x00')
    return obj[null_byte_loc + 1:].decode()


def main():
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")

    elif command == "cat-file":
        flag1 = sys.argv[2]
        hash = sys.argv[3]

        if flag1 != "-p":
            raise RuntimeError(f"Unrecognized flag:{flag1}\nValid options: -p")

        with open(f".git/objects/{hash[0:2]}/{hash[2:]}", "rb") as file:
            obj = zlib.decompress(file.read())
            print(extract_content(obj), end='')

    elif command == "hash-object":
        flag1 = sys.argv[2]
        fileName = sys.argv[3]

        if flag1 != "-w":
            raise RuntimeError(f"Unrecognized flag:{flag1}\nValid options: -w")

        with open(fileName, "rb") as file:
            contents = file.read()
            header = f"blob {len(contents)}\x00".encode()  # define header format

            # compute hash of object
            hash = sha1(header + contents).hexdigest()
            print(hash)

            # split up hash
            objectsDir = '.git/objects'
            dirName = hash[:2]
            fileName = hash[2:]

            if not os.path.isdir(f'{objectsDir}/{dirName}'):
                os.mkdir(f'{objectsDir}/{dirName}')

            # write compressed data to file
            with open(f'{objectsDir}/{dirName}/{fileName}', 'wb') as out_file:
                out_file.write(zlib.compress(header + contents))

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
