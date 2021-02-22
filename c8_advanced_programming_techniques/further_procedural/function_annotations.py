import unicodedata
import inspect
import functools


def is_unicode_punctuations(s: str) -> bool:
    for c in s:
        # print(unicodedata.category(c))

        # Every Unicode character belongs to a particular category and each category is
        # identified by a two-character identifier. All the categories that begin with P are
        # punctuation characters.
        if unicodedata.category(c)[0] != 'P':
            return False
    return True


def strictly_typed(function):
    """
    # This decorator requires that every argument and the return value must be
    # annotated with the expected type.
    # Notice that the checking is done only in debug mode (which is Python’s default
    # mode —- controlled by the -O command-line option and the PYTHONOPTIMIZE environment variable).

    :param function:
    :return: decorated function
    """
    annotations = function.__annotations__
    arg_spec = inspect.getfullargspec(function)

    # assert all type is given
    assert 'return' in annotations, 'missing type for return value'
    # arg_spec.args: positional arguments
    # kwonlyargs: keyword only arguments (kwargs after position delimiter sing(*))
    for arg in arg_spec.args + arg_spec.kwonlyargs:
        assert arg in annotations, f'missing type for parameter "{arg}"'

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # argument check
        # zip() returns an iterator and dictionary.times() returns a dictionary view
        # we cannot concatenate them directly, so first we convert them both to lists.
        all_args = list(zip(arg_spec.args, args)) + list(kwargs.items())
        for name, arg in all_args:
            assert isinstance(arg, annotations[name]), (
                f'expected argument "{name}" of {annotations[name]} got {type(arg)}')

        # result check
        result = function(*args, **kwargs)
        assert isinstance(result, annotations['return']), (
            f'expected return of {annotations["return"]} got {type(result)}')

        return result

    return wrapper


@strictly_typed
def just_type(s1: str, n1: int, *, s2: str = 'a') -> bool:
    return True


def range_of_float(*args) -> 'author=Mike Chyson':
    return (float(x) for x in range(*args))


if __name__ == '__main__':
    # r = is_unicode_punctuations('!@#')
    # print(r)
    # print(is_unicode_punctuations.__annotations__)
    #
    # r = is_unicode_punctuations(['a'])
    # print(r)

    print(just_type.__annotations__)
    just_type('s1', 1, s2='2')
    # just_type(1, 2)
    # AssertionError: expected argument "s1" of <class 'str'> got <class 'int'>

    print(range_of_float.__name__)
    print(range_of_float.__annotations__)
