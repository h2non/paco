# -*- coding: utf-8 -*-
import time
import asyncio
from .decorator import decorate
from .assertions import assert_corofunction


def now():
    """
    Returns the current machine time in milliseconds.
    """
    return int(round(time.time() * 1000))


@decorate
def throttle(coro, limit=1, timeframe=1,
             return_value=None, raise_exception=False):
    """
    Creates a throttled coroutine function that only invokes
    ``coro`` at most once per every time frame of seconds or milliseconds.

    Provide options to indicate whether func should be invoked on the
    leading and/or trailing edge of the wait timeout.

    Subsequent calls to the throttled coroutine
    return the result of the last coroutine invocation.

    This function can be used as decorator.

    Arguments:
        coro (coroutinefunction):
            coroutine function to wrap with throttle strategy.
        limit (int):
            number of coroutine allowed execution in the given time frame.
        timeframe (int|float):
            throttle limit time frame in seconds.
        return_value (mixed):
            optional return if the throttle limit is reached.
            Returns the latest returned value by default.
        raise_exception (bool):
            raise exception if throttle limit is reached.

    Raises:
        RuntimeError: if cannot throttle limit reached (optional).

    Returns:
        coroutinefunction

    Usage::

        async def mul_2(num):
            return num * 2

        # Use as simple wrapper
        throttled = paco.throttle(mul_2, limit=1, timeframe=2)
        await throttled(2)
        # => 4
        await throttled(3)  # ignored!
        # => 4
        await asyncio.sleep(2)
        await throttled(3)  # executed!
        # => 6

        # Use as decorator
        @paco.throttle(limit=1, timeframe=2)
        async def mul_2(num):
            return num * 2

        await mul_2(2)
        # => 4
        await mul_2(3)  # ignored!
        # => 4
        await asyncio.sleep(2)
        await mul_2(3)  # executed!
        # => 6

    """
    assert_corofunction(coro=coro)

    # Store execution limits
    limit = max(int(limit), 1)
    remaning = limit

    # Turn seconds in milliseconds
    timeframe = timeframe * 1000

    # Keep call state
    last_call = now()
    # Cache latest retuned result
    result = None

    def stop():
        if raise_exception:
            raise RuntimeError('coroutine throttle limit exceeded')
        if return_value:
            return return_value
        return result

    def elapsed():
        return now() - last_call

    @asyncio.coroutine
    def wrapper(*args, **kw):
        nonlocal result
        nonlocal remaning
        nonlocal last_call

        if elapsed() > timeframe:
            # Reset reamining calls counter
            remaning = limit
            # Update last call time
            last_call = now()
        elif elapsed() < timeframe and remaning <= 0:
            return stop()

        # Decrease remaining limit
        remaning -= 1

        # Schedule coroutine passing arguments and cache result
        result = yield from coro(*args, **kw)
        return result

    return wrapper
