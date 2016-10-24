# -*- coding: utf-8 -*-
import asyncio
from paco import repeat
from .helpers import run_in_loop


def test_repeat():
    calls = 0

    @asyncio.coroutine
    def coro(num):
        nonlocal calls
        calls += 1
        return num * 2

    assert run_in_loop(repeat(coro, 5)) == [2, 4, 6, 8, 10]
    assert calls == 5


def test_repeat_defaults():
    @asyncio.coroutine
    def coro(num):
        return num * 2

    assert run_in_loop(repeat(coro)) == [2]


def test_repeat_concurrency():
    @asyncio.coroutine
    def coro(num):
        return num * 2

    assert run_in_loop(repeat(coro, 5), limit=5) == [2, 4, 6, 8, 10]


def test_repeat_invalid_input():
    try:
        run_in_loop(repeat(None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
