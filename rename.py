import os
import sys

def main():
    base = sys.argv[1]
    for n, path in enumerate(os.listdir(base)):
        print(path)
        os.rename(base + '/' + path, base + '/' + str(n+400))

if __name__ == '__main__':
    main()
