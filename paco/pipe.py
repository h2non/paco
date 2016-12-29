# -*- coding: utf-8 -*-
import asyncio
import functools
from inspect import isfunction, getargspec
from .generator import consume
from .assertions import isiter

# Yielded iterable error
IterableError = TypeError('pipeline yielded a non iterable object')


class PipeOverloader(object):
    """
    Pipe operator overloader object wrapping a given fn.
    """
    def __init__(self, fn, args, kw):
        self.__fn = fn
        self.__args = args
        self.__kw = kw

    @asyncio.coroutine
    def __await_coro(self, coro):
        return (yield from self.__trigger((yield from coro)))

    @asyncio.coroutine
    def __consume_generator(self, iterable):
        return (yield from self.__trigger((yield from consume(iterable))))

    def __trigger(self, iterable):
        if not isiter(iterable):
            raise IterableError

        # Compose arguments, placing iterable as second one
        args = self.__args[:1] + (iterable,) + self.__args[1:]
        # Call wrapped function
        result = self.__fn(*args, **self.__kw)

        # Clean memoized arguments to prevent memory leaks
        self.__args = None
        self.__kw = None

        # Return actual result
        return result

    def __ror__(self, iterable):
        """
        Overloads ``|`` operator expressions.
        """
        if not iterable:
            raise IterableError

        if hasattr(iterable, '__anext__'):
            return self.__consume_generator(iterable)

        if asyncio.iscoroutine(iterable):
            return self.__await_coro(iterable)

        return self.__trigger(iterable)

    def __call__(self, *args, **kw):
        """
        Maintain callable object behaviour.
        """
        _args = self.__args + args
        _kw = self.__kw
        _kw.update(kw)

        #  Clean memoized falues
        self.__args = None
        self.__kw = None

        return self.__fn(*_args, **_kw)


def overload(fn):
    """
    Overload a given callable object to be used with ``|`` operator
    overloading.

    This is especially used for composing a pipeline of
    transformation over a single data set.

    Arguments:
        fn (function): target function to decorate.

    Raises:
        TypeError: if function or coroutine function is not provided.

    Returns:
        function: decorated function
    """
    if not isfunction(fn):
        raise TypeError('fn must be a callable object')

    args = getargspec(fn).args
    if len(args) < 2 or args[1] != 'iterable':
        raise ValueError('invalid function signature or arity')

    @functools.wraps(fn)
    def decorator(*args, **kw):
        # Check function arity
        if len(args) < 2:
            return PipeOverloader(fn, args, kw)
        # Otherwise, behave like a normal wrapper
        return fn(*args, **kw)

    return decorator
