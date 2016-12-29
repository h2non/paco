import asyncio


@asyncio.coroutine
def consume(generator):  # pragma: no cover
    """
    Helper function to consume a synchronous or asynchronous generator.

    Arguments:
        generator (generator|asyncgenerator): generator to consume.

    Returns:
        list
    """
    # If synchronous generator, just consume and return as list
    if hasattr(generator, '__next__'):
        return list(generator)

    # If asynchronous generator, consume it generator protocol manually
    buf = []
    while True:
        try:
            buf.append((yield from generator.__anext__()))
        except StopAsyncIteration:
            break

    return buf
