import sys
import asyncio

PY_35 = sys.version_info >= (3, 5)


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

    if not PY_35:
        raise RuntimeError('asynchronous iterator protocol not supported')

    # If asynchronous generator, consume it generator protocol manually
    buf = []
    while True:
        try:
            buf.append((yield from generator.__anext__()))
        except StopAsyncIteration:  # noqa
            break

    return buf
