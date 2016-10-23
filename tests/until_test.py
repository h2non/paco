# -*- coding: utf-8 -*-
import asyncio
from pyco import until
from .helpers import run_in_loop


def test_until():
    calls = 0

    @asyncio.coroutine
    def coro_test():
        return calls > 4

    @asyncio.coroutine
    def coro():
        nonlocal calls
        calls += 1
        return calls

    task = until(coro, coro_test)
    assert run_in_loop(task) == [1, 2, 3, 4, 5]


def test_until_invalid_input():
    try:
        run_in_loop(until(None, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
