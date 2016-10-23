import asyncio
from inspect import isfunction
from .assertions import assert_corofunction


def decorate(fn):
    """
    Generic decorator for coroutines helper functions allowing
    multiple variadic initialization arguments.

    Arguments:
        fn (function): target function to decorate.

    Raises:
        TypeError: if function or coroutine function is not provided.

    Returns:
        function: decorated function.
    """
    if not isfunction(fn):
        raise TypeError('fn must be a callable object')

    def decorator(*args, **kw):
        for arg in args:
            if asyncio.iscoroutinefunction(arg):
                return fn(*args, **kw)

        # Explicit argument must be at least a coroutine
        if len(args) and args[0] is None:
            raise TypeError('first argument cannot be None')

        def wrapper(coro, *_args, **_kw):
            assert_corofunction(coro=coro)
            return fn(*(coro, *(*args, *_args)), **{**kw, **_kw})
        return wrapper

    return decorator
