# -*- coding: utf-8 -*-
import asyncio
from .filter import assert_true
from .assertions import assert_corofunction


@asyncio.coroutine
def whilst(coro, coro_test, assert_coro=None, *args, **kw):
    """
    Make an iterator that drops elements from the iterable as long as the
    predicate is true; afterwards, returns every element.
    Note, the iterator does not produce any output until the predicate
    first becomes false, so it may have a lengthy start-up time.

    This function implements the same interface as Python standard
    `itertools.dropwhile()` function.

    All coroutines will be executed in the same loop.

    Arguments:
        coro (coroutine function): coroutine function to call with values
            to reduce.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list of resultant values.

    Usage::

        await pyco.whilst(coro, [1, 2, 3, 4, 5])
    """
    assert_corofunction(coro=coro, coro_test=coro_test)

    # Store yielded values by coroutine
    results = []

    # Set assertion coroutine
    assert_coro = assert_coro or assert_true

    # Execute coroutine until a certain
    while (yield from assert_coro((yield from coro_test()))):
        results.append((yield from coro(*args, **kw)))

    return results
