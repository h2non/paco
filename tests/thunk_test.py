# -*- coding: utf-8 -*-
import pytest
import asyncio
from paco import thunk
from .helpers import run_in_loop


@asyncio.coroutine
def task():
    return 'foo'


def test_thunk():
    coro = thunk(task)
    assert run_in_loop(coro()) == 'foo'
    assert run_in_loop(coro()) == 'foo'
    assert run_in_loop(coro()) == 'foo'


def test_thunk_error():
    with pytest.raises(TypeError):
        run_in_loop(None)

    with pytest.raises(TypeError):
        run_in_loop(1)

    with pytest.raises(TypeError):
        run_in_loop('foo')
