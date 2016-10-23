# -*- coding: utf-8 -*-
import asyncio
from .assertions import assert_corofunction
from .map import map


@asyncio.coroutine
def repeat(coro, times=1, step=1, limit=1, loop=None):
    """
    Executes the coroutine function ``x`` number of  times,
    and accumulates results in order as you would use with ``map``.

    Execution concurrency is configurable using ``limit`` param.

    This function is a coroutine.

    Arguments:
        coro (coroutinefunction): coroutine function to schedule.
        times (int): number of times to execute the coroutine.
        step (int): increment iteration step, as with ``range()``.
        limit (int): concurrency execution limit. Defaults to 10.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro is not a coroutine function.

    Returns:
        list: accumulated yielded values returned by coroutine.

    Usage::

        async def task(num):
            return num * 2

        await pyco.times(task, 10, limit=2)
        => [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    """
    assert_corofunction(coro=coro)

    # Iterate and attach coroutine for defer scheduling
    times = max(int(times), 1)
    iterable = range(1, times + 1, step)

    # Run iterable times
    return (yield from map(coro, iterable, limit=limit, loop=loop))
