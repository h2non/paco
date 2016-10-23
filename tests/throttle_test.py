# -*- coding: utf-8 -*-
import time
import asyncio
from pyco import throttle
from .helpers import run_in_loop


@asyncio.coroutine
def coro(num):
    return num


def test_throttle():
    task = throttle(coro, limit=2, timeframe=0.2)
    assert run_in_loop(task, 1) == 1
    assert run_in_loop(task, 2) == 2
    assert run_in_loop(task, 3) == 2
    assert run_in_loop(task, 4) == 2
    time.sleep(0.3)
    assert run_in_loop(task, 5) == 5
    assert run_in_loop(task, 6) == 6
    assert run_in_loop(task, 7) == 6
    assert run_in_loop(task, 8) == 6


def test_throttle_return_value():
    task = throttle(coro, limit=2, timeframe=0.2, return_value='ignored')
    assert run_in_loop(task, 1) == 1
    assert run_in_loop(task, 2) == 2
    assert run_in_loop(task, 3) == 'ignored'
    assert run_in_loop(task, 4) == 'ignored'
    time.sleep(0.3)
    assert run_in_loop(task, 5) == 5
    assert run_in_loop(task, 6) == 6
    assert run_in_loop(task, 7) == 'ignored'
    assert run_in_loop(task, 8) == 'ignored'


def test_throttle_raise_exception():
    task = throttle(coro, limit=1, timeframe=1, raise_exception=True)
    assert run_in_loop(task, 1) == 1

    try:
        run_in_loop(task, 2)
    except Exception as err:
        assert isinstance(err, RuntimeError)
    else:
        raise RuntimeError('function must raise an exception')


def test_throttle_invalid_coro():
    try:
        throttle(None)
    except Exception as err:
        assert isinstance(err, TypeError)
    else:
        raise RuntimeError('function must raise an exception')


def test_decorator():
    task = throttle(limit=2, timeframe=0.2)(coro)
    assert run_in_loop(task, 1) == 1
    assert run_in_loop(task, 2) == 2
    assert run_in_loop(task, 3) == 2
    assert run_in_loop(task, 4) == 2
