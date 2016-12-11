# -*- coding: utf-8 -*-
import asyncio
from .decorator import decorate


@decorate
def timeout(coro, timeout=None, loop=None):
    """
    Wraps a given coroutine function, that when executed, if it takes more
    than the given timeout in seconds to execute, it will be canceled and
    raise an `asyncio.TimeoutError`.

    This function is equivalent to Python standard
    `asyncio.wait_for()` function.

    This function can be used as decorator.

    Arguments:
        coro (coroutinefunction|coroutine): coroutine to wrap.
        timeout (int|float): max wait timeout in seconds.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        coroutinefunction: wrapper coroutine function.

    Usage::

        await paco.timeout(coro, timeout=10)

    """
    @asyncio.coroutine
    def _timeout(coro):
        return (yield from asyncio.wait_for(coro, timeout, loop=loop))

    @asyncio.coroutine
    def wrapper(*args, **kw):
        return (yield from _timeout(coro(*args, **kw)))

    return _timeout(coro) if asyncio.iscoroutine(coro) else wrapper


class TimeoutLimit(object):
    """
    Timeout limit context manager.

    Useful in cases when you want to apply timeout logic around block
    of code or in cases when asyncio.wait_for is not suitable.

    Originally based on: https://github.com/aio-libs/async-timeout

    Arguments:
        timeout (int): value in seconds or None to disable timeout logic.
        loop (asyncio.BaseEventLoop): asyncio compatible event loop.

    Usage::

        with paco.TimeoutLimit(0.1):
            await paco.wait(task1, task2)
    """

    def __init__(self, timeout, loop=None):
        self._timeout = timeout
        self._loop = loop or asyncio.get_event_loop()
        self._task = None
        self._cancelled = False
        self._cancel_handler = None

    def __enter__(self):
        self._task = asyncio.Task.current_task(loop=self._loop)
        if self._task is None:
            raise RuntimeError('Timeout context manager should be used '
                               'inside a task')
        if self._timeout is not None:
            self._cancel_handler = self._loop.call_later(
                self._timeout, self.cancel)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is asyncio.CancelledError and self._cancelled:
            self._cancel_handler = None
            self._task = None
            raise asyncio.TimeoutError from None
        if self._timeout is not None:
            self._cancel_handler.cancel()
            self._cancel_handler = None
        self._task = None

    def cancel(self):
        """
        Cancels current task running task in the context manager.
        """
        self._cancelled = self._task.cancel()
