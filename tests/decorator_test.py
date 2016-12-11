# -*- coding: utf-8 -*-
import pytest
import asyncio
from paco.decorator import decorate
from .helpers import run_in_loop


@asyncio.coroutine
def coro(*args, **kw):
    return args, kw


def sample(coro, *args, **kw):
    return coro(*args, **kw)


def test_decorate_with_arguments():
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


def test_decorate_coro_object_argument():
    wrapper = decorate(lambda coro: coro)
    task = wrapper(coro(1, foo='bar'))
    args, kw = run_in_loop(task)

    assert args == (1,)
    assert kw == {'foo': 'bar'}


def test_decorate_invalid_input():
    with pytest.raises(TypeError):
        decorate(None)


def test_decorate_invalid_coroutine():
    with pytest.raises(TypeError):
        decorate(sample)(1)()


def test_decorate_invalid_coroutine_param():
    with pytest.raises(TypeError):
        decorate(sample)(None)(None)
