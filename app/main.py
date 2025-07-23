import sys
import os
import zlib


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

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
