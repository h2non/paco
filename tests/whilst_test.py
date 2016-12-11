# -*- coding: utf-8 -*-
import pytest
import asyncio
from paco import whilst
from .helpers import run_in_loop


def test_whilst():
    calls = 0

    @asyncio.coroutine
    def coro_test():
        return calls < 5

    @asyncio.coroutine
    def coro():
        nonlocal calls
        calls += 1
        return calls

    task = whilst(coro, coro_test)
    assert run_in_loop(task) == [1, 2, 3, 4, 5]


def test_whilst_invalid_input():
    with pytest.raises(TypeError):
        run_in_loop(whilst(None, None))
