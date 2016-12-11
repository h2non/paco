# -*- coding: utf-8 -*-
import asyncio
from .assertions import isiter
from .concurrent import ConcurrentExecutor


@asyncio.coroutine
def wait(*coros_or_futures, limit=0, timeout=None, loop=None,
         return_exceptions=False, return_when='ALL_COMPLETED'):
    """
    Wait for the Futures and coroutine objects given by the sequence
    futures to complete, with optional concurrency limit.
    Coroutines will be wrapped in Tasks.

    ``timeout`` can be used to control the maximum number of seconds to
    wait before returning. timeout can be an int or float.
    If timeout is not specified or None, there is no limit to the wait time.

    If ``return_exceptions`` is True, exceptions in the tasks are treated the
    same as successful results, and gathered in the result list; otherwise,
    the first raised exception will be immediately propagated to the
    returned future.

    ``return_when`` indicates when this function should return.
    It must be one of the following constants of the concurrent.futures module.

    All futures must share the same event loop.

    This functions is mostly compatible with Python standard
    ``asyncio.wait()``.

    Arguments:
        *coros_or_futures (iter|list):
            an iterable collection yielding coroutines functions.
        limit (int):
            optional concurrency execution limit. Use ``0`` for no limit.
        timeout (int/float):
            maximum number of seconds to wait before returning.
        return_exceptions (bool):
            exceptions in the tasks are treated the same as successful results,
            instead of raising them.
        return_when (str):
            indicates when this function should return.
        loop (asyncio.BaseEventLoop):
            optional event loop to use.
        *args (mixed):
            optional variadic argument to pass to the coroutines function.

    Returns:
        tuple: Returns two sets of Future: (done, pending).

    Raises:
        TypeError: in case of invalid coroutine object.
        ValueError: in case of empty set of coroutines or futures.
        TimeoutError: if execution takes more than expected.

    Usage::

        async def sum(x, y):
            return x + y

        done, pending = await paco.wait(
            sum(1, 2),
            sum(3, 4))
        [task.result() for task in done]
        # => [3, 7]
    """
    # Support iterable as first argument for better interoperability
    if len(coros_or_futures) == 1 and isiter(coros_or_futures[0]):
        coros_or_futures = coros_or_futures[0]

    # If no coroutines to schedule, return empty list
    # Mimics asyncio behaviour.
    if len(coros_or_futures) == 0:
        raise ValueError('Set of coroutines/Futures is empty.')

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=limit, loop=loop,
                              coros=coros_or_futures)

    # Wait until all the tasks finishes
    return (yield from pool.run(timeout=timeout,
                                return_when=return_when,
                                return_exceptions=return_exceptions))
