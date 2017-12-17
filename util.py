import os
import sys
import threading

import git

def delayed_restart(delay=10):
    threading.Timer(delay, restart).start()

def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

def update_from_git():
    g = git.cmd.Git(os.getcwd())
    g.pull()
