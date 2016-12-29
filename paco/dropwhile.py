# -*- coding: utf-8 -*-
import asyncio
from .filter import filter
from .decorator import overload


@overload
@asyncio.coroutine
def dropwhile(coro, iterable, loop=None):
    """
    Make an iterator that drops elements from the iterable as long as the
    predicate is true; afterwards, returns every element.

    Note, the iterator does not produce any output until the predicate first
    becomes false, so it may have a lengthy start-up time.

    This function is pretty much equivalent to Python standard
    `itertools.dropwhile()`, but designed to be used with async coroutines.

    This function is a coroutine.

    This function can be composed in a pipeline chain with ``|`` operator.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable|asynchronousiterable): an iterable collection
            yielding coroutines functions.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list of resultant values.

    Usage::

        async def filter(num):
            return num < 4

        await paco.dropwhile(filter, [1, 2, 3, 4, 5, 1])
        # => [4, 5, 1]

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
