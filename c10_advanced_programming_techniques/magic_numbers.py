import sys
import os


def load_modules():
    pass


def main():
    modules = load_modules()
    get_file_type_functions = []
    for module in modules:
        get_file_type = get_functions(module, "get_file_type")
        if get_file_type is not None:
            get_file_type_functions.append(get_file_type)

    for file in get_files(sys.argv[1:]):
        fh = None
        try:
            fh = open(file, 'rb')
            magic = fh.read(1000)
            for get_file_type in get_file_type_functions:
                filetype = get_file_type(magic, os.path.splitext(file)[1])
                if filetype is not None:
                    print('{0:.<20}{1}'.format(filetype, file))
                    break
            else:
                print('{0:.<20}{1}'.format('Unknown', file))
        except EnvironmentError as err:
            print(err)

        finally:
            if fh is not None:
                fh.close()
