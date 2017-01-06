# -*- coding: utf-8 -*-
import asyncio


def constant(value, delay=None):
    """
    Returns a coroutine function that when called, always returns
    the provided value.

    This function has an alias: `paco.identity`.

    Arguments:
        value (mixed): value to constantly return when coroutine is called.
        delay (int/float): optional return value delay in seconds.

    Returns:
        coroutinefunction

    Usage::

        coro = paco.constant('foo')

        await coro()
        # => 'foo'
        await coro()
        # => 'foo'

    """
    @asyncio.coroutine
    def coro():
        if delay:
            yield from asyncio.sleep(delay)
        return value

    return coro


def identity(value, delay=None):
    """
    Returns a coroutine function that when called, always returns
    the provided value.

    This function is an alias to `paco.constant`.

    Arguments:
        value (mixed): value to constantly return when coroutine is called.
        delay (int/float): optional return value delay in seconds.

    Returns:
        coroutinefunction

    Usage::

        coro = paco.identity('foo')

        await coro()
        # => 'foo'
        await coro()
        # => 'foo'

    """
    return constant(value, delay=delay)
