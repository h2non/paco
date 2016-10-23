# -*- coding: utf-8 -*-
import time
import asyncio
from pyco import defer
from .helpers import run_in_loop


@asyncio.coroutine
def coro(x):
    return x


def test_defer():
    task = defer(coro, delay=0.2)
    now = time.time()
    assert run_in_loop(task, 1) == 1
    assert time.time() - now >= 0.2


def test_defer_decorator():
    task = defer(delay=0.2)(coro)
    now = time.time()
    assert run_in_loop(task, 1) == 1
    assert time.time() - now >= 0.2
