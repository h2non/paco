# -*- coding: utf-8 -*-
import asyncio
from .partial import partial
from .decorator import overload
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@overload
@asyncio.coroutine
def some(coro, iterable, limit=0, timeout=None, loop=None):
    """
    Returns `True` if at least one element in the iterable satisfies the
    asynchronous coroutine test. If any iteratee call returns `True`,
    iteration stops and `True` will be returned.

    This function is a coroutine.

    This function can be composed in a pipeline chain with ``|`` operator.

    Arguments:
        coro (coroutine function): coroutine function for test values.
        iterable (iterable|asynchronousiterable): an iterable collection
            yielding coroutines functions.
        limit (int): max concurrency limit. Use ``0`` for no limit.
        timeout can be used to control the maximum number
            of seconds to wait before returning. timeout can be an int or
            float. If timeout is not specified or None, there is no limit to
            the wait time.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if input arguments are not valid.

    Returns:
        bool: `True` if at least on value passes the test, otherwise `False`.

    Usage::

        async def gt_3(num):
            return num > 3

        await paco.some(test, [1, 2, 3, 4, 5])
        # => True

    """
    assert_corofunction(coro=coro)
    assert_iter(iterable=iterable)

    # Reduced accumulator value
    passes = False

    # If no items in iterable, return False
    if len(iterable) == 0:
        return passes

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=limit, loop=loop)

    # Reducer partial function for deferred coroutine execution
    @asyncio.coroutine
    def tester(element):
        nonlocal passes
        if passes:
            return None

        if (yield from coro(element)):
            # Flag as not test passed
            passes = True
            # Force stop pending coroutines
            pool.cancel()

    # Iterate and attach coroutine for defer scheduling
    for element in iterable:
        pool.add(partial(tester, element))

    # Wait until all coroutines finish
    yield from pool.run(timeout=timeout)

    return passes
