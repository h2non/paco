# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate


@decorate
def timeout(coro, timeout=None, loop=None):
    """
    Wraps a given coroutine function, that when executed, if it takes more
    than the given timeout in seconds to execute, it will be canceled and
    raise an `asyncio.TimeoutError`.

    This function is equivalent to Python standard
    `asyncio.wait_for()` function.

    This function can be used as decorator.

    Arguments:
        coro (coroutinefunction): coroutine to wrap.
        timeout (int|float): max wait timeout in seconds.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        coroutinefunction: wrapper coroutine function.

    Usage::

        await pyco.timeout(coro, timeout=10)
    """
    @asyncio.coroutine
    def wrapper(*args, **kw):
        coro_obj = coro(*args, **kw)
        return (yield from asyncio.wait_for(coro_obj, timeout, loop=loop))

    return wrapper
