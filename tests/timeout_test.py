# -*- coding: utf-8 -*-
import time
import asyncio
from paco import timeout
from .helpers import run_in_loop

try:
    from asyncio import ensure_future
except ImportError:
    ensure_future = asyncio.async


@asyncio.coroutine
def coro(delay=1):
    yield from asyncio.sleep(delay)


def test_timeout():
    task = timeout(coro, timeout=1)
    now = time.time()
    run_in_loop(task, delay=0.2)
    assert time.time() - now >= 0.2


def test_timeout_exceeded():
    task = timeout(coro, timeout=0.2)
    now = time.time()
    try:
        run_in_loop(task, delay=1)
    except asyncio.TimeoutError as err:
        pass
    else:
        raise RuntimeError('must raise timeout exception')
    assert time.time() - now >= 0.2


def test_timeout_decorator():
    task = timeout(timeout=1)(coro)
    now = time.time()
    run_in_loop(task, delay=0.2)
    assert time.time() - now >= 0.2


def create_future(loop):
    """
    Compatibility wrapper for the loop.create_future() call
    introduced in 3.5.2.
    """
    if hasattr(loop, 'create_future'):
        return loop.create_future()
    else:
        return asyncio.Future(loop=loop)
