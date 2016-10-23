# -*- coding: utf-8 -*-
import asyncio
from .gather import gather


@asyncio.coroutine
def series(*coros_or_futures, timeout=None,
           loop=None, return_exceptions=False):
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
        timeout (int/float):
            maximum number of seconds to wait before returning.
        return_exceptions (bool):
            exceptions in the tasks are treated the same as successful results,
            instead of raising them.
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

        results = await pyco.series(
          task(1, foo='bar'),
          task(2, foo='bar'),
          task(3, foo='bar'),
          task(4, foo='bar'),
          return_exceptions=True)
    """
    return (yield from gather(*coros_or_futures,
                              loop=loop, limit=1, timeout=timeout,
                              return_exceptions=return_exceptions))
