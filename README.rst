paco |Build Status| |PyPI| |Coverage Status| |Documentation Status| |Stability| |Quality| |Versions|
====================================================================================================

Small and idiomatic utility library for coroutine-driven, asynchronous-oriented generic programming in Python +3.4.

Built on top of `asyncio`_, paco provides missing capabilities from Python `stdlib`
to write asynchronous cooperative multitasking in a nice-ish way, plus higher-order function goodness.

paco can be your utility belt to deal with I/O-bound non-blocking concurrent code in a better and elegant way.

Features
--------

-  Simple and idiomatic API, extending Python ``stdlib`` with async coroutines gotchas.
-  Built-in configurable control-flow concurrency support.
-  Useful iterables, decorators, functors and convenient helpers.
-  Coroutine-based functional helpers: compose, throttle, partial, until, throttle, race...
-  Asynchronous coroutine port of Python built-in functions: `filter`, `map`, `dropwhile`, `filterfalse`, `reduce`...
-  Concurrent iterables and higher-order functions.
-  Better ``asyncio.gather()`` and ``asyncio.wait()`` with optional concurrency control and ordered results.
-  Works with both `async/await`_ and `yield from`_ coroutines syntax.
-  Designed for intensive I/O-bound concurrent non-blocking tasks.
-  Good interoperability with ``asyncio`` and Python ``stdlib`` functions.
-  Composable pipelines of functors for iterables via ``|` operator overloading.
-  Small and dependency free.
-  Compatible with Python +3.4.

Installation
------------

Using ``pip`` package manager:

.. code-block:: bash

    pip install paco

Or install the latest sources from Github:

.. code-block:: bash

    pip install -e git+git://github.com/h2non/paco.git#egg=paco


API
---

- paco.run_
- paco.partial_
- paco.apply_
- paco.constant_
- paco.throttle_
- paco.compose_
- paco.wraps_
- paco.once_
- paco.times_
- paco.defer_
- paco.timeout_
- paco.wait_
- paco.gather_
- paco.each_
- paco.series_
- paco.map_
- paco.filter_
- paco.reduce_
- paco.some_
- paco.every_
- paco.filterfalse_
- paco.dropwhile_
- paco.repeat_
- paco.until_
- paco.whilst_
- paco.race_
- paco.ConcurrentExecutor_


.. _paco.map: http://paco.readthedocs.io/en/latest/api.html#paco.map
.. _paco.run: http://paco.readthedocs.io/en/latest/api.html#paco.run
.. _paco.each: http://paco.readthedocs.io/en/latest/api.html#paco.each
.. _paco.some: http://paco.readthedocs.io/en/latest/api.html#paco.some
.. _paco.race: http://paco.readthedocs.io/en/latest/api.html#paco.race
.. _paco.once: http://paco.readthedocs.io/en/latest/api.html#paco.once
.. _paco.wait: http://paco.readthedocs.io/en/latest/api.html#paco.wait
.. _paco.wraps: http://paco.readthedocs.io/en/latest/api.html#paco.wraps
.. _paco.defer: http://paco.readthedocs.io/en/latest/api.html#paco.defer
.. _paco.apply: http://paco.readthedocs.io/en/latest/api.html#paco.apply
.. _paco.every: http://paco.readthedocs.io/en/latest/api.html#paco.every
.. _paco.until: http://paco.readthedocs.io/en/latest/api.html#paco.until
.. _paco.times: http://paco.readthedocs.io/en/latest/api.html#paco.times
.. _paco.series: http://paco.readthedocs.io/en/latest/api.html#paco.searies
.. _paco.gather: http://paco.readthedocs.io/en/latest/api.html#paco.gather
.. _paco.repeat: http://paco.readthedocs.io/en/latest/api.html#paco.repeat
.. _paco.reduce: http://paco.readthedocs.io/en/latest/api.html#paco.reduce
.. _paco.filter: http://paco.readthedocs.io/en/latest/api.html#paco.filter
.. _paco.whilst: http://paco.readthedocs.io/en/latest/api.html#paco.whilst
.. _paco.partial: http://paco.readthedocs.io/en/latest/api.html#paco.partial
.. _paco.timeout: http://paco.readthedocs.io/en/latest/api.html#paco.timeout
.. _paco.compose: http://paco.readthedocs.io/en/latest/api.html#paco.compose
.. _paco.throttle: http://paco.readthedocs.io/en/latest/api.html#paco.throttle
.. _paco.constant: http://paco.readthedocs.io/en/latest/api.html#paco.constant
.. _paco.dropwhile: http://paco.readthedocs.io/en/latest/api.html#paco.dropwhile
.. _paco.filterfalse: http://paco.readthedocs.io/en/latest/api.html#paco.filterfalse
.. _paco.concurrent: http://paco.readthedocs.io/en/latest/api.html#paco.concurrent
.. _paco.ConcurrentExecutor: http://paco.readthedocs.io/en/latest/api.html#paco.ConcurrentExecutor

Examples
^^^^^^^^

Asynchronously and concurrently execute multiple HTTP requests.

.. code-block:: python

    import paco
    import aiohttp

    async def fetch(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                return res

    async def fetch_urls():
        urls = [
            'https://www.google.com',
            'https://www.yahoo.com',
            'https://www.bing.com',
            'https://www.baidu.com',
            'https://duckduckgo.com',
        ]

        # Map concurrent executor with concurrent limit of 3
        responses = await paco.map(fetch, urls, limit=3)

        for res in responses:
            print('Status:', res.status)

    # Run in event loop
    paco.run(fetch_urls())



Concurrent pipeline-style chain composition of functors over any iterable object.

.. code-block:: python

    import paco

    async def filterer(x):
        return x < 8

    async def mapper(x):
        return x * 2

    async def drop(x):
        return x < 10

    async def reducer(acc, x):
        return acc + x

    async def task(numbers):
        return await (numbers
                       | paco.filter(filterer)
                       | paco.map(mapper)
                       | paco.dropwhile(drop)
                       | paco.reduce(reducer, initializer=0))

    # Run in event loop
    number = paco.run(task((1, 2, 3, 4, 5, 6, 7, 8, 9, 10)))
    print('Number:', number) # => 36

License
-------

MIT - Tomas Aparicio

.. _asynchronous: http://python.org
.. _asyncio: https://docs.python.org/3.5/library/asyncio.html
.. _Python: http://python.org
.. _annotated API reference: https://h2non.github.io/paco
.. _async/await: https://www.python.org/dev/peps/pep-0492/
.. _yield from: https://www.python.org/dev/peps/pep-0380/

.. |Build Status| image:: https://travis-ci.org/h2non/paco.svg?branch=master
   :target: https://travis-ci.org/h2non/paco
.. |PyPI| image:: https://img.shields.io/pypi/v/paco.svg?maxAge=2592000?style=flat-square
   :target: https://pypi.python.org/pypi/paco
.. |Coverage Status| image:: https://coveralls.io/repos/github/h2non/paco/badge.svg?branch=master
   :target: https://coveralls.io/github/h2non/paco?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/paco/badge/?version=latest
   :target: http://paco.readthedocs.io/en/latest/?badge=latest
.. |Quality| image:: https://codeclimate.com/github/h2non/paco/badges/gpa.svg
   :target: https://codeclimate.com/github/h2non/paco
   :alt: Code Climate
.. |Stability| image:: https://img.shields.io/pypi/status/paco.svg
   :target: https://pypi.python.org/pypi/paco
   :alt: Stability
.. |Versions| image:: https://img.shields.io/pypi/pyversions/paco.svg
   :target: https://pypi.python.org/pypi/paco
   :alt: Python Versions
