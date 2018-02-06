# -*- coding: utf-8 -*-
import time
import pytest
import asyncio
from paco import timeout, TimeoutLimit, run
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

    with pytest.raises(asyncio.TimeoutError):
        run_in_loop(task, delay=1)

    assert time.time() - now >= 0.2


def test_timeout_decorator():
    task = timeout(timeout=1)(coro)
    now = time.time()
    run_in_loop(task, delay=0.2)
    assert time.time() - now >= 0.2


def test_timeout_coroutine_object():
    now = time.time()

    with pytest.raises(asyncio.TimeoutError):
        @asyncio.coroutine
        def _run():
            task = timeout(coro(delay=1), timeout=0.2)
            return (yield from task)

        run(_run())

    assert time.time() - now >= 0.2


def test_timeout_limit_context():
    now = time.time()

    @asyncio.coroutine
    def test():
        with TimeoutLimit(timeout=0.2):
            yield from coro(delay=1)

    with pytest.raises(asyncio.TimeoutError):
        run(test())

    assert time.time() - now >= 0.2


def test_timeout_limit_out_of_context():
    with pytest.raises(RuntimeError, message='Timeout context manager '
                                             'should be used inside a task'):
        with TimeoutLimit(timeout=1):
            pass


def create_future(loop):
    """
    Compatibility wrapper for the loop.create_future() call
    introduced in 3.5.2.
    """
    if hasattr(loop, 'create_future'):
        return loop.create_future()
    else:
        return asyncio.Future(loop=loop)
