# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate


@decorate
def defer(coro, seconds=None):
    """
    Make an iterator that drops elements from the iterable as long as the
    predicate is true; afterwards, returns every element.
    Note, the iterator does not produce any output until the predicate
    first becomes false, so it may have a lengthy start-up time.

    This function implements the same interface as Python standard
    `itertools.dropwhile()` function.

    All coroutines will be executed in the same loop.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list of resultant values.

    Usage::

        await pyco.defer(coro, 1)
        await pyco.defer(coro, 0.5)

        @pyco.defer(seconds=1)
        async def task(n):
            return n * n
        await task(2)
        => 4
    """
    @asyncio.coroutine
    def wrapper(*args, **kw):
        # Wait until we're done
        yield from asyncio.sleep(seconds)
        return (yield from coro(*args, **kw))

    return wrapper
