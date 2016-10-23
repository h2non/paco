# -*- coding: utf-8 -*-
import asyncio
from pyco import some
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num < 2


@asyncio.coroutine
def coro_false(num):
    return num > 10


def test_some_truly():
    task = some(coro, [1, 2, 3, 4, 3, 1])
    assert run_in_loop(task) is True


def test_some_false():
    task = some(coro_false, [1, 2, 3, 4, 3, 1])
    assert run_in_loop(task) is False


def test_some_empty():
    task = some(coro, [])
    assert run_in_loop(task) is False


def test_some_invalid_input():
    try:
        run_in_loop(some(coro, None))
    except TypeError:
        pass
    else:
        raise RuntimeError('must raise exception')
