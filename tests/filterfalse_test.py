# -*- coding: utf-8 -*-
import time
import asyncio
from paco import filterfalse
from .helpers import run_in_loop


@asyncio.coroutine
def even(num):
    return num % 2 == 0


def test_filterfalse():
    task = filterfalse(even, [1, 2, 3, 4, 5, 6])
    assert run_in_loop(task) == [1, 3, 5]


def test_filterfalse_collect_sequential():
    @asyncio.coroutine
    def coro(num):
        yield from asyncio.sleep(0.1)
        return (yield from even(num))

    init = time.time()
    task = filterfalse(coro, [1, 2, 3, 4, 5, 6], limit=1)
    assert run_in_loop(task) == [1, 3, 5]
    assert time.time() - init >= 0.5


def test_filterfalse_invalid_input():
    try:
        run_in_loop(filterfalse(even, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')


def test_filterfalse_invalid_coro():
    try:
        run_in_loop(filterfalse(None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
