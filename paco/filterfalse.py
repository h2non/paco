# -*- coding: utf-8 -*-
import asyncio
from .filter import filter
from .decorator import overload


@asyncio.coroutine
def assert_false(element):
    """
    Asserts that a given coroutine yields a non-true value.
    """
    return not element


@overload
@asyncio.coroutine
def filterfalse(coro, iterable, limit=0, loop=None):
    """
    Returns a list of all the values in coll which pass an asynchronous truth
    test coroutine.

    Operations are executed concurrently by default, but results
    will be in order.

    You can configure the concurrency via `limit` param.

    This function is the asynchronous equivalent port Python built-in
    `filterfalse()` function.

    This function is a coroutine.

    This function can be composed in a pipeline chain with ``|`` operator.

    Arguments:
        coro (coroutine function): coroutine filter function to call accepting
            iterable values.
        iterable (iterable): an iterable collection yielding
            coroutines functions.
        assert_fn (coroutinefunction): optional assertion function.
        limit (int): max filtering concurrency limit. Use ``0`` for no limit.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        filtered values (list): ordered list containing values that do not
            passed the filter.

    Usage::

        async def iseven(num):
            return num % 2 == 0

        await paco.filterfalse(coro, [1, 2, 3, 4, 5])
        # => [1, 3, 5]

    """
    return (yield from filter(coro, iterable,
                              assert_fn=assert_false,
                              limit=limit, loop=loop))
