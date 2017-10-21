import paco


async def filterer(x):
    return x < 8


async def mapper(x):
    return x * 2


async def drop(x):
    return x < 10


async def reducer(acc, x):
    return acc + x


async def task(numbers):
    return await (numbers
                   | paco.filter(filterer)
                   | paco.map(mapper)
                   | paco.dropwhile(drop)
                   | paco.reduce(reducer, initializer=0))


# Run in event loop
number = paco.run(task((1, 2, 3, 4, 5, 6, 7, 8, 9, 10)))
print('Number:', number) # => 36
