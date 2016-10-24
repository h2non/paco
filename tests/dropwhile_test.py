# -*- coding: utf-8 -*-
import asyncio
from paco import dropwhile
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num < 4


def test_dropwhile():
    task = dropwhile(coro, [1, 2, 3, 4, 3, 1])
    assert run_in_loop(task) == [4, 3, 1]


def test_dropwhile_empty():
    task = dropwhile(coro, [])
    assert run_in_loop(task) == []


def test_dropwhile_invalid_input():
    try:
        run_in_loop(dropwhile(coro, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
