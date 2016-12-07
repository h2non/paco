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

        async def mul_2(num):
            return num * 2

        once = paco.once(mul_2)
        await once(2)
        # => 4
        await once(3)
        # => 4

        once = paco.once(mul_2, return_value='exceeded')
        await once(2)
        # => 4
        await once(3)
        # => 'exceeded'

    """
    return times(coro,
                 limit=1,
                 return_value=return_value,
                 raise_exception=raise_exception)
