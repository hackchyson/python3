# from c10_advanced_programming_techniques.decorators_ import logged
# import logging
#
# logging.basicConfig(level=logging.INFO)
#
#
# @logged
# def hello(x):
#     return x
#
#
# if __name__ == '__main__':
#     hello(10)
#
# from c10_advanced_programming_techniques.function_annotations import range_from_one

import sys
from chyson.os.magic.magic_file_type import get_file_types

get_file_types(sys.argv[1:])
