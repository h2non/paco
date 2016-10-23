# -*- coding: utf-8 -*-
from .times import times
from .decorator import decorate


@decorate
def once(coro, raise_exception=False, return_value=None):
    """
    Creates a continuation coroutine function with some arguments
    already applied.

    Useful as a shorthand when combined with other control flow functions.
    Any arguments passed to the returned function are added to the arguments
    originally passed to apply.

    This function is similar to ``pyco.partial``.

    This function can be used as decorator.

    arguments:
        coro (coroutinefunction): coroutine function to wrap.
        raise_exception (bool): raise exception if execution times exceeded.
        return_value (mixed): value to return when execution times exceeded.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        coroutinefunction

    Usage::

        task = pyco.once(coro, return_value='exceeded')
        task(1, foo='bar')
        => 1
        task(2, foo='baz')
        => 'exceeded'
    """
    return times(coro,
                 limit=1,
                 return_value=return_value,
                 raise_exception=raise_exception)
