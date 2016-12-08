# -*- coding: utf-8 -*-
import asyncio
from .partial import partial
from .decorator import overload
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@overload
@asyncio.coroutine
def every(coro, iterable, limit=1, loop=None):
    """
    Returns `True` if every element in a given iterable satisfies the coroutine
    asynchronous test.

    If any iteratee coroutine call returns `False`, the process is inmediately
    stopped, and `False` will be returned.

    You can increase the concurrency limit for a fast race condition scenario.

    This function is a coroutine.

    This function can be composed in a pipeline chain with ``|`` operator.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        limit (int): max concurrency execution limit. Use ``0`` for no limit.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if input arguments are not valid.

    Returns:
        bool: `True` if all the values passes the test, otherwise `False`.

    Usage::

        async def gt_10(num):
            return num > 10

        await paco.every(gt_10, [1, 2, 3, 11])
        # => False

        await paco.every(gt_10, [11, 12, 13])
        # => True

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

    # Tester function to guarantee the file is canceled.
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
