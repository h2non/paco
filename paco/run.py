import asyncio


def run(coro, loop=None):
    """
    Convenient shortcut alias to ``loop.run_until_complete``.

    Arguments:
        coro (coroutine): coroutine object to schedule.
        loop (asyncio.BaseEventLoop): optional event loop to use.
            Defaults to: ``asyncio.get_event_loop()``.

    Returns:
        mixed: returned value by coroutine.

    Usage::

        async def mul_2(num):
            return num * 2

        paco.run(mul_2(4))
        # => 8

    """
    loop = loop or asyncio.get_event_loop()
    return loop.run_until_complete(coro)
