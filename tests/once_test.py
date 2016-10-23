# -*- coding: utf-8 -*-
import asyncio
from pyco import once
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

    try:
        run_in_loop(task, 3, foo='foo')
    except Exception as err:
        assert isinstance(err, RuntimeError)
    else:
        raise RuntimeError('function must raise an exception')


def test_once_invalid_coro():
    try:
        once(None)
    except Exception as err:
        assert isinstance(err, TypeError)
    else:
        raise RuntimeError('function must raise an exception')
