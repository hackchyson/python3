#!/usr/bin/env python3
"""
@project: python3
@file: findduplicates_t
@author: mike
@time: 2021/2/23
 
@function:
The program iterates over all the files in the current directory (or the specified path),
recursively going into subdirectories. It compares the lengths of all the files with the
same name, and for those files that have the same name and the same size it then uses
the MD5 (Message Digest) algorithm to check whether the files are the same, reporting
any that are.
"""

import collections
import os
import queue
import threading
import hashlib
import optparse


def main():
    # parse commandline arguments
    opts, path = parse_options()
    # prepare the data
    data = collections.defaultdict(list)
    for root, dirs, files in os.walk(path):
        for filename in files:
            fullname = os.path.join(root, filename)
            try:
                key = (os.path.getsize(fullname), filename)
            except EnvironmentError:
                continue

            if key[0] == 0:
                continue

            data[key].append(fullname)

    # Create the worker threads
    work_queue = queue.PriorityQueue()
    results_queue = queue.Queue()
    # Reduce the duplicate computation of the same file
    md5_from_filename = {}
    for i in range(opts.count):
        number = f'{i + 1}: ' if opts.debug else ''
        worker = Worker(work_queue, md5_from_filename, results_queue, number)
        worker.daemon = True
        worker.start()

    # Create the result thread
    result_thread = threading.Thread(target=lambda: print_results(results_queue))
    result_thread.daemon = True
    result_thread.start()

    for size, filename in sorted(data):
        names = data[size, filename]
        if len(names) > 1:
            work_queue.put((size, names))
        # Blocks until all items in the Queue have been gotten and processed.
        work_queue.join()
        results_queue.join()


def print_results(results_queue):
    while True:
        try:
            results = results_queue.get()
            if results:
                print(results)
        finally:
            results_queue.task_done()


class Worker(threading.Thread):
    # class attribute
    Md5_lock = threading.Lock()

    def __init__(self, work_queue, md5_from_filename, results_queue, number):
        super().__init__()
        self.work_queue = work_queue
        self.md5_from_filename = md5_from_filename
        self.results_queue = results_queue
        self.number = number

    def run(self):
        while True:
            try:
                size, names = self.work_queue.get()
                self.process(size, names)
            finally:
                self.work_queue.task_done()

    def process(self, size, filenames):
        md5s = collections.defaultdict(set)
        for filename in filenames:
            with self.Md5_lock:
                md5 = self.md5_from_filename.get(filename, None)
            if md5 is not None:
                md5s[md5].add(filename)
            else:
                try:
                    md5 = hashlib.md5()
                    with open(filename, 'rb') as fh:
                        md5.update(fh.read())
                    md5 = md5.digest()
                    md5s[md5].add(filename)
                    with self.Md5_lock:
                        self.md5_from_filename[filename] = md5
                except EnvironmentError:
                    continue

        for filenames in md5s.values():
            if len(filenames) == 1:
                continue
            self.results_queue.put(
                "{0}Duplicate files ({1:n} bytes): \n\t{2}".format(self.number, size, "\n\t".join(sorted(filenames)))
            )


def parse_options():
    parser = optparse.OptionParser(
        usage=("usage: %prog [options] [path]\n"
               "outputs a list of duplicate files in path "
               "using the MD5 algorithm\n"
               "ignores zero-length files\n"
               "path defaults to ."))
    parser.add_option("-t", "--threads", dest="count", default=7,
                      type="int",
                      help=("the number of threads to use (1..20) "
                            "[default %default]"))
    parser.add_option("-v", "--verbose", dest="verbose",
                      default=False, action="store_true")
    parser.add_option("-d", "--debug", dest="debug", default=False,
                      action="store_true")
    opts, args = parser.parse_args()
    if not (1 <= opts.count <= 20):
        parser.error("thread count must be 1..20")
    return opts, args[0] if args else "."


main()
