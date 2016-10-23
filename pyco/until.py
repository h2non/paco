# -*- coding: utf-8 -*-
import asyncio
from .whilst import whilst


@asyncio.coroutine
def until(coro, coro_test, assert_coro=None, *args, **kw):
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

        await pyco.until(coro, [1, 2, 3, 4, 5])
    """
    @asyncio.coroutine
    def assert_coro(value):
        return not value

    return (yield from whilst(coro, coro_test, assert_coro=assert_coro))
