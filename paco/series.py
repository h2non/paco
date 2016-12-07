# -*- coding: utf-8 -*-
import asyncio
from .gather import gather


@asyncio.coroutine
def series(*coros_or_futures, timeout=None,
           loop=None, return_exceptions=False):
    """
    Run the given coroutine functions in series, each one
    running once the previous execution has completed.

    If any coroutines raises an exception, no more
    coroutines are executed. Otherwise, the coroutines returned values
    will be returned as `list`.

    ``timeout`` can be used to control the maximum number of seconds to
    wait before returning. timeout can be an int or float.
    If timeout is not specified or None, there is no limit to the wait time.

    If ``return_exceptions`` is True, exceptions in the tasks are treated the
    same as successful results, and gathered in the result list; otherwise,
    the first raised exception will be immediately propagated to the
    returned future.

    All futures must share the same event loop.

    This functions is basically the sequential execution version of
    ``asyncio.gather()``. Interface compatible with ``asyncio.gather()``.

    This function is a coroutine.

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
        list: coroutines returned results.

    Raises:
        TypeError: in case of invalid coroutine object.
        ValueError: in case of empty set of coroutines or futures.
        TimeoutError: if execution takes more than expected.

    Usage::

        async def sum(x, y):
            return x + y

        await paco.series(
            sum(1, 2),
            sum(2, 3),
            sum(3, 4))
        # => [3, 5, 7]

    """
    return (yield from gather(*coros_or_futures,
                              loop=loop, limit=1, timeout=timeout,
                              return_exceptions=return_exceptions))
