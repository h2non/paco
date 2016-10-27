Examples
--------


Asynchronously and concurrently execute multiple HTTP requests.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
