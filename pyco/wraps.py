# -*- coding: utf-8 -*-
import asyncio


def wraps(fn):
    """
    Wraps a given function as coroutine function.

    This is a convenient helper function.

    Arguments:
        fn (function): function object to wrap.

    Returns:
        coroutinefunction.

    Usage::

        def mult(num, foo=None):
            return num * num
        coro = pyco.wrap(mult)
        await coro(2, foo='bar')
    """
    @asyncio.coroutine
    def wrapper(*args, **kw):
        return fn(*args, **kw)
    return wrapper
