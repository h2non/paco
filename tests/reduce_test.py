# -*- coding: utf-8 -*-
import pytest
import asyncio
from paco import reduce
from .helpers import run_in_loop


@asyncio.coroutine
def coro(acc, num):
    return acc + (num * 2,)


@asyncio.coroutine
def sumfn(acc, num):
    return acc + num


def test_reduce():
    task = reduce(coro, [1, 2, 3, 4, 5], initializer=())
    assert run_in_loop(task) == (2, 4, 6, 8, 10)


def test_reduce_right():
    task = reduce(coro, [1, 2, 3, 4, 5], initializer=(), right=True)
    assert run_in_loop(task) == (10, 8, 6, 4, 2)


def test_reduce_acc():
    task = reduce(sumfn, [1, 2, 3, 4, 5], initializer=0)
    assert run_in_loop(task) == 15


def test_reduce_empty():
    assert run_in_loop(reduce(coro, (), initializer=1)) == 1


def test_reduce_invalid_input():
    with pytest.raises(TypeError):
        run_in_loop(reduce(coro, None))


def test_reduce_invalid_coro():
    with pytest.raises(TypeError):
        run_in_loop(reduce(None))
