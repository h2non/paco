pyco |Build Status| |PyPI| |Coverage Status| |Documentation Status|
===================================================================

Small utility library for generic coroutine-driven, asynchronous-oriented programming in Python +3.4.

Built on top of `asyncio`_, pyco provides missing capabilities from Python `stdlib`
to write asynchronous cooperative multitasking in a nice-ish way + some convenient functional helpers.

Note: pyco is still beta.

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

    pip install pyco

Or install the latest sources from Github:

.. code-block:: bash

    pip install -e git+git://github.com/h2non/pyco.git#egg=pyco


API
---

- pyco.run_
- pyco.partial_
- pyco.apply_
- pyco.constant_
- pyco.throttle_
- pyco.compose_
- pyco.wraps_
- pyco.once_
- pyco.times_
- pyco.defer_
- pyco.timeout_
- pyco.wait_
- pyco.gather_
- pyco.each_
- pyco.series_
- pyco.map_
- pyco.filter_
- pyco.reduce_
- pyco.some_
- pyco.every_
- pyco.filterfalse_
- pyco.dropwhile_
- pyco.repeat_
- pyco.until_
- pyco.whilst_
- pyco.race_
- pyco.ConcurrentExecutor_


.. _pyco.map: http://pyco.readthedocs.io/en/latest/api.html#pyco.map
.. _pyco.run: http://pyco.readthedocs.io/en/latest/api.html#pyco.run
.. _pyco.each: http://pyco.readthedocs.io/en/latest/api.html#pyco.each
.. _pyco.some: http://pyco.readthedocs.io/en/latest/api.html#pyco.some
.. _pyco.race: http://pyco.readthedocs.io/en/latest/api.html#pyco.race
.. _pyco.once: http://pyco.readthedocs.io/en/latest/api.html#pycoonce
.. _pyco.wait: http://pyco.readthedocs.io/en/latest/api.html#pycowait
.. _pyco.wraps: http://pyco.readthedocs.io/en/latest/api.html#pycowraps
.. _pyco.defer: http://pyco.readthedocs.io/en/latest/api.html#pycodefer
.. _pyco.apply: http://pyco.readthedocs.io/en/latest/api.html#pycoapply
.. _pyco.every: http://pyco.readthedocs.io/en/latest/api.html#pycoevery
.. _pyco.until: http://pyco.readthedocs.io/en/latest/api.html#pycountil
.. _pyco.times: http://pyco.readthedocs.io/en/latest/api.html#pycotimes
.. _pyco.series: http://pyco.readthedocs.io/en/latest/api.html#pycosearies
.. _pyco.gather: http://pyco.readthedocs.io/en/latest/api.html#pycogather
.. _pyco.repeat: http://pyco.readthedocs.io/en/latest/api.html#pycorepeat
.. _pyco.reduce: http://pyco.readthedocs.io/en/latest/api.html#pycoreduce
.. _pyco.filter: http://pyco.readthedocs.io/en/latest/api.html#pycofilter
.. _pyco.whilst: http://pyco.readthedocs.io/en/latest/api.html#pycowhilst
.. _pyco.partial: http://pyco.readthedocs.io/en/latest/api.html#pycopartial
.. _pyco.timeout: http://pyco.readthedocs.io/en/latest/api.html#pycotimeout
.. _pyco.compose: http://pyco.readthedocs.io/en/latest/api.html#pycocompose
.. _pyco.throttle: http://pyco.readthedocs.io/en/latest/api.html#pycothrottle
.. _pyco.constant: http://pyco.readthedocs.io/en/latest/api.html#pycoconstant
.. _pyco.dropwhile: http://pyco.readthedocs.io/en/latest/api.html#pycodropwhile
.. _pyco.filterfalse: http://pyco.readthedocs.io/en/latest/api.html#pycofilterfalse
.. _pyco.concurrent: http://pyco.readthedocs.io/en/latest/api.html#pycoconcurrent
.. _pyco.ConcurrentExecutor: http://pyco.readthedocs.io/en/latest/api.html#pycoConcurrentExecutor

Examples
^^^^^^^^

Asynchronously execute multiple HTTP requests concurrently.

.. code-block:: python

    import pyco
    import aiohttp
    import asyncio

    async def fetch(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return resp

    async def fetch_urls():
        urls = [
            'https://www.google.com',
            'https://www.yahoo.com',
            'https://www.bing.com',
            'https://www.baidu.com',
            'https://duckduckgo.com',
        ]

        # Map concurrent executor with concurrent limit of 3
        responses = await pyco.map(fetch, urls, limit=3)

        for res in responses:
            print('Status:', res.status)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_urls())


License
-------

MIT - Tomas Aparicio

.. _asynchronous: http://python.org
.. _asyncio: https://docs.python.org/3.5/library/asyncio.html
.. _Python: http://python.org
.. _annotated API reference: https://h2non.github.io/pyco
.. _async/await: https://www.python.org/dev/peps/pep-0492/
.. _yield from: https://www.python.org/dev/peps/pep-0380/

.. |Build Status| image:: https://travis-ci.org/h2non/pyco.svg?branch=master
   :target: https://travis-ci.org/h2non/pyco
.. |PyPI| image:: https://img.shields.io/pypi/v/pyco.svg?maxAge=2592000?style=flat-square
   :target: https://pypi.python.org/pypi/pyco
.. |Coverage Status| image:: https://coveralls.io/repos/github/h2non/pyco/badge.svg?branch=master
   :target: https://coveralls.io/github/h2non/pyco?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/pyco/badge/?version=latest
   :target: http://pyco.readthedocs.io/en/latest/?badge=latest
