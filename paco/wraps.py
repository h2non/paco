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

        # Use as function wrapper
        def mult(num, foo=None):
            return num * 2

        coro = paco.wraps(mult)
        await coro(2, foo='bar')
        => 4

        # Use as decorator
        @paco.wraps
        def mult(num):
            return num * 2

        await mult(2)
        => 4
    """
    @functools.wraps(fn)
    @asyncio.coroutine
    def wrapper(*args, **kw):
        return fn(*args, **kw)
    return wrapper
