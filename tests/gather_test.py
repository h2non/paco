# -*- coding: utf-8 -*-
import time
import asyncio
from paco import gather, partial
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    yield from asyncio.sleep(0.1)
    return num * 2


def test_gather():
    results = run_in_loop(gather(coro(1), coro(2), coro(3),
                                 preserve_order=True))
    assert results == [2, 4, 6]

    # Test array first argument
    results = run_in_loop(gather([coro(1), coro(2), coro(3)],
                                 preserve_order=True))
    assert results == [2, 4, 6]


def test_gather_sequential():
    start = time.time()
    results = run_in_loop(gather(coro(1), coro(2), coro(3), limit=1))
    assert results == [2, 4, 6]
    assert time.time() - start >= 0.3


def test_gather_empty():
    results = run_in_loop(gather(limit=1))
    assert results == []


def test_gather_coroutinefunction():
    results = run_in_loop(gather(partial(coro, 1), partial(coro, 2), limit=1))
    assert results == [2, 4]


def test_gather_invalid_coro():
    try:
        run_in_loop(None)
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')


def test_gather_return_exceptions():
    @asyncio.coroutine
    def coro(num):
        if num == 2:
            raise ValueError('foo')
        return num * 2

    results = run_in_loop(gather(coro(1), coro(2), coro(3),
                                 return_exceptions=True, preserve_order=True))
    assert results == [2, results[1], 6]


def test_gather_no_order():
    start = time.time()
    results = run_in_loop(gather(coro(1), coro(2), coro(3)))
    assert 2 in results
    assert 4 in results
    assert 6 in results
    assert len(results) == 3
    assert time.time() - start < 0.3
