# -*- coding: utf-8 -*-
import time
import asyncio
from paco import series
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    yield from asyncio.sleep(0.1)
    return num * 2


def test_series():
    init = time.time()
    task = series(coro(1), coro(2), coro(3))
    assert run_in_loop(task) == [2, 4, 6]
    assert time.time() - init >= 0.3


def test_series_return_exceptions():
    @asyncio.coroutine
    def coro(num):
        raise ValueError('foo')

    task = series(coro(1), coro(2), coro(3), return_exceptions=True)
    results = run_in_loop(task)
    assert len(results) == 3

    for err in results:
        assert str(err) == 'foo'
