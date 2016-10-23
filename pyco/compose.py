# -*- coding: utf-8 -*-
import asyncio
from .reduce import reduce


def compose(*coros):
    """
    Creates a coroutine function based on the composition of the passed
    coroutine functions.

    Each function consumes the yielded result of the coroutine that follows.

    Composing coroutine functions f(), g(), and h() would produce
    the result of f(g(h())).

    arguments:
        *coros (coroutinefunction): coroutine function to compose.

    Raises:
        RuntimeError: if cannot execute a coroutine function.

    Returns:
        coroutinefunction

    Usage::

        coro = pyco.compose(sum, mul, sum)
        coro(1)
        => 5
    """
    # Make list to inherit built-in type methods
    coros = list(coros)

    @asyncio.coroutine
    def reducer(acc, coro):
        return (yield from coro(acc))

    @asyncio.coroutine
    def wrapper(acc):
        return (yield from reduce(reducer, coros,
                                  initializer=acc, right=True))

    return wrapper
