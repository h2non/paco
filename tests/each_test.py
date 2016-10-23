# -*- coding: utf-8 -*-
import time
import asyncio
from pyco import each
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num


def test_each():
    calls = 0

    @asyncio.coroutine
    def coro(num):
        nonlocal calls
        calls += 1

    task = each(coro, [1, 2, 3, 4, 5])
    assert run_in_loop(task) is None
    assert calls == 5


def test_each_collect():
    task = each(coro, [1, 2, 3, 4, 5], collect=True)
    assert run_in_loop(task) == [1, 2, 3, 4, 5]


def test_each_collect_sequential():
    @asyncio.coroutine
    def coro(num):
        yield from asyncio.sleep(0.1)
        return num

    init = time.time()
    task = each(coro, [1, 2, 3, 4, 5], limit=1)
    assert run_in_loop(task) is None
    assert time.time() - init >= 0.5


def test_each_exception():
    @asyncio.coroutine
    def coro(num):
        yield from asyncio.sleep(0.1)
        if num == 4:
            raise ValueError('foo')
        return num

    init = time.time()
    task = each(coro, [1, 2, 3, 4, 5], limit=1)
    try:
        run_in_loop(task)
    except ValueError:
        pass
    else:
        raise RuntimeError('must raise exception')

    assert time.time() - init >= 0.3


def test_each_invalid_input():
    try:
        run_in_loop(each(coro, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')


def test_each_invalid_coro():
    try:
        run_in_loop(each(None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
