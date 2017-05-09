import requests
import signal
import sys
from .session import Session, SessionException
from .settings import Settings


commands = {
    "connect": (lambda app: app.establishHandshake()),
    "group":(lambda app: app.subscribeGroup(input("Provide groupId: "))),
    "user":(lambda app: app.subscribeUser(input("Provide userId: "))),
    "poll":(lambda app: app.poll()),
    "help": lambda _ : print(commands.keys())
}

def checkConfig():
    # TODO: Once again with the logging warn.
    # Also parse args and crap to check before this
    try:
        sessionSettings = Settings(file="config.json")
    except:
        raise SessionException("Running as module. Ensure config")

    return sessionSettings


def main():

    # Load config
    sessionSettings = checkConfig()

    # Otherwise establish connection
    connection = requests.session()
    app = Session(sessionSettings, connection)

    # In here for scope
    def gracefulExit(signum, frame):
        connection.close()
        # Do logging instead here
        print("Exiting...")
        sys.exit(0)

    # Handle abrupt endings
    originalSigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, gracefulExit)

    # Poor man's Terminal
    key = ""
    while key != "exit":
        key = input("Please provide command: ")
        if key in commands:
            commands[key](app)

if __name__ == "__main__":
    main()