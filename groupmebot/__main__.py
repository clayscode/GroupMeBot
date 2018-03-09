from __future__ import print_function
from .session import Session, SessionException
from .settings import Settings
from .utils import *
import argparse
import requests
import signal
import sys


commands = {
    "connect": (lambda app: app.establishHandshake()),
    "getgroup": (lambda app: app.getGroup(input("Provide groupId: "))),
    "group": (lambda app: app.subscribeGroup(input("Provide groupId: "))),
    "user": (lambda app: app.subscribeUser(input("Provide userId: "))),
    "poll": (lambda app: app.poll()),
}
commands.update(dict.fromkeys(["help", "?", "h"], (lambda _: print(commands.keys()))))


def buildSettings():

    # Read in args
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="accessToken")
    args = vars(parser.parse_args())

    try:
        return Settings(file="config.json", **args)
    except Exception:
        raise SessionException("Running as module. Ensure config")


def main():
    # Start logging
    setupLogger()
    logging.debug('Logger set up')

    # Load config
    sessionSettings = buildSettings()

    # Otherwise establish connection
    connection = requests.session()
    app = Session(sessionSettings, connection)

    # In here for scope
    def gracefulExit(signum=None, frame=None):
        connection.close()
        # Do logging instead here
        logging.info("Exiting...")
        sys.exit(0)

    # Handle abrupt endings
    signal.signal(signal.SIGINT, gracefulExit)

    # Poor man's Terminal
    key = ""
    # Python 2 compat
    try:
        get_input = raw_input
    except NameError:
        get_input = input
    try:
        while key not in ["exit", "quit"]:
            key = get_input("Please provide command: ")
            if key in commands:
                commands[key](app)
    except EOFError:
        pass
    gracefulExit()

if __name__ == "__main__":
    main()
