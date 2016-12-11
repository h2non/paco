# -*- coding: utf-8 -*-
import asyncio
from .assertions import assert_iter

try:
    from asyncio import ensure_future
except ImportError:
    ensure_future = asyncio.async


@asyncio.coroutine
def race(iterable, loop=None, timeout=None, *args, **kw):
    """
    Runs coroutines from a given iterable concurrently without waiting until
    the previous one has completed.

    Once any of the tasks completes, the main coroutine
    is immediately resolved, yielding the first resolved value.

    All coroutines will be executed in the same loop.

    This function is a coroutine.

    Arguments:
        iterable (iterable): an iterable collection yielding
            coroutines functions or coroutine objects.
        *args (mixed): mixed variadic arguments to pass to coroutines.
        loop (asyncio.BaseEventLoop): optional event loop to use.
        timeout (int|float): timeout can be used to control the maximum number
            of seconds to wait before returning. timeout can be an int or
            float. If timeout is not specified or None, there is no limit to
            the wait time.
        *args (mixed): optional variadic argument to pass to coroutine
            function, if provided.

    Raises:
        TypeError: if ``iterable`` argument is not iterable.
        asyncio.TimoutError: if wait timeout is exceeded.

    Returns:
        filtered values (list): ordered list of resultant values.

    Usage::

        async def coro1():
            await asyncio.sleep(2)
            return 1

        async def coro2():
            return 2

        async def coro3():
            await asyncio.sleep(1)
            return 3

        await paco.race([coro1, coro2, coro3])
        # => 2

    """
    assert_iter(iterable=iterable)

    # Store coros and internal state
    coros = []
    resolved = False
    result = None

    # Resolve first yielded data from coroutine and stop pending ones
    @asyncio.coroutine
    def resolver(index, coro):
        nonlocal result
        nonlocal resolved

        value = yield from coro
        if not resolved:
            resolved = True

            # Flag as not test passed
            result = value

            # Force canceling pending coroutines
            for _index, future in enumerate(coros):
                if _index != index:
                    future.cancel()

    # Iterate and attach coroutine for defer scheduling
    for index, coro in enumerate(iterable):
        # Validate yielded object
        isfunction = asyncio.iscoroutinefunction(coro)
        if not isfunction and not asyncio.iscoroutine(coro):
            raise TypeError('coro must be a coroutine or coroutine function')

        # Init coroutine function, if required
        if isfunction:
            coro = coro(*args, **kw)

        # Store future tasks
        coros.append(ensure_future(resolver(index, coro)))

    # Run coroutines concurrently
    yield from asyncio.wait(coros, timeout=timeout, loop=loop)

    return result
