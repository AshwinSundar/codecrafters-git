import sys
import os
import zlib


def find_nth(string, substring, n):
    '''Helper for extract_content'''
    if (n == 1):
        return string.find(substring)
    else:
        return string.find(substring, find_nth(string, substring, n - 1) + 1)


def extract_content(obj: str):
    return find_nth(obj, " ", 2) + 1


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
            obj_raw = file.read()
            obj_decompressed = zlib.decompress(obj_raw).decode()
            print(obj_decompressed[extract_content(obj_decompressed):])

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
