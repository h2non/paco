# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate
from .assertions import assert_corofunction

ExceptionMessage = 'coroutine cannot be executed more than {} times'


@decorate
def times(coro, limit=1, raise_exception=False, return_value=None):
    """
    Wraps a given coroutine function to be executed only a certain amount
    of times.

    If the execution limit is exceeded, the last execution return value will
    be returned as result.

    You can optionally define a custom return value on exceeded via
    `return_value` param.

    This function can be used as decorator.

    arguments:
        coro (coroutinefunction): coroutine function to wrap.
        limit (int): max limit of coroutine executions.
        raise_exception (bool): raise exception if execution times exceeded.
        return_value (mixed): value to return when execution times exceeded.

    Raises:
        TypeError: if coro argument is not a coroutine function.
        RuntimeError: if max execution excedeed (optional).

    Returns:
        coroutinefunction

    Usage::

        async def mul_2(num):
            return num * 2

        timed = paco.times(mul_2, 3)
        await timed(2)
        # => 4
        await timed(3)
        # => 6
        await timed(4)
        # => 8
        await timed(5)  # ignored!
        # => 8
    """
    assert_corofunction(coro=coro)

    # Store call times
    limit = max(limit, 1)
    times = limit

    # Store result from last execution
    result = None

    @asyncio.coroutine
    def wrapper(*args, **kw):
        nonlocal limit
        nonlocal result

        # Check execution limit
        if limit == 0:
            if raise_exception:
                raise RuntimeError(ExceptionMessage.format(times))
            if return_value:
                return return_value
            return result

        # Decreases counter
        limit -= 1

        # If return_value is present, do not memoize result
        if return_value:
            return (yield from coro(*args, **kw))

        # Schedule coroutine and memoize result
        result = yield from coro(*args, **kw)
        return result

    return wrapper
