# This file is placed in the Public Domain.
# pylint: disable=W0212,W0718


"reactor"


import queue
import threading
import time
import _thread


from .errors import later
from .thread import launch


class Reactor:

    "Reactor"

    threaded = True

    def __init__(self):
        self.cbs      = {}
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt):
        "call callback based on event type."
        func = self.cbs.get(evt.type, None)
        if func:
            evt._thr = launch(func, evt)

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            evt = None
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            except Exception as ex:
                later(ex)
                evt.ready()

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)


    def register(self, typ, cbs):
        "register callback for a type."
        self.cbs[typ] = cbs

    def start(self):
        "start the event loop."
        launch(self.loop)

    def stop(self):
        "stop the event loop."
        self.stopped.set()

    def wait(self):
        "wait until queue is empty."
        while 1:
            if self.queue.qsize() == 0:
                break
            time.sleep(1.0)


def __dir__():
    return (
        'Reactor',
    )
