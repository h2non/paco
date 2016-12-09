# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate
from .assertions import assert_corofunction


@decorate
def apply(coro, *args, **kw):
    """
    Creates a continuation coroutine function with some arguments
    already applied.

    Useful as a shorthand when combined with other control flow functions.
    Any arguments passed to the returned function are added to the arguments
    originally passed to apply.

    This is similar to `paco.partial()`.

    This function can be used as decorator.

    arguments:
        coro (coroutinefunction): coroutine function to wrap.
        *args (mixed): mixed variadic arguments for partial application.
        *kwargs (mixed): mixed variadic keyword arguments for partial
            application.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        coroutinefunction: wrapped coroutine function.

    Usage::

        async def hello(name, mark='!'):
            print('Hello, {name}{mark}'.format(name=name, mark=mark))

        hello_mike = paco.apply(hello, 'Mike')
        await hello_mike()
        # => Hello, Mike!

        hello_mike = paco.apply(hello, 'Mike', mark='?')
        await hello_mike()
        # => Hello, Mike?

    """
    assert_corofunction(coro=coro)

    @asyncio.coroutine
    def wrapper(*_args, **_kw):
        # Explicitely ignore wrapper arguments
        return (yield from coro(*args, **kw))

    return wrapper
