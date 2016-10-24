# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate
from .assertions import assert_corofunction


@decorate
def defer(coro, delay=1):
    """
    Returns a coroutine function wrapper that will defer the given coroutine
    execution for a certain amount of seconds in a non-blocking way.

    This function can be used as decorator.

    Arguments:
        coro (coroutinefunction): coroutine function to defer.
        delay (int/float): number of seconds to defer execution.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list of resultant values.

    Usage::

        # Usage as function
        await paco.defer(coro, 1)
        await paco.defer(coro, 0.5)

        # Usage as decorator
        @paco.defer(delay=1)
        async def task(n):
            return n * n
        await task(2)
        => 4
    """
    assert_corofunction(coro=coro)

    @asyncio.coroutine
    def wrapper(*args, **kw):
        # Wait until we're done
        yield from asyncio.sleep(delay)
        return (yield from coro(*args, **kw))

    return wrapper
