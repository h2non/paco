# -*- coding: utf-8 -*-
import asyncio
import functools


def wraps(fn):
    """
    Wraps a given function as coroutine function.

    This function can be used as decorator.

    Arguments:
        fn (function): function object to wrap.

    Returns:
        coroutinefunction: wrapped function as coroutine.

    Usage::

        def mul_2(num):
            return num * 2

        # Use as function wrapper
        coro = paco.wraps(mul_2)
        await coro(2)
        # => 4

        # Use as decorator
        @paco.wraps
        def mul_2(num):
            return num * 2

        await mul_2(2)
        # => 4

    """
    # If already a coroutine function, just return it
    if asyncio.iscoroutinefunction(fn):
        return fn

    @functools.wraps(fn)
    @asyncio.coroutine
    def wrapper(*args, **kw):
        return fn(*args, **kw)

    return wrapper
