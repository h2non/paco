# -*- coding: utf-8 -*-
import asyncio
from .filter import filter


@asyncio.coroutine
def dropwhile(coro, iterable, loop=None):
    """
    Make an iterator that drops elements from the iterable as long as the
    predicate is true; afterwards, returns every element.
    Note, the iterator does not produce any output until the predicate
    first becomes false, so it may have a lengthy start-up time.

    This function implements the same interface as Python standard
    `itertools.dropwhile()` function.

    This function is a coroutine.

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

        await pyco.dropwhile(coro, [1, 2, 3, 4, 5])
    """
    drop = False

    @asyncio.coroutine
    def assert_fn(element):
        nonlocal drop

        if element and not drop:
            return False

        if not element and not drop:
            drop = True

        return True if drop else element

    @asyncio.coroutine
    def filter_fn(element):
        return (yield from coro(element))

    return (yield from filter(filter_fn, iterable,
                              assert_fn=assert_fn, limit=1, loop=loop))
