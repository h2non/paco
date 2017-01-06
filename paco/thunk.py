# -*- coding: utf-8 -*-
import asyncio
from .assertions import assert_corofunction


def thunk(coro):
    """
    A thunk is a subroutine that is created, often automatically, to assist
    a call to another subroutine.

    Creates a thunk coroutine which returns coroutine function that accepts no
    arguments and when invoked it schedules the wrapper coroutine and
    returns the final result.

    See Wikipedia page for more information about Thunk subroutines:
    https://en.wikipedia.org/wiki/Thunk

    Arguments:
        value (coroutinefunction): wrapped coroutine function to invoke.

    Returns:
        coroutinefunction

    Usage::

        async def task():
            return 'foo'

        coro = paco.thunk(task)

        await coro()
        # => 'foo'
        await coro()
        # => 'foo'

    """
    assert_corofunction(coro=coro)

    @asyncio.coroutine
    def wrapper():
        return (yield from coro())

    return wrapper
