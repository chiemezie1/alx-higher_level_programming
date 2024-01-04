#!/usr/bin/python3
import builtins
if __name__ == "__main__":
    for name in dir(builtins):
        if name[:2] != "__":
            print(name)
