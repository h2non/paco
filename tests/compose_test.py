# -*- coding: utf-8 -*-
import time
import asyncio
from paco import compose, partial
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num, acc):
    yield from asyncio.sleep(0.1)
    return acc + (num,)


def test_compose():
    task = compose(partial(coro, 1), partial(coro, 2), partial(coro, 3))
    now = time.time()
    assert run_in_loop(task, (0,)) == (0, 3, 2, 1)
    assert time.time() - now >= 0.3


def test_compose_exception():
    count = 0

    @asyncio.coroutine
    def coro_exception(x):
        nonlocal count
        count += 1

        if count == 2:
            raise ValueError('foo')

        return x + 1

    task = compose(*(coro_exception,) * 5)

    try:
        run_in_loop(task, 0)
    except ValueError as err:
        pass
    else:
        raise RuntimeError('ValueError exception must be raised')

    assert count == 2
