# -*- coding: utf-8 -*-
import time
from paco import constant, identity
from .helpers import run_in_loop


def test_constant():
    task = constant(1)
    assert run_in_loop(task) == 1

    task = constant('foo')
    assert run_in_loop(task) == 'foo'

    task = constant({'foo': 'bar'})
    assert run_in_loop(task) == {'foo': 'bar'}

    task = constant((1, 2, 3))
    assert run_in_loop(task) == (1, 2, 3)

    task = constant(None)
    assert run_in_loop(task) is None


def test_identify():
    task = identity(1)
    assert run_in_loop(task) == 1

    task = identity('foo')
    assert run_in_loop(task) == 'foo'

    task = identity({'foo': 'bar'})
    assert run_in_loop(task) == {'foo': 'bar'}

    task = identity((1, 2, 3))
    assert run_in_loop(task) == (1, 2, 3)

    task = identity(None)
    assert run_in_loop(task) is None


def test_constant_delay():
    task = constant(1, delay=0.5)
    now = time.time()
    assert run_in_loop(task) == 1
    assert time.time() - now >= 0.5
