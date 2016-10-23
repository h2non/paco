# -*- coding: utf-8 -*-
import time
import asyncio
from pyco import wait
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    yield from asyncio.sleep(0.1)
    return num * 2


def test_wait(limit=0):
    done, pending = run_in_loop(wait([coro(1), coro(2), coro(3)], limit=limit))
    assert len(done) == 3
    assert len(pending) == 0

    for future in done:
        assert future.result() < 7


def test_wait_sequential():
    start = time.time()
    test_wait(limit=1)
    assert time.time() - start >= 0.3


def test_wait_return_exceptions():
    @asyncio.coroutine
    def coro(num):
        raise ValueError('foo')

    done, pending = run_in_loop(wait([coro(1), coro(2), coro(3)],
                                return_exceptions=True))
    assert len(done) == 3
    assert len(pending) == 0

    for future in done:
        assert str(future.result()) == 'foo'
