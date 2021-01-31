# coding=utf8
"""
@project: python3
@file: statistics
@author: mike
@time: 2021/1/31
 
@function:
"""
import collections
import sys
import math

# a simper way to class
# mode: most frequently occurring
Statistics = collections.namedtuple('Statistics', 'mean mode median std_dev')


def main():
    # commandline part
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        print('usage: {} file1 [file2 [... fileN]]'.format(sys.argv[0]))
        sys.exit(1)

    numbers = []
    frequencies = collections.defaultdict(int)

    for filename in sys.argv[1:]:
        # function to read data
        read_data(filename, numbers, frequencies)
    if numbers:
        # function to calculate statistics
        statistics = calculate_statistics(numbers, frequencies)
        # function to print
        print_result(len(numbers), statistics)
    else:
        print('no numbers found')


def read_data(filename, numbers, frequencies):
    for lino, line in enumerate(open(filename), start=1):
        for x in line.split():
            try:
                number = float(x)
                numbers.append(number)
                frequencies[number] += 1
            except ValueError as err:
                print('{filename}:{lino}: skipping{x}: {err}'.format(**locals()))


# learn programming manner
def calculate_statistics(numbers, frequencies):
    mean = sum(numbers) / len(numbers)
    mode = calculate_mode(frequencies, 3)
    median = calculate_median(numbers)
    std_dev = calculate_std_dev(numbers, mean)
    return Statistics(mean, mode, median, std_dev)


def calculate_mode(frequencies, maximum_modes):
    """
    Calculate the most frequently occurring numbers.

    :param frequencies: a dict containing number and frequencies
    :param maximum_modes: the count of different numbers with the most frequency
    :return:
    """
    highest_frequency = max(frequencies.values())
    mode = [number for number, frequency in frequencies.items() if frequency == highest_frequency]
    # if there are 0 or greater than the maximum mode
    if not (1 <= len(mode) <= maximum_modes):
        mode = None
    else:
        mode.sort()
    return mode


def calculate_median(numbers):
    numbers = sorted(numbers)
    middle = len(numbers) // 2
    median = numbers[middle]
    # define and change thought
    if len(numbers) % 2 == 0:
        median = (median + numbers[middle - 1]) / 2
    return median


def calculate_std_dev(numbers, mean):
    total = 0
    for number in numbers:
        total += ((number - mean) ** 2)
    variance = total / (len(numbers) - 1)
    return math.sqrt(variance)


def print_result(count, statistics):
    fmt = '9.2f'

    if statistics.mode is None:
        modeline = ''
    elif len(statistics.mode) == 1:
        modeline = 'mode         = {:{fmt}}\n'.format(statistics.mode[0], **locals())
    else:
        modeline = 'mode         = [' + ', '.join(['{:.2f}'.format(m) for m in statistics.mode]) + ']\n'

    # The backslash escapes the newline,
    # so if the mode is the empty string no blank line will appear.
    print("""\
count        = {0:6}
mean         = {mean:{fmt}}
median       = {median:{fmt}}
{1}\
std. dev.    = {std_dev: {fmt}}"""
          .format(count, modeline, **locals(), **statistics._asdict()))


if __name__ == '__main__':
    main()
