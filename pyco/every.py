# -*- coding: utf-8 -*-
import asyncio
from .partial import partial
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@asyncio.coroutine
def every(coro, iterable, limit=0, loop=None):
    """
    Make an iterator that drops elements from the iterable as long as the
    predicate is true; afterwards, returns every element.
    Note, the iterator does not produce any output until the predicate
    first becomes false, so it may have a lengthy start-up time.

    This function implements the same interface as Python standard
    `itertools.dropwhile()` function.

    This function is a coroutine.

    All coroutines must run in the same loop.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        bool: True if all the values passes the test, otherwise False.

    Usage::

        await pyco.some(coro, [1, 2, 3, 4, 5])
    """
    assert_corofunction(coro=coro)
    assert_iter(iterable=iterable)

    # Reduced accumulator value
    passes = True

    # Handle empty iterables
    if len(iterable) == 0:
        return passes

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=limit, loop=loop)

    # Reducer partial function for deferred coroutine execution
    @asyncio.coroutine
    def tester(element):
        nonlocal passes
        if not passes:
            return None

        if not (yield from coro(element)):
            # Flag as not test passed
            passes = False
            # Force ignoring pending coroutines
            pool.cancel()

    # Iterate and attach coroutine for defer scheduling
    for element in iterable:
        pool.add(partial(tester, element))

    # Wait until all coroutines finish
    yield from pool.run()

    return passes
