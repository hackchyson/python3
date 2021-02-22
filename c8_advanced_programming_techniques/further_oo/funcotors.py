import operator


class Strip:
    def __init__(self, characters):
        self.characters = characters

    def __call__(self, string):
        return string.strip(self.characters)


# A closure is a function or method that captures some external state.
# make_strip_function is a closure
def make_strip_function(characters):
    def strip_function(string):
        return string.strip(characters)

    return strip_function


class SortedKey:
    def __init__(self, *attribute_names):  # variable length parameters
        self.attribute_names = attribute_names

    def __call__(self, instance):
        values = []
        for attribute_name in self.attribute_names:
            #     getattr(object, name[, default]) -> value
            #
            #     Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
            #     When a default argument is given, it is returned when the attribute doesn't
            #     exist; without it, an exception is raised in that case.
            values.append(getattr(instance, attribute_name))
        return values


class Person:
    def __init__(self, forename, surname, email):
        self.forename = forename
        self.surname = surname
        self.email = email

    def __str__(self):
        return 'Person({}, {}, {})'.format(self.forename, self.surname, self.email)


# if __name__ == '__main__':
# We could achieve the same thing using a plain function or lambda, but if we
# need to store a bit more state or perform more complex processing, a functor is
# often the right solution.
strip_punctuation = Strip(',;:.!?')
print(strip_punctuation('Mike Chyson!'))  # Mike Chyson

strip_punctuation = make_strip_function(',;:.!?')
print(strip_punctuation('Mike Chyson!'))  # Mike Chyson

people = []
people.append(Person('Hack', 'Chyson', 'chyson@aliyun.com'))
people.append(Person('A', 'B', 'c@d.com'))
people.sort(key=SortedKey('surname', 'forename'))  # in sort method, the person object is passed as the instance
for i in people:
    print(i)

# this can be achieved with operator module without creating a class
people.sort(key=operator.attrgetter('surname', 'forename'))


