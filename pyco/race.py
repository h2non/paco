# -*- coding: utf-8 -*-
import asyncio
from .assertions import assert_iter


@asyncio.coroutine
def race(iterable, loop=None, timeout=None, *args, **kw):
    """
    Make an iterator that drops elements from the iterable as long as the
    predicate is true; afterwards, returns every element.
    Note, the iterator does not produce any output until the predicate
    first becomes false, so it may have a lengthy start-up time.

    This function implements the same interface as Python standard
    `itertools.dropwhile()` function.

    All coroutines will be executed in the same loop.

    Arguments:
        iterable (iterable): an iterable collection yielding
            coroutines functions or coroutine objects.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if ``iterable`` argument is not iterable.
        asyncio.TimoutError: if wait timeout is exceeded.

    Returns:
        filtered values (list): ordered list of resultant values.

    Usage::

        await pyco.race(coro)
    """
    assert_iter(iterable=iterable)

    # Store coros and internal state
    coros = []
    resolved = False
    result = None

    # Resolve first yielded data from coroutine and stop pending ones
    @asyncio.coroutine
    def resolver(index, coro):
        nonlocal resolved
        nonlocal result

        if resolved:
            return None

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
        coros.append(asyncio.ensure_future(resolver(index, coro)))

    # Run coroutines concurrently
    yield from asyncio.wait(coros, timeout=timeout, loop=loop)

    return result
