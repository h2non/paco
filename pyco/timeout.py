# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate


@decorate
def timeout(coro, timeout=None, loop=None):
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
        timeout (int|float): max wait timeout.
            coroutines functions.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list of resultant values.

    Usage::

        await pyco.timeout(coro, timeout=10)
    """
    @asyncio.coroutine
    def wrapper(*args, **kw):
        coro_obj = coro(*args, **kw)
        return (yield from asyncio.wait_for(coro_obj, timeout, loop=loop))

    return wrapper
