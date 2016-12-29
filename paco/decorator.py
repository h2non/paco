# -*- coding: utf-8 -*-
import asyncio
import functools
from inspect import isfunction
from .generator import consume
from .assertions import iscoro_or_corofunc, isgenerator
from .pipe import overload  # noqa


def generator_consumer(coro):  # pragma: no cover
    """
    Decorator wrapper that consumes sync/async generators provided as
    interable input argument.

    This function is only intended to be used internally.

    Arguments:
        coro (coroutinefunction): function to decorate

    Raises:
        TypeError: if function or coroutine function is not provided.

    Returns:
        function: decorated function.
    """
    if not asyncio.iscoroutinefunction(coro):
        raise TypeError('coro must be a coroutine function')

    @functools.wraps(coro)
    @asyncio.coroutine
    def wrapper(*args, **kw):
        if len(args) > 1 and isgenerator(args[1]):
            args = list(args)
            args[1] = (yield from consume(args[1])
                       if hasattr(args[1], '__anext__')
                       else list(args[1]))
            args = tuple(args)
        return (yield from coro(*args, **kw))
    return wrapper


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
