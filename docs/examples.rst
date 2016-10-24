Examples
--------


URL fetching with concurrency limit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
