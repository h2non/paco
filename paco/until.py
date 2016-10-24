# -*- coding: utf-8 -*-
import asyncio
from .whilst import whilst


@asyncio.coroutine
def until(coro, coro_test, assert_coro=None, *args, **kw):
    """
    Repeatedly call `coro` coroutine function until `coro_test` returns `True`.

    This function is the inverse of `paco.whilst()`.

    This function is a coroutine.

    Arguments:
        coro (coroutinefunction): coroutine function to execute.
        coro_test (coroutinefunction): coroutine function to test.
        assert_coro (coroutinefunction): optional assertion coroutine used
            to determine if the test passed or not.
        *args (mixed): optional variadic arguments to pass to `coro` function.

    Raises:
        TypeError: if input arguments are invalid.

    Returns:
        list: result values returned by `coro`.

    Usage::

        await paco.until(coro, [1, 2, 3, 4, 5])
    """
    @asyncio.coroutine
    def assert_coro(value):
        return not value

    return (yield from whilst(coro, coro_test,
                              assert_coro=assert_coro, *args, **kw))
