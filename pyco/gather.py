# -*- coding: utf-8 -*-
import asyncio
from .utils import isiter
from .concurrent import ConcurrentExecutor, collect


@asyncio.coroutine
def gather(*coros_or_futures, limit=0, loop=None, timeout=None,
           preserve_order=False, return_exceptions=False):
    """
    Return a future aggregating results from the given coroutine objects
    with a concurrency execution limit.

    If all the tasks are done successfully, the returned future’s result is
    the list of results (in the order of the original sequence,
    not necessarily the order of results arrival).

    If return_exceptions is True, exceptions in the tasks are treated the
    same as successful results, and gathered in the result list; otherwise,
    the first raised exception will be immediately propagated to the
    returned future.

    All futures must share the same event loop.

    This functions is mostly compatible with Python standard
    ``asyncio.gather``.

    This function is a coroutine.

    Arguments:
        *coros_or_futures (iter|list):
            an iterable collection yielding coroutines functions.
        limit (int):
            concurrency execution limit. Defaults to 10.
        loop (asyncio.BaseEventLoop):
            optional event loop to use.
        *args (mixed):
            optional variadic argument to pass to the coroutines function.

    Returns:
        list: coroutines results

    Usage::

        results = await pyco.gather(
          task(1, foo='bar'),
          task(2, foo='bar'),
          task(3, foo='bar'),
          task(4, foo='bar'),
          limit=2, return_exceptions=True)
        print('Results:', results)
    """
    # If no coroutines to schedule, return empty list (as Python stdlib)
    if len(coros_or_futures) == 0:
        return []

    # Support iterable as first argument for better interoperability
    if len(coros_or_futures) == 1 and isiter(coros_or_futures[0]):
        coros_or_futures = coros_or_futures[0]

    # Pre-initialize results
    results = [None] * len(coros_or_futures) if preserve_order else []

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=limit, loop=loop)

    # Iterate and attach coroutine for defer scheduling
    for index, coro in enumerate(coros_or_futures):
        # Validate coroutine object
        if asyncio.iscoroutinefunction(coro):
            coro = coro()
        if not asyncio.iscoroutine(coro):
            raise TypeError('only coroutines or coroutine functions allowed')

        # Add coroutine to the executor pool
        pool.add(collect(coro, index, results,
                         preserve_order=preserve_order,
                         return_exceptions=return_exceptions))

    # Wait until all the tasks finishes
    yield from pool.run(timeout=timeout, return_exceptions=return_exceptions)

    # Returns aggregated results
    return results
