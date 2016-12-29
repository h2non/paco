import asyncio
import inspect

# Safe alias to inspect.isasyncgen for Python 3.6+
isasyncgen = getattr(inspect, 'isasyncgen', lambda x: False)


def isiter(x):
    """
    Returns `True` if the given value implements an valid iterable
    interface.

    Arguments:
        x (mixed): value to check if it is an iterable.

    Returns:
        bool
    """
    return hasattr(x, '__iter__') and not isinstance(x, (str, bytes))


def isgenerator(x):
    """
    Returns `True` if the given value is sync or async generator coroutine.

    Arguments:
        x (mixed): value to check if it is an iterable.

    Returns:
        bool
    """
    return any([
        hasattr(x, '__next__'),
        hasattr(x, '__anext__')
    ])


def iscallable(x):
    """
    Returns `True` if the given value is a callable primitive object.

    Arguments:
        x (mixed): value to check.

    Returns:
        bool
    """
    return any([
        isfunc(x),
        asyncio.iscoroutinefunction(x)
    ])


def isfunc(x):
    """
    Returns `True` if the given value is a function or method object.

    Arguments:
        x (mixed): value to check.

    Returns:
        bool
    """
    return any([
        inspect.isfunction(x) and not asyncio.iscoroutinefunction(x),
        inspect.ismethod(x) and not asyncio.iscoroutinefunction(x)
    ])


def iscoro_or_corofunc(x):
    """
    Returns ``True`` if the given value is a coroutine or a coroutine function.

    Arguments:
        x (mixed): object value to assert.

    Returns:
        bool: returns ``True`` if ``x` is a coroutine or coroutine function.
    """
    return asyncio.iscoroutinefunction(x) or asyncio.iscoroutine(x)


def assert_corofunction(**kw):
    """
    Asserts if a given values are a coroutine function.

    Arguments:
        **kw (mixed): value to check if it is an iterable.

    Raises:
        TypeError: if assertion fails.
    """
    for name, value in kw.items():
        if not asyncio.iscoroutinefunction(value):
            raise TypeError('{} must be a coroutine function'.format(name))


def assert_iter(**kw):
    """
    Asserts if a given values implements a valid iterable interface.

    Arguments:
        **kw (mixed): value to check if it is an iterable.

    Raises:
        TypeError: if assertion fails.
    """
    for name, value in kw.items():
        if not isiter(value):
            raise TypeError('{} must be an iterable object'.format(name))
