import asyncio
import functools
from .utils import isiter
from inspect import isfunction, getargspec
from .assertions import assert_corofunction


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
        for arg in args:
            if asyncio.iscoroutinefunction(arg):
                return fn(*args, **kw)

        # Explicit argument must be at least a coroutine
        if len(args) and args[0] is None:
            raise TypeError('first argument cannot be None')

        def wrapper(coro, *_args, **_kw):
            assert_corofunction(coro=coro)
            # Merge call arguments
            _args = ((coro,) + (args + _args))
            kw.update(_kw)
            return fn(*_args, **kw)
        return wrapper
    return decorator


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

    def __trigger(self, iterable):
        if not isiter(iterable):
            raise TypeError('the pipeline yielded a non iterable object')

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
        if asyncio.iscoroutine(iterable):
            return self.__await_coro(iterable)
        else:
            return self.__trigger(iterable)

    def __call__(self, *args, **kw):
        return self.__fn(*args, **kw)


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
