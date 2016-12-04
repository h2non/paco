# -*- coding: utf-8 -*-
import pytest
import asyncio
from paco import times
from .helpers import run_in_loop


@asyncio.coroutine
def coro(*args, **kw):
    return args, kw


def test_times():
    task = times(coro, 2)

    args, kw = run_in_loop(task, 1, 2, foo='bar')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    args, kw = run_in_loop(task, 3, 4, foo='baz')
    assert args == (3, 4)
    assert kw == {'foo': 'baz'}

    # Memoized result
    args, kw = run_in_loop(task, 5, 6, foo='foo')
    assert args == (3, 4)
    assert kw == {'foo': 'baz'}

    args, kw = run_in_loop(task, 7, 8, foo='foo')
    assert args == (3, 4)
    assert kw == {'foo': 'baz'}


def test_times_return_value():
    task = times(coro, 1, return_value='ignored')

    args, kw = run_in_loop(task, 1, 2, foo='bar')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    # Memoized result
    assert run_in_loop(task, 3, foo='foo') == 'ignored'
    assert run_in_loop(task, 4, foo='baz') == 'ignored'


def test_times_raise_exception():
    task = times(coro, 1, raise_exception=True)

    args, kw = run_in_loop(task, 1, 2, foo='bar')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    with pytest.raises(RuntimeError):
        run_in_loop(task, 3, foo='foo')


def test_times_invalid_coro():
    with pytest.raises(TypeError):
        times(None)
