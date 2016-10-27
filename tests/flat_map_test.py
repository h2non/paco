# -*- coding: utf-8 -*-
# import time
import asyncio
from paco import flat_map
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num * 2


def test_flat_map():
    task = flat_map(coro, [1, [2, 3, 4], 5, 6, (7, [8, [(9,)]])])
    results = run_in_loop(task)
    results.sort()
    assert results == [2, 4, 6, 8, 10, 12, 14, 16, 18]


def test_flat_map_sequential():
    task = flat_map(coro, [1, [2], (3, [4]), [5]], limit=1)
    assert run_in_loop(task) == [2, 4, 6, 8, 10]


def test_flat_map_invalid_input():
    try:
        run_in_loop(flat_map(coro, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')


def test_flat_map_invalid_coro():
    try:
        run_in_loop(flat_map(None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')


def test_flat_map_pipeline():
    results = run_in_loop([1, [2], [(3, [4]), 5]] | flat_map(coro, limit=1))
    assert results == [2, 4, 6, 8, 10]
