import sys


def quarters(next_quarter=0.0):
    while True:
        yield next_quarter
        next_quarter += .25


result = []
for x in quarters():
    result.append(x)
    if x >= 1.0:
        break
print(result)  # [0.0, 0.25, 0.5, 0.75, 1.0]


def quarters(next_quarter=0.0):
    while True:
        received = (yield next_quarter)  # The yield expression returns each value to the caller in turn.
        # In addition, if
        # the caller calls the generator’s send() method, the value sent is received in the
        # generator function as the result of the yield expression.
        if received is None:
            next_quarter += 0.25
        else:
            next_quarter = received


result = []
generator = quarters()
while len(result) < 5:
    x = next(generator)
    if abs(x - 0.5) < sys.float_info.epsilon:
        x = generator.send(1.0)
    result.append(x)
print(result)  # [0.0, 0.25, 1.0, 1.25, 1.5]
