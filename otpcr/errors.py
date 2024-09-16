# This file is placed in the Public Domain.
# pylint: disable=R0903


"deferred exception handling"


import traceback


class Errors:

    "Errors"

    errors = []


def format(exc):
    "format an exception"
    return traceback.format_exception(
                               type(exc),
                               exc,
                               exc.__traceback__
                              )


def errors(outer):
    "display errors."
    for exc in Errors.errors:
        for line in exc:
            outer(line.strip())


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    fmt = format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


def __dir__():
    return (
        'Errors',
        'errors',
        'later'
    )
