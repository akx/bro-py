# -- encoding: UTF-8 --

"""Bropages. See http://bropages.org

Usage:
  bro (t|up|thanks) <name>
  bro (n|down|no|...no) <name>
  bro (l|lookup) <name>
  bro (add) <name> [-m message]
  bro <name>
  bro (-h | --help)
  bro --version

Options:
  -h --help     Show this screen.
"""

import os
import requests
import sys

try:
    from termcolor import colored

    if "win" in sys.platform:
        import colorama
        colorama.init()

except ImportError:
    colored = lambda text, *args, **kwargs: text

URL = os.environ.get("BROPAGES_URL") or 'http://bropages.org'


class Problem(Exception):
    pass


class Bro(object):
    def __init__(self):
        self.client = requests.Session()
        self.client.headers["User-Agent"] = "Bro-Py " + self.client.headers["User-Agent"]

    def lookup(self, name):
        if not name:
            raise Problem("Need a name to look up a bropage.")

        resp = self.client.get("%s/%s.json" % (URL, name))
        if resp.status_code == 404:
            raise Problem("Don't know about '%s'." % name)

        resp.raise_for_status()
        data = resp.json()
        for entry in data:
            for line in entry["msg"].strip().splitlines():
                if line.startswith("#"):
                    print(colored(line, 'magenta', attrs=['bold']))
                else:
                    print(line)
            print("")

    def vote(self, name, direction):
        raise Problem("Voting isn't implemented.")

    def add(self, name, message=None):
        raise Problem("Adding isn't implemented.")

def simple():
    bro = Bro()
    try:
        bro.lookup(sys.argv[-1] if len(sys.argv) > 1 else None)
    except Problem, prob:
        print(colored(prob.message, "red", attrs=['bold']))

def main():
    try:
        from docopt import docopt
    except ImportError:
        return simple()

    arguments = docopt(__doc__, version='Bropages')
    bro = Bro()
    name = arguments.get("<name>")
    try:
        if arguments.get("t") or arguments.get("thanks") or arguments.get("up"):
            bro.vote(name, +1)
        elif arguments.get("n") or arguments.get("no") or arguments.get("...no") or arguments.get("down"):
            bro.vote(name, -1)
        elif arguments.get("add"):
            bro.add(name, arguments.get("message"))
        else:
            bro.lookup(name)
    except Problem, prob:
        print(colored(prob.message, "red", attrs=['bold']))


if __name__ == "__main__":
    main()
