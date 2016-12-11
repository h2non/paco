# -*- coding: utf-8 -*-
import pytest
import asyncio
from paco import once
from .helpers import run_in_loop


@asyncio.coroutine
def coro(*args, **kw):
    return args, kw


def test_once():
    task = once(coro)

    args, kw = run_in_loop(task, 1, 2, foo='bar')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    # Memoized result
    args, kw = run_in_loop(task, 3, 4, foo='baz')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    args, kw = run_in_loop(task, 5, 6, foo='foo')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}


def test_once_return_value():
    task = once(coro, return_value='ignored')

    args, kw = run_in_loop(task, 1, 2, foo='bar')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    # Ignored calls
    assert run_in_loop(task, 3, foo='foo') == 'ignored'
    assert run_in_loop(task, 4, foo='baz') == 'ignored'


def test_once_raise_exception():
    task = once(coro, raise_exception=True)

    args, kw = run_in_loop(task, 1, 2, foo='bar')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    with pytest.raises(RuntimeError):
        run_in_loop(task, 3, foo='foo')


def test_once_invalid_coro():
    with pytest.raises(TypeError):
        once(None)
