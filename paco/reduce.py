# -*- coding: utf-8 -*-
import asyncio
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@asyncio.coroutine
def reduce(coro, iterable, right=False, initializer=None, loop=None):
    """
    Apply function of two arguments cumulatively to the items of sequence,
    from left to right, so as to reduce the sequence to a single value.

    Reduction will be executed sequentially without concurrency,
    so passed values would be in order.

    This function is the asynchronous coroutine equivalent to Python standard
    `functools.reduce()` function.

    This function is a coroutine.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        right (bool): reduce iterable from right to left.
        initializer (mixed): initial accumulator value used in
            the first reduction call.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if input arguments are not valid.

    Returns:
        mixed: accumulated final reduced value.

    Usage::

        async def reducer(acc, num):
           return acc + num

        await paco.reduce(reducer, [1, 2, 3, 4, 5], initializer=0)
        => 10
    """
    assert_corofunction(coro=coro)
    assert_iter(iterable=iterable)

    # Reduced accumulator value
    acc = initializer

    # If interable is empty, just return the initializer value
    if len(iterable) == 0:
        return initializer

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=1, loop=loop)

    # Reducer partial function for deferred coroutine execution
    def reducer(element):
        @asyncio.coroutine
        def wrapper():
            nonlocal acc
            acc = yield from coro(acc, element)
        return wrapper

    # Support right reduction
    if right:
        iterable.reverse()

    # Iterate and attach coroutine for defer scheduling
    for element in iterable:
        pool.add(reducer(element))

    # Wait until all coroutines finish
    yield from pool.run()

    # Returns final reduced value
    return acc
