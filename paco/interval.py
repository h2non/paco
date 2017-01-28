# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate
from .assertions import assert_corofunction


@decorate
def interval(coro, interval=1, times=None):
    """
    Schedules the execution of a coroutine function every `x` amount of
    seconds.

    The function returns an `asyncio.Task`, which implements also an
    `asyncio.Future` interface, allowing the user to cancel the execution
    cycle.

    This function can be used as decorator.

    Arguments:
        coro (coroutinefunction): coroutine function to defer.
        interval (int/float): number of seconds to repeat the coroutine
            execution.
        times (int): optional maximum time of executions. Infinite by default.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        future (asyncio.Task): coroutine wrapped as task future.
            Useful for cancellation and state checking.

    Usage::

        # Usage as function
        future = paco.interval(coro, 1)

        # Cancel it after a while...
        await asyncio.sleep(5)
        future.cancel()

        # Usage as decorator
        @paco.interval(10)
        async def metrics():
            await send_metrics()

        future = await metrics()

    """
    assert_corofunction(coro=coro)

    # Store maximum allowed number of calls
    times = int(times or 0) or float('inf')

    @asyncio.coroutine
    def schedule(times, *args, **kw):
        while times > 0:
            # Decrement times counter
            times -= 1

            # Schedule coroutine
            yield from coro(*args, **kw)
            yield from asyncio.sleep(interval)

    def wrapper(*args, **kw):
        return asyncio.ensure_future(schedule(times, *args, **kw))

    return wrapper
