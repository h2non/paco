# -*- coding: utf-8 -*-
import asyncio
from paco import partial
from .helpers import run_in_loop


@asyncio.coroutine
def coro(*args, **kw):
    return args, kw


def test_partial():
    task = partial(coro, 1, 2, foo='bar')
    args, kw = run_in_loop(task, 3, 4, bar='baz')

    assert len(args) == 4
    assert len(kw) == 2
    assert args == (1, 2, 3, 4)
    assert kw == {'foo': 'bar', 'bar': 'baz'}


def test_partial_variadic_arguments():
    task = partial(coro, 1)
    args, kw = run_in_loop(task, *(2, 3, 4))

    assert len(args) == 4
    assert len(kw) == 0
    assert args == (1, 2, 3, 4)


def test_partial_keyword_params_overwrite():
    task = partial(coro, foo='bar', bar='baz')
    args, kw = run_in_loop(task, bar='foo')

    assert len(args) == 0
    assert len(kw) == 2
    assert kw == {'foo': 'bar', 'bar': 'foo'}


def test_partial_no_extra_arguments():
    task = partial(coro, *(1, 2, 3, 4), foo='bar')
    args, kw = run_in_loop(task)

    assert len(args) == 4
    assert len(kw) == 1
    assert args == (1, 2, 3, 4)
    assert kw == {'foo': 'bar'}
