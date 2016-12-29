# -*- coding: utf-8 -*-
"""Coroutines concurrent pool executor with built-in
concurrency limit based on a semaphore free slots algorithm.

Usage::

    async def fetch(url):
        r = await aiohttp.get(url)
        return await r.read()
    # limit the concurrent coroutines to 3
    pool = concurrent(3)
    for _ in range(10):
        p.submit(fetch, 'http://www.baidu.com')
    await p.join()
"""
import asyncio
from collections import deque, namedtuple
from .observer import Observer
from .assertions import isiter

# Task represents an immutable tuple storing the index order
# and coroutine object.
Task = namedtuple('Task', ['index', 'coro'])


@asyncio.coroutine
def safe_run(coro, return_exceptions=False):
    """
    Executes a given coroutine and optionally catches exceptions, returning
    them as value. This function is intended to be used internally.
    """
    try:
        result = yield from coro
    except Exception as err:
        if return_exceptions:
            result = err
        else:
            raise err
    return result


@asyncio.coroutine
def collect(coro, index, results,
            preserve_order=False,
            return_exceptions=False):
    """
    Collect is used internally to execute coroutines and collect the returned
    value. This function is intended to be used internally.
    """
    result = yield from safe_run(coro, return_exceptions=return_exceptions)

    if preserve_order:
        results[index] = result
    else:
        results.append(result)


class ConcurrentExecutor(object):
    """
    Concurrent executes a set of asynchronous coroutines
    with a simple throttle concurrency configurable concurrency limit.

    Provides an observer pub/sub interface, allowing API consumers to
    subscribe normal functions or coroutines to certain events that happen
    internally.

    ConcurrentExecutor is a low-level implementation that powers most of the
    utility functions provided in `paco`.

    For most cases you won't need to rely on it, instead you can
    use the high-level API functions that provides a simpler abstraction for
    the majority of the use cases.

    This class is not thread safe.

    Events:
        - start (executor): triggered before executor cycle starts.
        - finish (executor): triggered when all the coroutine finished.
        - task.start (task): triggered before coroutine starts.
        - task.finish (task, result): triggered when the coroutine finished.

    Arguments:
        limit (int): concurrency limit. Defaults to 10.
        coros (list[coroutine], optional): list of coroutines to schedule.
        loop (asyncio.BaseEventLoop, optional): loop to run.
            Defaults to asyncio.get_event_loop().
        ignore_empty (bool, optional): do not raise an exception if there are
            no coroutines to schedule are empty.

    Returns:
        ConcurrentExecutor

    Usage::

        async def sum(x, y):
            return x + y

        pool = paco.ConcurrentExecutor(limit=2)
        pool.add(sum, 1, 2)
        pool.add(sum, None, 'str')

        done, pending = await pool.run(return_exceptions=True)
        [task.result() for task in done]
        # => [3, TypeError("unsupported operand type(s) for +: 'NoneType' and 'str'")]  # noqa
    """

    def __init__(self, limit=10, loop=None, coros=None, ignore_empty=False):
        self.running = False
        self.return_exceptions = False
        self.limit = max(int(limit), 0)
        self.pool = deque()
        self.observer = Observer()
        self.ignore_empty = ignore_empty
        self.loop = loop or asyncio.get_event_loop()
        self.semaphore = asyncio.Semaphore(self.limit, loop=self.loop)

        # Register coroutines in the pool
        if isiter(coros):
            self.extend(*coros)

    def __len__(self):
        """
        Returns the current length of the coroutines pool queue.

        Returns:
            int: current coroutines pool length.
        """
        return len(self.pool)

    def reset(self):
        """
        Resets the executer scheduler internal state.

        Raises:
            RuntimeError: is the executor is still running.
        """
        if self.running:
            raise RuntimeError('executor is still running')

        self.pool.clear()
        self.observer.clear()
        self.semaphore = asyncio.Semaphore(self.limit, loop=self.loop)

    def cancel(self):
        """
        Tries to gracefully cancel the pending coroutine scheduled
        coroutine tasks.
        """
        self.pool.clear()
        self.running = False

    def on(self, event, fn):
        """
        Subscribes to a specific event.

        Arguments:
            event (str): event name to subcribe.
            fn (function): function to trigger.
        """
        return self.observer.on(event, fn)

    def off(self, event):
        """
        Removes event subscribers.

        Arguments:
            event (str): event name to remove observers.
        """
        return self.observer.off(event)

    def extend(self, *coros):
        """
        Add multiple coroutines to the executor pool.

        Raises:
            TypeError: if the coro object is not a valid coroutine
        """
        for coro in coros:
            self.add(coro)

    def add(self, coro, *args, **kw):
        """
        Adds a new coroutine function with optional variadic argumetns.

        Arguments:
            coro (coroutine function): coroutine to execute.
            *args (mixed): optional variadic arguments

        Raises:
            TypeError: if the coro object is not a valid coroutine

        Returns:
            future: coroutine wrapped future
        """
        # Create coroutine object if a function is provided
        if asyncio.iscoroutinefunction(coro):
            coro = coro(*args, **kw)

        # Verify coroutine
        if not asyncio.iscoroutine(coro):
            raise TypeError('coro must be a coroutine object')

        # Store coroutine with arguments for deferred execution
        index = max(len(self.pool), 0)
        task = Task(index, coro)

        # Append the coroutine data to the pool
        self.pool.append(task)

        return coro

    # Alias to add()
    submit = add

    @asyncio.coroutine
    def _run_sequentially(self):
        # Store futures in two queues
        done, pending = [], []

        # Run until the pool is empty
        while len(self.pool):
            future = asyncio.Future(loop=self.loop)
            pending.append(future)

            # Run coroutine
            result = yield from self._run_coro((self.pool.popleft()))

            # Assign result to future
            if isinstance(result, Exception):
                if not self.return_exceptions:
                    raise result
                future.set_exception(result)
            else:
                future.set_result(result)

            # Swap future between queues
            future = pending.pop()
            done.append(future)

        # Build futures tuple to be compatible with asyncio.wait() interface
        return set(done), set(pending)

    @asyncio.coroutine
    def _run_concurrently(self, timeout=None, return_when=None):
        coros = []
        limit = self.limit

        while len(self.pool):
            task = self.pool.popleft()

            # Run without concurrency limit
            if limit <= 0:
                coros.append(self._run_coro(task))
            # Otherwise, schedule for concurrent based flow
            else:
                coros.append(self._schedule_coro(task))

        # Wait until all the coroutines finish
        return (yield from asyncio.wait(coros,
                                        loop=self.loop,
                                        timeout=timeout,
                                        return_when=return_when))

    @asyncio.coroutine
    def _run_coro(self, task):
        # Executor must be running
        if not self.running:
            return None

        # Trigger task pre-execution event
        yield from self.observer.trigger('task.start', task)

        # Trigger coroutine task
        index, coro = task

        # Safe coroutine execution
        result = yield from safe_run(coro,
                                     return_exceptions=self.return_exceptions)

        # Trigger task post-execution event
        yield from self.observer.trigger('task.finish', task, result)

        # Return result to future binding
        return result

    @asyncio.coroutine
    def _schedule_coro(self, task):
        """
        Executes a given coroutine in the next available slot.

        Slots are available based on a simple free slots
        scheduling semaphore-based algorithm.
        """
        # Run when a slot is available
        with (yield from self.semaphore):
            return (yield from self._run_coro(task))

    @asyncio.coroutine
    def run(self, timeout=None,
            return_exceptions=None,
            return_when='ALL_COMPLETED',
            ignore_empty=None):
        """
        Executes the registered coroutines in the executor queue.

        Arguments:
            timeout (int/float): max execution timeout. No limit by default.
            return_exceptions (bool): in case of coroutine exception.
            return_when (str): sets when coroutine should be resolved.
                See `asyncio.wait`_ for supported values.
            ignore_empty (bool, optional): do not raise an exception if there are
                no coroutines to schedule are empty.

        Returns:
            asyncio.Future (tuple): two sets of Futures: ``(done, pending)``

        Raises:
            ValueError: if there is no coroutines to schedule.
            RuntimeError: if executor is still running.
            TimeoutError: if execution takes more than expected.

        .. _asyncio.wait: https://docs.python.org/3/library/asyncio-task.html#asyncio.wait  # noqa
        """
        # Only allow 1 concurrent execution
        if self.running:
            raise RuntimeError('executor is already running')

        # Overwrite ignore empty behaviour, if explicitly defined
        ignore_empty = (self.ignore_empty if ignore_empty is None
                        else ignore_empty)

        # Check we have coroutines to schedule
        if len(self.pool) == 0:
            # If ignore empty mode enabled, just return an empty tuple
            if ignore_empty:
                return (tuple(), tuple())
            # Othwerise raise an exception
            raise ValueError('Set of coroutines is empty')

        # Set executor state to running
        self.running = True

        # Configure return exceptions
        if return_exceptions is not None:
            self.return_exceptions = return_exceptions

        # Trigger pre-execution event
        self.observer.trigger('start', self)

        # Sequential coroutines execution
        if self.limit == 1:
            done, pending = yield from self._run_sequentially()

        # Concurrent execution based on configured limit
        if self.limit != 1:
            done, pending = yield from self._run_concurrently(
                timeout=timeout,
                return_when=return_when)

        # Reset internal state and queue
        self.running = False

        # Trigger pre-execution event
        self.observer.trigger('finish', self)

        # Reset executor state to defaults after each execution
        self.reset()

        # Return resultant futures in two tuples
        return done, pending

    # Idiomatic method alias to run()
    wait = run

    def is_running(self):
        """
        Checks the executor running state.

        Returns:
            bool: ``True`` if the executur is running, otherwise ``False``.
        """
        return self.running


# Semantic shortcut to ConcurrentExecutor()
concurrent = ConcurrentExecutor
