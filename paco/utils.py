def isiter(x):
    """
    Returns True if the given value implements an valid iterable
    interface.

    Arguments:
        x (mixed): value to check if it is an iterable.

    Returns:
        bool
    """
    return hasattr(x, '__iter__')
