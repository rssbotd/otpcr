# This file is placed in the Public Domain.
# pylint: disable=C0413,W0212


"daemon"


import getpass
import os
import sys


sys.path.insert(0, os.getcwd())


from .main    import Config, forever, initer, pidfile
from .main    import privileges, wrap
from .modules import face


Cfg = Config()
Cfg.mod = "cmd,err,mod,irc,rss,thr"
Cfg.user = getpass.getuser()


def daemon(verbose=False):
    "switch to background."
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    os.nice(10)


ever = forever


def main():
    "main"
    daemon()
    privileges(Cfg.user)
    pidfile(Cfg.pidfile)
    initer(Cfg.mod, face)
    ever()


def wrapping():
    "Wrap main."
    wrap(main)


if __name__ == "__main__":
    wrapping()
    