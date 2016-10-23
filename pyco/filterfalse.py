# -*- coding: utf-8 -*-
import asyncio
from .filter import filter


@asyncio.coroutine
def assert_false(element):
    """
    Asserts that a given coroutine yields a non-true value.
    """
    return not element


@asyncio.coroutine
def filterfalse(coro, iterable, limit=0, loop=None):
    """
    Construct an iterator from those elements of iterable for which function
    returns true. iterable may be either a sequence, a container which supports
    iteration, or an iterator.

    Since reduction concurrency can be enable, there is no guarantees
    that passed values to the reducer function would be in order.

    All coroutines will be executed in the same loop.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        limit (int): reduction concurrency limit. Defaults to 10.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list containing values that do not
            passed the filter.

    Usage::

        await pyco.filterfalse(coro, [1, 2, 3, 4, 5], limit=3)
    """
    return (yield from filter(coro, iterable,
                              assert_fn=assert_false,
                              limit=limit, loop=loop))
