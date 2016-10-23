# -*- coding: utf-8 -*-
import asyncio


def constant(value, delay=None):
    """
    Returns a coroutine function that when called, always returns
    the provided value.

    arguments:
        value (mixed): value to constantly return.
        delay (int/float): optional return value delay in seconds.

    Returns:
        coroutinefunction

    Usage::

        coro = pyco.constant('foo')
        await coro()
        'foo'
    """
    @asyncio.coroutine
    def coro():
        if delay:
            yield from asyncio.sleep(delay)
        return value

    return coro
