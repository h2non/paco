# -*- coding: utf-8 -*-
from .times import times
from .decorator import decorate


@decorate
def once(coro, raise_exception=False, return_value=None):
    """
    Wrap a given coroutine function that is restricted to one execution.

    Repeated calls to the coroutine function will return the value of the first
    invocation.

    This function can be used as decorator.

    arguments:
        coro (coroutinefunction): coroutine function to wrap.
        raise_exception (bool): raise exception if execution times exceeded.
        return_value (mixed): value to return when execution times exceeded,
            instead of the memoized one from last invocation.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        coroutinefunction

    Usage::

        task = paco.once(coro, return_value='exceeded')
        task(1, foo='bar')
        => 1
        task(2, foo='baz')
        => 'exceeded'
    """
    return times(coro,
                 limit=1,
                 return_value=return_value,
                 raise_exception=raise_exception)
