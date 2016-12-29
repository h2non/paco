# -*- coding: utf-8 -*-
import asyncio
from .each import each
from .decorator import overload


@overload
@asyncio.coroutine
def map(coro, iterable, limit=0, loop=None, timeout=None,
        return_exceptions=False, *args, **kw):
    """
    Concurrently maps values yielded from an iterable, passing then
    into an asynchronous coroutine function.

    Mapped values will be returned as list.
    Items order will be preserved based on origin iterable order.

    Concurrency level can be configurable via ``limit`` param.

    This function is the asynchronous equivalent port Python built-in
    `map()` function.

    This function is a coroutine.

    This function can be composed in a pipeline chain with ``|`` operator.

    Arguments:
        coro (coroutinefunction): map coroutine function to use.
        iterable (iterable|asynchronousiterable): an iterable collection
            yielding coroutines functions.
        limit (int): max concurrency limit. Use ``0`` for no limit.
        loop (asyncio.BaseEventLoop): optional event loop to use.
        timeout (int|float): timeout can be used to control the maximum number
            of seconds to wait before returning. timeout can be an int or
            float. If timeout is not specified or None, there is no limit to
            the wait time.
        return_exceptions (bool): returns exceptions as valid results.
        *args (mixed): optional variadic arguments to be passed to the
            coroutine map function.

    Returns:
        list: ordered list of values yielded by coroutines

    Usage::

        async def mul_2(num):
            return num * 2

        await paco.map(mul_2, [1, 2, 3, 4, 5])
        # => [2, 4, 6, 8, 10]

    """
    # Call each iterable but collecting yielded values
    return (yield from each(coro, iterable,
                            limit=limit, loop=loop,
                            timeout=timeout, collect=True))
