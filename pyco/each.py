# -*- coding: utf-8 -*-
import asyncio
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@asyncio.coroutine
def each(coro, iterable, limit=0, loop=None,
         collect=False, timeout=None, return_exceptions=False, *args, **kw):
    """
    Concurrently iterates values yielded from an iterable, passing them to
    an asynchronous coroutine.

    You can optionally collect yielded values passing collect=True param,
    which would be equivalent to .map().

    Mapped values will be returned as an ordered list.
    Items order is preserved based on origin iterable order.

    Concurrency level can be configurable via `limit` param.

    All coroutines will be executed in the same loop.

    This function is not thread safe.

    Arguments:
        iterable (iter): an iterable collection yielding
            coroutines functions. Asynchronous iterables are not supported.
        limit (int): max concurrency execution limit.
        collect (bool): return yielded values from coroutines. Default False.
        loop (asyncio.BaseEventLoop): optional event loop to use.
        timeout (int|float): timeout can be used to control the maximum number
            of seconds to wait before returning. timeout can be an int or
            float. If timeout is not specified or None, there is no limit to
            the wait time.
        *args (mixed): optional variadic argument to pass to the
            coroutines function.

    Returns:
        results (list): ordered list of values yielded by coroutines

    Usage::

        await pyco.each(pow, [1, 2, 3, 4, 5], limit=3)
    """
    assert_corofunction(coro=coro)
    assert_iter(iterable=iterable)

    # By default do not collect yielded values from coroutines
    results = None

    if collect:
        # Store ordered results
        results = [None] * len(iterable)

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=limit, loop=loop)

    @asyncio.coroutine
    def collector(index, item):
        result = yield from coro(item, *args, **kw)
        if collect:
            results[index] = result
        return result

    # Iterate and pass elements to coroutine
    for index, value in enumerate(iterable):
        pool.add(collector(index, value))

    # Wait until all the coroutines finishes
    yield from pool.run(timeout=timeout)

    # Returns list of mapped results in order
    return results
