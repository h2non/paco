# -*- coding: utf-8 -*-
import asyncio
import pytest
import paco
from paco.pipe import overload


def test_pipe_operator_overload():
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

    @asyncio.coroutine
    def task(numbers):
        return (yield from (numbers
                            | paco.filter(filterer)
                            | paco.map(mapper)
                            | paco.dropwhile(drop)
                            | paco.reduce(reducer, initializer=0)))

    result = paco.run(task((1, 2, 3, 4, 5, 6, 7, 8, 9, 10)))
    assert result == 36


def test_overload_error():
    with pytest.raises(TypeError, message='fn must be a callable object'):
        overload(None)

    with pytest.raises(ValueError,
                       messsage='invalid function signature or arity'):
        overload(lambda x: True)

    with pytest.raises(ValueError,
                       messsage='invalid function signature or arity'):
        overload(lambda x, y: True)
