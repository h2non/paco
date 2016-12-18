# -*- coding: utf-8 -*-
import asyncio
from paco import curry
from .helpers import run_in_loop


def task(x, y, baz=None, *args, **kw):
    return x + y, baz, kw


@asyncio.coroutine
def coro(x, y, baz=None, *args, **kw):
    return task(x, y, baz=baz, *args, **kw)


def test_curry_function_arity():
    num, val, kw = run_in_loop(curry(task)(2)(4)(baz='foo'))
    assert num == 6
    assert val == 'foo'
    assert kw == {}

    num, val, kw = run_in_loop(curry(task)(2, 4)(baz='foo'))
    assert num == 6
    assert val == 'foo'
    assert kw == {}

    num, val, kw = run_in_loop(curry(task)(2, 4, baz='foo'))
    assert num == 6
    assert val == 'foo'
    assert kw == {}

    num, val, kw = run_in_loop(curry(task)(2, 4, baz='foo', fee=True))
    assert num == 6
    assert val == 'foo'
    assert kw == {'fee': True}


def test_curry_single_arity():
    assert run_in_loop(curry(lambda x: x)(True))


def test_curry_zero_arity():
    assert run_in_loop(curry(lambda: True))


def test_curry_custom_arity():
    currier = curry(4)
    num, val, kw = run_in_loop(currier(task)(2)(4)(baz='foo')(tee=True))
    assert num == 6
    assert val == 'foo'
    assert kw == {'tee': True}


def test_curry_ignore_kwargs():
    currier = curry(ignore_kwargs=True)
    num, val, kw = run_in_loop(currier(task)(2)(4))
    assert num == 6
    assert val is None
    assert kw == {}

    currier = curry(ignore_kwargs=True)
    num, val, kw = run_in_loop(currier(task)(2)(4, baz='foo', tee=True))
    assert num == 6
    assert val is 'foo'
    assert kw == {'tee': True}


def test_curry_extra_arguments():
    currier = curry(4)
    num, val, kw = run_in_loop(currier(task)(2)(4)(baz='foo')(tee=True))
    assert num == 6
    assert val == 'foo'
    assert kw == {'tee': True}

    currier = curry(4)
    num, val, kw = run_in_loop(currier(task)(2)(4)(baz='foo')(tee=True))
    assert num == 6
    assert val == 'foo'
    assert kw == {'tee': True}


def test_curry_evaluator_function():
    def evaluator(acc, fn):
        return len(acc[0]) < 3

    def task(x, y):
        return x * y

    currier = curry(evaluator=evaluator)
    assert run_in_loop(currier(task)(4, 4)) == 16


def test_curry_decorator():
    @curry
    def task(x, y, z):
        return x + y + z

    assert run_in_loop(task(2)(4)(8)) == 14

    @curry(4)
    def task(x, y, *args):
        return x + y + args[0] + args[1]

    assert run_in_loop(task(2)(4)(8)(10)) == 24

    @curry(4)
    @asyncio.coroutine
    def task(x, y, *args):
        return x + y + args[0] + args[1]

    assert run_in_loop(task(2)(4)(8)(10)) == 24


def test_curry_coroutine():
    num, val, kw = run_in_loop(curry(coro)(2)(4)(baz='foo', tee=True))
    assert num == 6
    assert val == 'foo'
    assert kw == {'tee': True}
