import time
import asyncio
from inspect import isfunction


@asyncio.coroutine
def sleep_coro(timespan=0.1):
    start = time.time()
    yield from asyncio.sleep(timespan)
    return time.time() - start


def run_in_loop(coro, *args, **kw):
    loop = asyncio.get_event_loop()
    if asyncio.iscoroutinefunction(coro) or isfunction(coro):
        coro = coro(*args, **kw)
    return loop.run_until_complete(coro)
