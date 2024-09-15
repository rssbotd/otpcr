# This file is placed in the Public Domain.


"show errors"


from ..errors import Errors
from ..main   import Commands


def err(event):
    "show errors."
    nmr = 0
    for exc in Errors.errors:
        event.reply(exc)
        nmr += 1
    if not nmr:
        event.reply("no errors")
        return
    event.reply(f"found {nmr} errors.")


Commands.add(err)
