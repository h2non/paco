# -*- coding: utf-8 -*-
import sys
import pytest
import asyncio
import paco
from paco.pipe import overload


@asyncio.coroutine
def filterer(x):
    return x < 8


@asyncio.coroutine
def mapper(x):
    return x * 2


@asyncio.coroutine
def drop(x):
    return x < 10


@asyncio.coroutine
def reducer(acc, x):
    return acc + x


def test_pipe_operator_overload():
    @asyncio.coroutine
    def task(numbers):
        return (yield from (numbers
                            | paco.filter(filterer)
                            | paco.map(mapper)
                            | paco.dropwhile(drop)
                            | paco.reduce(reducer, initializer=0)))

    result = paco.run(task((1, 2, 3, 4, 5, 6, 7, 8, 9, 10)))
    assert result == 36


@pytest.mark.skipif(sys.version_info < (3, 5), reason='requires Python 3.5+')
def test_pipe_async_generator():
    class AsyncGenerator(object):
        def __init__(self, values=None):
            self.pos = 0
            self.values = values or [1, 2, 3]

        @asyncio.coroutine
        def __aiter__(self):
            self.pos = 0
            return self

        @asyncio.coroutine
        def __anext__(self):
            if self.pos == len(self.values):
                raise StopAsyncIteration  # noqa

            value = self.values[self.pos]
            self.pos += 1
            return value

    @asyncio.coroutine
    def task(numbers):
        return (yield from (AsyncGenerator(numbers)
                            | paco.map(mapper)
                            | paco.reduce(reducer, initializer=0)))

    result = paco.run(task([1, 2, 3, 4, 5]))
    assert result == 30


def test_overload_error():
    with pytest.raises(TypeError, message='fn must be a callable object'):
        overload(None)

    with pytest.raises(ValueError,
                       messsage='invalid function signature or arity'):
        overload(lambda x: True)

    with pytest.raises(ValueError,
                       messsage='invalid function signature or arity'):
        overload(lambda x, y: True)
