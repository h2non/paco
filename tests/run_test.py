# -*- coding: utf-8 -*-
import asyncio
from pyco import run


@asyncio.coroutine
def coro(num):
    return num * 2


def test_run():
    assert run(coro(2)) == 4


def test_run_loop():
    loop = asyncio.get_event_loop()
    assert run(coro(2), loop=loop) == 4
