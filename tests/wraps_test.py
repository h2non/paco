# -*- coding: utf-8 -*-
from pyco import wraps
from .helpers import run_in_loop


def task(*args, **kw):
    return args, kw


def test_wraps():
    coro = wraps(task)

    args, kw = run_in_loop(coro, 1, 2, foo='bar')
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}

    args, kw = run_in_loop(coro, 3, 4, foo='baz')
    assert args == (3, 4)
    assert kw == {'foo': 'baz'}

    args, kw = run_in_loop(coro, 5, 6, foo='foo')
    assert args == (5, 6)
    assert kw == {'foo': 'foo'}
