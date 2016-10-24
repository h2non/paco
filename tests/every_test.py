# -*- coding: utf-8 -*-
import asyncio
from paco import every
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num < 4


@asyncio.coroutine
def coro_truly(num):
    return num < 10


def test_every_truly():
    task = every(coro_truly, [1, 2, 3, 4, 3, 1])
    assert run_in_loop(task) is True


def test_every_false():
    task = every(coro, [1, 2, 3, 4, 3, 1])
    assert run_in_loop(task) is False


def test_every_empty():
    task = every(coro, [])
    assert run_in_loop(task) is True


def test_every_invalid_input():
    try:
        run_in_loop(every(coro, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
