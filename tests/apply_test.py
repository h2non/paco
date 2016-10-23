# -*- coding: utf-8 -*-
import asyncio
from pyco import apply
from .helpers import run_in_loop


@asyncio.coroutine
def coro(*args, **kw):
    return args, kw


def test_apply():
    task = apply(coro, 1, 2, foo='bar')
    args, kw = run_in_loop(task)

    assert len(args) == 2
    assert len(kw) == 1
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}


def test_apply_variadic_arguments():
    task = apply(coro, *(1, 2, 3, 4))
    args, kw = run_in_loop(task)

    assert len(args) == 4
    assert len(kw) == 0
    assert args == (1, 2, 3, 4)


def test_apply_ignore_call_arguments():
    task = apply(coro, 1, 2, foo='bar')
    args, kw = run_in_loop(task, 1, 2, bar='foo')

    assert len(args) == 2
    assert len(kw) == 1
    assert args == (1, 2)
    assert kw == {'foo': 'bar'}
