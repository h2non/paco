# -*- coding: utf-8 -*-
import asyncio
from .decorator import overload
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@overload
@asyncio.coroutine
def each(coro, iterable, limit=0, loop=None,
         collect=False, timeout=None, return_exceptions=False, *args, **kw):
    """
    Concurrently iterates values yielded from an iterable, passing them to
    an asynchronous coroutine.

    You can optionally collect yielded values passing collect=True param,
    which would be equivalent to `paco.map()``.

    Mapped values will be returned as an ordered list.
    Items order is preserved based on origin iterable order.

    Concurrency level can be configurable via `limit` param.

    All coroutines will be executed in the same loop.

    This function is a coroutine.

    This function can be composed in a pipeline chain with ``|`` operator.

    Arguments:
        coro (coroutinefunction): coroutine iterator function that accepts
            iterable values.
        iterable (iterable|asynchronousiterable): an iterable collection
            yielding coroutines functions.
        limit (int): max iteration concurrency limit. Use ``0`` for no limit.
        collect (bool): return yielded values from coroutines. Default False.
        loop (asyncio.BaseEventLoop): optional event loop to use.
        return_exceptions (bool): enable/disable returning exceptions in case
            of error. `collect` param must be True.
        timeout (int|float): timeout can be used to control the maximum number
            of seconds to wait before returning. timeout can be an int or
            float. If timeout is not specified or None, there is no limit to
            the wait time.
        *args (mixed): optional variadic arguments to pass to the
            coroutine iterable function.

    Returns:
        results (list): ordered list of values yielded by coroutines

    Raises:
        TypeError: in case of invalid input arguments.

    Usage::

        async def mul_2(num):
            return num * 2

        await paco.each(mul_2, [1, 2, 3, 4, 5])
        # => None

        await paco.each(mul_2, [1, 2, 3, 4, 5], collect=True)
        # => [2, 4, 6, 8, 10]

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
    yield from pool.run(timeout=timeout, ignore_empty=True)

    # Returns list of mapped results in order
    return results
