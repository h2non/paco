# -*- coding: utf-8 -*-
import pytest
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
    with pytest.raises(TypeError):
        run_in_loop(dropwhile(coro, None))
