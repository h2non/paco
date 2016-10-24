# -*- coding: utf-8 -*-
import asyncio
from paco.decorator import decorate
from .helpers import run_in_loop


@asyncio.coroutine
def coro(*args, **kw):
    return args, kw


def sample(coro, *args, **kw):
    return coro(*args, **kw)


def test_decorate_arguments():
    wrapper = decorate(sample)
    task = wrapper(1, foo='bar')
    args, kw = run_in_loop(task, coro, 2, bar='baz')

    assert args == (1, 2)
    assert kw == {'foo': 'bar', 'bar': 'baz'}


def test_decorate_coro_argument():
    wrapper = decorate(sample)
    task = wrapper(coro, 1, foo='bar')
    args, kw = run_in_loop(task)

    assert args == (1,)
    assert kw == {'foo': 'bar'}


def test_decorate_invalid_input():
    try:
        decorate(None)
    except TypeError:
        pass
    else:
        raise RuntimeError('exception must be raised')


def test_decorate_invalid_coroutine():
    try:
        decorate(sample)(1)()
    except TypeError:
        pass
    else:
        raise RuntimeError('exception must be raised')
