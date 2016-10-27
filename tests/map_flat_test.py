# -*- coding: utf-8 -*-
# import time
import asyncio
from paco import map_flat
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num * 2


def test_map_flat():
    task = map_flat(coro, [1, [2, 3, 4], 5, 6, (7, [8, [(9,)]])])
    results = run_in_loop(task)
    results.sort()
    assert results == [2, 4, 6, 8, 10, 12, 14, 16, 18]


def test_map_flat_sequential():
    task = map_flat(coro, [1, [2], (3, [4]), [5]], limit=1)
    assert run_in_loop(task) == [2, 4, 6, 8, 10]


def test_map_flat_invalid_input():
    try:
        run_in_loop(map_flat(coro, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')


def test_map_flat_invalid_coro():
    try:
        run_in_loop(map_flat(None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')


def test_map_flat_pipeline():
    results = run_in_loop([1, [2], [(3, [4]), 5]] | map_flat(coro, limit=1))
    assert results == [2, 4, 6, 8, 10]
