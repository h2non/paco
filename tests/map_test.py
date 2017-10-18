# -*- coding: utf-8 -*-
import time
import pytest
import asyncio
from paco import map
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num * 2


def test_map():
    task = map(coro, [1, 2, 3, 4, 5])
    assert run_in_loop(task) == [2, 4, 6, 8, 10]


def test_map_sequential():
    @asyncio.coroutine
    def _coro(num):
        yield from asyncio.sleep(0.1)
        return (yield from coro(num))

    init = time.time()
    task = map(_coro, [1, 2, 3, 4, 5], limit=1)
    assert run_in_loop(task) == [2, 4, 6, 8, 10]
    assert time.time() - init >= 0.5


def test_map_empty():
    assert run_in_loop(map(coro, [])) == []


def test_map_invalid_input():
    with pytest.raises(TypeError):
        run_in_loop(map(coro, None))


def test_map_invalid_coro():
    with pytest.raises(TypeError):
        run_in_loop(map(None))


def test_map_exceptions():
    @asyncio.coroutine
    def coro(num):
        raise ValueError('foo')

    task = map(coro, [1, 2, 3, 4, 5], return_exceptions=True)
    for exp in run_in_loop(task):
        assert isinstance(exp, ValueError)


def test_map_return_exceptions():
    @asyncio.coroutine
    def coro(num):
        raise ValueError('foo')

    task = map(coro, [1, 2, 3, 4, 5], return_exceptions=True)
    results = run_in_loop(task)
    assert len(results) == 5

    for err in results:
        assert str(err) == 'foo'
