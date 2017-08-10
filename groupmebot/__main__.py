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
    "help": (lambda _: print(commands.keys()))
}


def buildSettings():

    # Read in args
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="accessToken")
    args = vars(parser.parse_args())

    try:
        sessionSettings = Settings(file="config.json", **args)
    except Exception:
        raise SessionException("Running as module. Ensure config")

    return sessionSettings


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
    def gracefulExit(signum, frame):
        connection.close()
        # Do logging instead here
        logging.info("Exiting...")
        sys.exit(0)

    # Handle abrupt endings
    signal.signal(signal.SIGINT, gracefulExit)

    # Poor man's Terminal
    key = ""
    # Python 2 compat
    input = raw_input or input
    while key != "exit":
        key = input("Please provide command: ")
        if key in commands:
            commands[key](app)


if __name__ == "__main__":
    main()
