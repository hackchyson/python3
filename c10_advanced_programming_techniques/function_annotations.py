import unicodedata
import inspect
import functools


# Annotations have no special significance to Python.
# The only thing that Python does in the face of annotations is
# to put them in the __annotations__ dictionary; any other action is up to us.
def is_unicode_punctuations(s: str) -> bool:
    for c in s:
        # print(unicodedata.category(c))

        # Every Unicode character belongs to a particular category and each category is
        # identified by a two-character identifier. All the categories that begin with P are
        # punctuation characters.
        if unicodedata.category(c)[0] != 'P':
            return False
    return True


# If we want to give meaning to annotations, for example, to provide type checking,
# one approach is to decorate the functions we want the meaning to apply to
# with a suitable decorator.
def strictly_typed(function):
    """
    # This decorator requires that every argument and the return value must be
    # annotated with the expected type.
    # Notice that the checking is done only in debug mode (which is Python’s default
    # mode—controlled by the -O command-line option and the PYTHONOPTIMIZE environment variable).

    :param function:
    :return:
    """
    annotations = function.__annotations__
    arg_spec = inspect.getfullargspec(function)

    # assert all type is given
    assert 'return' in annotations, 'missing type for return value'
    for arg in arg_spec.args + arg_spec.kwonlyargs:  # keyword only args
        assert arg in annotations, 'missing type for parameter "{}"'.format(arg)

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # argument check
        # zip() returns an iterator and dictionary.times() returns a dictionary view
        # we cannot concatenate them directly, so first we convert them both to lists.
        all_args = list(zip(arg_spec.args, args)) + list(kwargs.items())
        for name, arg in all_args:
            assert isinstance(arg, annotations[name]), (  # the () protect the format
                'expected argument "{}" of {} get {}'.format(name, annotations[name], type(arg)))

        # result check
        result = function(*args, **kwargs)
        assert isinstance(result, annotations['return']), (
            'expected return of {} got {}'.format(annotations['return'], type(result)))

        return result

    return wrapper


@strictly_typed
def is_unicode_punctuations2(s: str, a: int, b: str = 'a') -> bool:
    return True


def range_from_one(*args) -> 'author=Hack Chyson':
    return (x + 1 for x in range(*args))


if __name__ == '__main__':
    r = is_unicode_punctuations('!@#')
    print(r)
    print(is_unicode_punctuations.__annotations__)

    r = is_unicode_punctuations(['a'])
    print(r)

    r = is_unicode_punctuations2('!@#', 1)
    print(r)

    # r = is_unicode_punctuations2(['a'], 1)
    # AssertionError: expected argument "s" of <class 'str'> get <class 'list'>

    print(range_from_one.__name__)
    print(range_from_one.__annotations__)
