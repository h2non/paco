# -*- coding: utf-8 -*-
import asyncio
from paco.observer import Observer
from .helpers import run_in_loop


def test_observer():
    def foo_listener(data, key=None):
        assert data == 'foo'
        assert key == 'foo'

    @asyncio.coroutine
    def bar_listener(data, key=None):
        assert data == 'bar'
        assert key == 'bar'

    observer = Observer()

    observer.observe('foo', foo_listener)
    observer.observe('bar', bar_listener)
    assert len(observer._pool) == 2

    run_in_loop(observer.trigger, 'foo', 'foo', key='foo')
    run_in_loop(observer.trigger, 'bar', 'bar', key='bar')

    # Event with no listeners
    observer.trigger('baz')

    # Remove listenrs
    observer.remove('bar')
    assert len(observer._pool) == 2
    assert len(observer._pool['bar']) == 0
    assert len(observer._pool['foo']) == 1

    # Remove all listeners
    observer.clear()
    assert len(observer._pool) == 0
