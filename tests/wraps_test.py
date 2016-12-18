# -*- coding: utf-8 -*-
import asyncio
from paco import wraps
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


def test_wraps_coroutine():
    @asyncio.coroutine
    def coro(x, foo=None):
        return x * 2, foo

    coro = wraps(coro)
    num, foo = run_in_loop(coro, 2, foo='bar')
    assert num == 4
    assert foo == 'bar'
