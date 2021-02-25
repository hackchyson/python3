#!/usr/bin/env python3
"""
@project: python3
@file: Console
@author: mike
@time: 2021/2/23
 
@function:
"""
import sys
import datetime


class _RangeError(Exception):
    pass


def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80,
               force_lower=False):
    message += ": " if default is None else f" [{default}]: "
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError(f"{name} may not be empty")
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{0} must have at least {1} and "
                                 "at most {2} characters".format(
                    name, minimum_length, maximum_length))
            return line if not force_lower else line.lower()
        except ValueError as err:
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=None,
                maximum=None, allow_zero=True):
    message += ": " if default is None else f" [{default}]: "
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            x = int(line)
            if x == 0:
                if allow_zero:
                    return x
                else:
                    raise _RangeError(f"{name} may not be 0")
            if ((minimum is not None and minimum > x) or
                    (maximum is not None and maximum < x)):
                raise _RangeError("{0} must be between {1} and {2} "
                                  "inclusive{3}".format(name, minimum, maximum,
                                                        (" (or 0)" if allow_zero else "")))
            return x
        except _RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))


def get_float(message, name="float", default=None, minimum=None,
              maximum=None, allow_zero=True):
    message += ": " if default is None else f" [{default}]: "
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            x = float(line)
            if abs(x) < sys.float_info.epsilon:
                if allow_zero:
                    return x
                else:
                    raise _RangeError(f"{name} may not be 0.0")
            if ((minimum is not None and minimum > x) or
                    (maximum is not None and maximum < x)):
                raise _RangeError("{0} must be between {1} and {2} "
                                  "inclusive{3}".format(name, minimum, maximum,
                                                        (" (or 0.0)" if allow_zero else "")))
            return x
        except _RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be a float".format(name))


def get_bool(message, default=None):
    yes = frozenset({"1", "y", "yes", "t", "true", "ok"})
    message += " (y/yes/n/no)"
    message += ": " if default is None else f" [{default}]: "
    line = input(message)
    if not line and default is not None:
        return default in yes
    return line.lower() in yes


def get_date(message, default=None, format="%y-%m-%d"):
    # message should include the format in human-readable form, e.g.
    # for %y-%m-%d, "YY-MM-DD".
    message += ": " if default is None else f" [{default}]: "
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            return datetime.datetime.strptime(line, format)
        except ValueError as err:
            print("ERROR", err)


def get_menu_choice(message, valid, default=None, force_lower=False):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        line = input(message)
        if not line and default is not None:
            return default
        if line not in valid:
            print("ERROR only {0} are valid choices".format(
                ", ".join(["'{0}'".format(x)
                           for x in sorted(valid)])))
        else:
            return line if not force_lower else line.lower()
