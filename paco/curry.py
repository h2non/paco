# -*- coding: utf-8 -*-
import inspect
import functools
from .wraps import wraps
from .assertions import isfunc, iscallable


def curry(arity_or_fn=None, ignore_kwargs=False, evaluator=None, *args, **kw):
    """
    Creates a function that accepts one or more arguments of a function and
    either invokes func returning its result if at least arity number of
    arguments have been provided, or returns a function that accepts the
    remaining function arguments until the function arity is satisfied.

    This function is overloaded: you can pass a function or coroutine function
    as first argument or an `int` indicating the explicit function arity.

    Function arity can be inferred via function signature or explicitly
    passed via `arity_or_fn` param.

    You can optionally ignore keyword based arguments as well passsing the
    `ignore_kwargs` param with `True` value.

    This function can be used as decorator.

    Arguments:
        arity_or_fn (int|function|coroutinefunction): function arity to curry
            or function to curry.
        ignore_kwargs (bool): ignore keyword arguments as arity to satisfy
            during curry.
        evaluator (function): use a custom arity evaluator function.
        *args (mixed): mixed variadic arguments for partial function
            application.
        *kwargs (mixed): keyword variadic arguments for partial function
            application.

    Raises:
        TypeError: if function is not a function or a coroutine function.

    Returns:
        function or coroutinefunction: function will be returned until all the
            function arity is satisfied, where a coroutine function will be
            returned instead.

    Usage::

        # Function signature inferred function arity
        @paco.curry
        async def task(x, y, z=0):
            return x * y + z

        await task(4)(4)(z=8)
        # => 24

        # User defined function arity
        @paco.curry(4)
        async def task(x, y, *args, **kw):
            return x * y + args[0] * args[1]

        await task(4)(4)(8)(8)
        # => 80

        # Ignore keyword arguments from arity
        @paco.curry(ignore_kwargs=True)
        async def task(x, y, z=0):
            return x * y

        await task(4)(4)
        # => 16

    """
    def isvalidarg(x):
        return all([
            x.kind != x.VAR_KEYWORD,
            x.kind != x.VAR_POSITIONAL,
            any([
                not ignore_kwargs,
                ignore_kwargs and x.default == x.empty
            ])
        ])

    def params(fn):
        return inspect.signature(fn).parameters.values()

    def infer_arity(fn):
        return len([x for x in params(fn) if isvalidarg(x)])

    def merge_args(acc, args, kw):
        _args, _kw = acc
        _args = _args + args
        _kw = _kw or {}
        _kw.update(kw)
        return _args, _kw

    def currier(arity, acc, fn, *args, **kw):
        """
        Function either continues curring of the arguments
        or executes function if desired arguments have being collected.
        If function curried is variadic then execution without arguments
        will finish curring and trigger the function
        """
        # Merge call arguments with accumulated ones
        _args, _kw = merge_args(acc, args, kw)

        # Get current function call accumulated arity
        current_arity = len(args)

        # Count keyword params as arity to satisfy, if required
        if not ignore_kwargs:
            current_arity += len(kw)

        # Decrease function arity to satisfy
        arity -= current_arity

        # Use user-defined custom arity evaluator strategy, if present
        currify = evaluator and evaluator(acc, fn)

        # If arity is not satisfied, return recursive partial function
        if currify is not False and arity > 0:
            return functools.partial(currier, arity, (_args, _kw), fn)

        # If arity is satisfied, instanciate coroutine and return it
        return fn(*_args, **_kw)

    def wrapper(fn, *args, **kw):
        if not iscallable(fn):
            raise TypeError('first argument must a coroutine function, a '
                            'function or a method.')

        # Infer function arity, if required
        arity = (arity_or_fn if isinstance(arity_or_fn, int)
                 else infer_arity(fn))

        # Wraps function as coroutine function, if needed.
        fn = wraps(fn) if isfunc(fn) else fn

        # Otherwise return recursive currier function
        return currier(arity, (args, kw), fn, *args, **kw) if arity > 0 else fn

    # Return currier function or decorator wrapper
    return (wrapper(arity_or_fn, *args, **kw)
            if iscallable(arity_or_fn)
            else wrapper)
