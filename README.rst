paco |Build Status| |PyPI| |Coverage Status| |Documentation Status| |Stability| |Quality| |Versions|
====================================================================================================

Small utility library for generic coroutine-driven, asynchronous-oriented programming in Python +3.4.

Built on top of `asyncio`_, paco provides missing capabilities from Python `stdlib`
to write asynchronous cooperative multitasking in a nice-ish way + some convenient functional helpers.

Note: paco is still beta.

Features
--------

-  Simple and idiomatic API, extending Python `stdlib` with async coroutines gotchas.
-  Built-in configurable control-flow concurrency support.
-  Useful iterables, decorators and functors.
-  Provides coroutine-ready compose, throttle, partial, until, race and other functional helpers.
-  Asynchronous coroutine port of Python built-in functions: `filter`, `map`, `dropwhile`, `filterfalse`, `reduce`...
-  Coroutines control flow and higher-order functions goodness.
-  Better `asyncio.gather()` and `asyncio.wait()` implementations with optional concurrency control and ordered results.
-  Good interoperability with `asyncio` and Python `stdlib` functions.
-  Partially ports Python `stdlib` higher-order functions and iterables to be used in async coroutines world.
-  Works with both `async/await`_ and `yield from`_ coroutines syntax.
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

Asynchronously execute multiple HTTP requests concurrently.

.. code-block:: python

    import paco
    import aiohttp
    import asyncio

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
