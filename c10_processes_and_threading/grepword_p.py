#!/usr/bin/env python3
"""
@project: python3
@file: grepword_p
@author: mike
@time: 2021/2/22
 
@function:
Searches for a word specified on the command line in the files listed after the word.
This the parent program.
The corresponding child program is grepword_p_child.py.
"""
import os
import sys
import subprocess
import optparse


def main():
    child = os.path.join(os.path.dirname(__file__), 'grepword_p_child.py')
    opts, word, args = parse_options()
    filelist = get_files(args, opts.recurse)
    files_per_process = len(filelist) // opts.count
    # Usually the number of files won’t be an exact multiple of the number of processes,
    # so we increase the number of files the first process is given by the remainder.
    start, end = 0, files_per_process + (len(filelist) % opts.count)
    number = 1

    pipes = []
    while start < len(filelist):
        command = [sys.executable, child]
        if opts.debug:
            command.append(str(number))
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
        pipes.append(pipe)
        pipe.stdin.write(word.encode('utf8') + b'\n')
        for filename in filelist[start:end]:
            pipe.stdin.write(filename.encode('utf8') + b'\n')
        pipe.stdin.close()
        number += 1
        start, end = end, end + files_per_process

    while pipes:
        pipe = pipes.pop()
        pipe.wait()


def parse_options():
    parser = optparse.OptionParser(
        usage=("usage: %prog [options] word name1 "
               "[name2 [... nameN]]\n\n"
               "names are filenames or paths; paths only "
               "make sense with the -r option set"))
    parser.add_option("-p", "--processes", dest="count", default=7,
                      type="int",
                      help=("the number of child processes to use (1..20) "
                            "[default %default]"))
    parser.add_option("-r", "--recurse", dest="recurse",
                      default=False, action="store_true",
                      help="recurse into subdirectories")
    parser.add_option("-d", "--debug", dest="debug", default=False,
                      action="store_true")
    opts, args = parser.parse_args()
    if len(args) == 0:
        parser.error("a word and at least one path must be specified")
    elif len(args) == 1:
        parser.error("at least one path must be specified")
    if (not opts.recurse and
            not any([os.path.isfile(arg) for arg in args])):
        parser.error("at least one file must be specified; or use -r")
    if not (1 <= opts.count <= 20):
        parser.error("process count must be 1..20")
    return opts, args[0], args[1:]


def get_files(args, recurse):
    filelist = []
    for path in args:
        if os.path.isfile(path):
            filelist.append(path)
        elif recurse:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    filelist.append(os.path.join(root, filename))
    return filelist


main()
