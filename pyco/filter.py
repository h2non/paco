# -*- coding: utf-8 -*-
import asyncio
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@asyncio.coroutine
def assert_true(element):
    """
    Asserts that a given coroutine yields a true-like value.
    """
    return element


@asyncio.coroutine
def filter(coro, iterable, assert_fn=None, limit=0, loop=None):
    """
    Construct an iterator from those elements of iterable for which function
    returns true. iterable may be either a sequence, a container which supports
    iteration, or an iterator.

    Since reduction concurrency can be enable, there is no guarantees
    that passed values to the reducer function would be in order.

    This function implements the same interface as Python standard
    `filter()` function.

    All coroutines will be executed in the same loop.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        assert_fn (coroutine function): optional assertion function.
        limit (int): reduction concurrency limit. Use ``0`` for no limit.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list containing values that passed
            the filter.

    Usage::

        await pyco.filter(coro, [1, 2, 3, 4, 5], limit=2)
    """
    assert_corofunction(coro=coro)
    assert_iter(iterable=iterable)

    # Check valid or empty iterable
    if len(iterable) == 0:
        return iterable

    # Reduced accumulator value
    results = [None] * len(iterable)

    # Use a custom or default filter assertion function
    assert_fn = assert_fn or assert_true

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=limit, loop=loop)

    # Reducer partial function for deferred coroutine execution
    def filterer(index, element):
        @asyncio.coroutine
        def wrapper():
            result = yield from coro(element)
            if (yield from assert_fn(result)):
                results[index] = element
        return wrapper

    # Iterate and attach coroutine for defer scheduling
    for index, element in enumerate(iterable):
        pool.add(filterer(index, element))

    # Wait until all coroutines finish
    yield from pool.run()

    # Returns filtered elements
    return [x for x in results if x is not None]
