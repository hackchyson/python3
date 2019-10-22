from chyson.decorators.decorators import logged


@logged('/home/hack/log/logged.log')
def say_hello():
    print('hello')
    return 'hello'


if __name__ == '__main__':
    say_hello()
