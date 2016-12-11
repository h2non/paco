# -*- coding: utf-8 -*-
import time
import pytest
import asyncio
from paco import filter
from .helpers import run_in_loop


@asyncio.coroutine
def even(num):
    return num % 2 == 0


def test_filter():
    task = filter(even, [1, 2, 3, 4, 5, 6])
    assert run_in_loop(task) == [2, 4, 6]


def test_filter_collect_sequential():
    @asyncio.coroutine
    def coro(num):
        yield from asyncio.sleep(0.1)
        return (yield from even(num))

    init = time.time()
    task = filter(coro, [1, 2, 3, 4, 5, 6], limit=1)
    assert run_in_loop(task) == [2, 4, 6]
    assert time.time() - init >= 0.5


def test_filter_empty():
    assert run_in_loop(filter(even, [])) == []


def test_filter_invalid_input():
    with pytest.raises(TypeError):
        run_in_loop(filter(even, None))


def test_filter_invalid_coro():
    with pytest.raises(TypeError):
        run_in_loop(filter(None))
