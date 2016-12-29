# -*- coding: utf-8 -*-
import asyncio
from .decorator import overload
from .concurrent import ConcurrentExecutor
from .assertions import assert_corofunction, assert_iter


@asyncio.coroutine
def assert_true(element):
    """
    Asserts that a given coroutine yields a true-like value.

    Arguments:
        element (mixed): element to evaluate.

    Returns:
        bool
    """
    return element


@overload
@asyncio.coroutine
def filter(coro, iterable, assert_fn=None, limit=0, loop=None):
    """
    Returns a list of all the values in coll which pass an asynchronous truth
    test coroutine.

    Operations are executed concurrently by default, but results
    will be in order.

    You can configure the concurrency via `limit` param.

    This function is the asynchronous equivalent port Python built-in
    `filter()` function.

    This function is a coroutine.

    This function can be composed in a pipeline chain with ``|`` operator.

    Arguments:
        coro (coroutine function): coroutine filter function to call accepting
            iterable values.
        iterable (iterable|asynchronousiterable): an iterable collection
            yielding coroutines functions.
        assert_fn (coroutinefunction): optional assertion function.
        limit (int): max filtering concurrency limit. Use ``0`` for no limit.
        loop (asyncio.BaseEventLoop): optional event loop to use.

    Raises:
        TypeError: if coro argument is not a coroutine function.

    Returns:
        list: ordered list containing values that passed
            the filter.

    Usage::

        async def iseven(num):
            return num % 2 == 0

        async def assert_false(el):
            return not el

        await paco.filter(iseven, [1, 2, 3, 4, 5])
        # => [2, 4]

        await paco.filter(iseven, [1, 2, 3, 4, 5], assert_fn=assert_false)
        # => [1, 3, 5]

    """
    assert_corofunction(coro=coro)
    assert_iter(iterable=iterable)

    # Check valid or empty iterable
    if len(iterable) == 0:
        return iterable

    # Reduced accumulator value
    results = [None] * len(iterable)

    # Use a custom or default filter assertion function
    assert_fn = assert_fn or assert_true

    # Create concurrent executor
    pool = ConcurrentExecutor(limit=limit, loop=loop)

    # Reducer partial function for deferred coroutine execution
    def filterer(index, element):
        @asyncio.coroutine
        def wrapper():
            result = yield from coro(element)
            if (yield from assert_fn(result)):
                results[index] = element
        return wrapper

    # Iterate and attach coroutine for defer scheduling
    for index, element in enumerate(iterable):
        pool.add(filterer(index, element))

    # Wait until all coroutines finish
    yield from pool.run(ignore_empty=True)

    # Returns filtered elements
    return [x for x in results if x is not None]
