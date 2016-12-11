# -*- coding: utf-8 -*-
import asyncio
from inspect import isfunction


def coroutine_wrapper(fn):
    @asyncio.coroutine
    def wrapper(*args, **kw):
        return fn(*args, **kw)
    return wrapper


class Observer(object):
    """
    Observer implements a simple observer pub/sub pattern with a minimal
    interface and built-in coroutines support for asynchronous-first approach,
    desiged as abstract class to be inherited or embed by observable classes.
    """

    def __init__(self):
        self._pool = {}

    def observe(self, event, fn):
        """
        Arguments:
            event (str): event to subscribe.
            fn (function|coroutinefunction): function to trigger.

        Raises:
            TypeError: if fn argument is not valid
        """
        iscoroutine = asyncio.iscoroutinefunction(fn)
        if not iscoroutine and not isfunction(fn):
            raise TypeError('fn param must be a callable object '
                            'or coroutine function')

        observers = self._pool.get(event)
        if not observers:
            observers = self._pool[event] = []

        # Register the observer
        observers.append(fn if iscoroutine else coroutine_wrapper(fn))

    def remove(self, event=None):
        """
        Remove all the registered observers for the given event name.

        Arguments:
            event (str): event name to remove.
        """
        observers = self._pool.get(event)
        if observers:
            self._pool[event] = []

    def clear(self):
        """
        Clear all the registered observers.
        """
        self._pool = {}

    # Shortcut methods
    on = observe
    off = remove

    @asyncio.coroutine
    def trigger(self, event, *args, **kw):
        """
        Triggers event observers for the given event name,
        passing custom variadic arguments.
        """
        observers = self._pool.get(event)

        # If no observers registered for the event, do no-op
        if not observers or len(observers) == 0:
            return None

        # Trigger observers coroutines in FIFO sequentially
        for fn in observers:
            # Review: perhaps this should not wait
            yield from fn(*args, **kw)
