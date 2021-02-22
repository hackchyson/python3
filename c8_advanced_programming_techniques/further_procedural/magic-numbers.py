#!/usr/bin/env python3
"""
@project: python3
@file: magic-numbers
@author: mike
@time: 2021/2/7
 
@function:
This program reads the first 1 000 bytes of each file given on the command line and
for each one outputs the file’s type (or the text “Unknown”), and the filename.
"""

import sys
import os
import glob


def main():
    modules = load_modules()
    get_file_type_functions = []
    for module in modules:
        get_file_type = get_function(module, 'get_file_type')
        if get_file_type is None:
            get_file_type_functions.append(get_file_type)

    for file in get_files(sys.argv[1:]):
        fh = None
        try:
            fh = open(file, 'rb')
            magic = fh.read(1000)
            for get_file_type in get_file_type_functions:
                filetype = get_file_type(magic, os.path.splitext(file)[1])  # file extension
                if filetype is not None:
                    print(f'{filetype:.<20}{file}')
                    break
            else:
                print('{:.<20}{}'.format('Unknown', file))
        except EnvironmentError as err:
            print(err)
        finally:
            if fh is not None:
                fh.close()


if sys.platform.startswith("win"):
    def get_files(names):
        for name in names:
            if os.path.isfile(name):
                yield name
            else:
                for file in glob.iglob(name):
                    if not os.path.isfile(file):
                        continue
                    yield file
else:
    def get_files(names):
        return (file for file in names if os.path.isfile(file))


def load_modules():
    modules = []
    # __file__ is the current file name
    for name in os.listdir(os.path.dirname(__file__) or '.'):
        if name.endswith('.py') and 'magic' in name.lower():
            filename = name
            name = os.path.splitext(name)[0]  # remove extension
            if name.isidentifier() and name not in sys.modules:
                # approach 1
                # fh = None
                # try:
                #     fh = open(filename)
                #     code = fh.read()
                #     module = type(sys)(name)
                #     sys.modules[name] = module
                #     exec(code, module.__dict__)  # __dict__ to provide module reference
                #     modules.append(module)
                # except (EnvironmentError, SyntaxError) as err:
                #     sys.modules.pop(name, None)
                #     print(err)
                # finally:
                #     if fh is not None:
                #         fh.close()

                # approach 2
                # try:
                #     exec('import ' + name)
                #     modules.append(sys.modules[name])
                # except SyntaxError as err:
                #     print(err)

                # approach 3
                try:
                    module = __import__(name)
                    modules.append(module)
                except SyntaxError as err:
                    print(err)
    return modules


def get_function(module, function_name):
    function = get_function.cache.get((module, function_name), None)
    if function is None:
        try:
            function = getattr(module, function_name)
            if not hasattr(function, '__call__'):
                raise AttributeError()
            get_function.cache[(module, function_name)] = function
        except AttributeError:
            function = None
    return function


if __name__ == '__main__':
    main()
