import asyncio


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
        if not hasattr(value, '__iter__'):
            raise TypeError('{} must be an iterable'.format(name))
