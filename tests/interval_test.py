# -*- coding: utf-8 -*-
import time
import pytest
import asyncio
from paco import interval
from .helpers import run_in_loop


@asyncio.coroutine
def coro(track):
    track['calls'] += 1


def test_interval():
    track = {'calls': 0}
    start = time.time()

    task = interval(coro, .1, 5)
    future = task(track)

    run_in_loop(future)

    assert future.cancelled
    assert track['calls'] == 5
    assert time.time() - start > .4


def test_interval_cancellation():
    track = {'calls': 0}
    start = time.time()

    task = interval(coro, .1)
    future = task(track)

    def cancel():
        future.cancel()

    @asyncio.coroutine
    def runner(loop):
        loop.call_later(1, cancel)
        try:
            yield from future
        except asyncio.CancelledError:
            pass

    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner(loop))

    assert future.cancelled
    assert track['calls'] > 9
    assert time.time() - start > .9


def test_interval_decorator():
    track = {'calls': 0}
    start = time.time()

    task = interval(.1, 3)(coro)
    future = task(track)

    run_in_loop(future)

    assert future.cancelled
    assert track['calls'] == 3
    assert time.time() - start > .2


def test_interval_invalid_input():
    with pytest.raises(TypeError):
        run_in_loop(interval(None))

    with pytest.raises(TypeError):
        run_in_loop(interval(lambda x: x))
