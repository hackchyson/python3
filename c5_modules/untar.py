# coding=utf8
"""
@project: python3
@file: untar
@author: mike
@time: 2021/2/4
 
@function:
"""
import tarfile
import string
import sys
import os

BZ2_AVAILABLE = True
try:
    import bz2
except ImportError:
    BZ2_AVAILABLE = False

# absolute path is not permitted
UNTRUSTED_PREFIXES = tuple(['/', '\\'] + [c + ':' for c in string.ascii_letters])


def untar(archive):
    tar = None
    try:
        tar = tarfile.open(archive)
        for member in tar.getmembers():
            if member.name.startswith(UNTRUSTED_PREFIXES):
                print('untrusted prefix, ignoring', member.name)
            elif '..' in member.name:
                print('suspect path, ignoring', member.name)
            else:
                tar.extract(member)
                print('unpacked', member.name)
    except (tarfile.TarError, EnvironmentError) as err:
        print(err)
    finally:
        if tar is not None:
            tar.close()


def error(message, exit_status=1):
    print(message)
    sys.exit(exit_status)


def main():
    if len(sys.argv) != 2 or sys.argv[1] in {"-h", "--help"}:
        error("usage: untar.py archive.{{tar,{0}tar.gz}}".format(
            "tar.bz2," if BZ2_AVAILABLE else ""), 2)

    archive = sys.argv[1]
    if not archive.lower().endswith((".tar", ".tar.gz", ".tar.bz2")):
        error("{0} doesn't appear to be a tarball".format(archive))
    if not BZ2_AVAILABLE and archive.lower().endswith(".bz2"):
        error("bzip2 decompression is not available")
    if not os.path.exists(archive):
        error("{0} doesn't appear to exist".format(archive))
    untar(archive)


if __name__ == '__main__':
    main()
