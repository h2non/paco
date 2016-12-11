# -*- coding: utf-8 -*-
import functools
from inspect import isfunction
from .assertions import iscoro_or_corofunc
from .pipe import overload  # noqa


def decorate(fn):
    """
    Generic decorator for coroutines helper functions allowing
    multiple variadic initialization arguments.

    This function is intended to be used internally.

    Arguments:
        fn (function): target function to decorate.

    Raises:
        TypeError: if function or coroutine function is not provided.

    Returns:
        function: decorated function.
    """
    if not isfunction(fn):
        raise TypeError('fn must be a callable object')

    @functools.wraps(fn)
    def decorator(*args, **kw):
        # If coroutine object is passed
        for arg in args:
            if iscoro_or_corofunc(arg):
                return fn(*args, **kw)

        # Explicit argument must be at least a coroutine
        if len(args) and args[0] is None:
            raise TypeError('first argument cannot be empty')

        def wrapper(coro, *_args, **_kw):
            # coro must be a valid type
            if not iscoro_or_corofunc(coro):
                raise TypeError('first argument must be a '
                                'coroutine or coroutine function')

            # Merge call arguments
            _args = ((coro,) + (args + _args))
            kw.update(_kw)

            # Trigger original decorated function
            return fn(*_args, **kw)
        return wrapper
    return decorator
