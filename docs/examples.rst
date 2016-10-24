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

        # Map concurrent executor with 3 concurrent limit
        responses = await paco.map(fetch, urls, limit=3)

        for res in responses:
            print('Response:', res.status)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_urls())
