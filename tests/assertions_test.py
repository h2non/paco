# -*- coding: utf-8 -*-
import asyncio
from pyco.assertions import assert_corofunction, assert_iter


@asyncio.coroutine
def coro(*args, **kw):
    return args, kw


def test_assert_corofunction():
    assert_corofunction(coro=coro)

    try:
        assert_corofunction(coro=None)
    except TypeError as err:
        assert str(err) == 'coro must be a coroutine function'
    else:
        raise RuntimeError('must raise assert exception')


def test_assert_iter():
    assert_iter(iterable=())

    try:
        assert_iter(iterable=None)
    except TypeError as err:
        assert str(err) == 'iterable must be an iterable'
    else:
        raise RuntimeError('must raise assert exception')
