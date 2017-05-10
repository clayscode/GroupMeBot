import copy
CONFIG_FILE = "config.json"


class ENDPOINTS(object):
    FAYE = "https://push.groupme.com/faye"
    BOT_POST = "https://api.groupme.com/v3/bots/post"


class CHANNELS(object):
    HANDSHAKE = "/meta/handshake"
    SUBSCRIBE = "/meta/subscribe"
    CONNECT = "/meta/connect"


class EXCEPTIONS(object):
    BAD_SESSION_SETTINGS = "Cannot start session with bad settings"
    BAD_CONFIG = "Invalid configuration file"
    BAD_CONFIG_SAVE = "Error saving config file"
    CONNECTIONLESS = "Need to establish connection first"


class SUBSCRIPTIONS(object):
    USER = "/user/{}"
    GROUP = "/group/{}"


class JSON(object):
    HANDSHAKE = {
        "channel": CHANNELS.HANDSHAKE,
        "version": "1.0",
        "supportedConnectionTypes": ["long-polling"],
        "id": "3"
    }

    SUBSCRIBE_USER = {
        "channel": CHANNELS.SUBSCRIBE,
        "id": "4",
    }

    SUBSCRIBE_GROUP = {
        "channel": CHANNELS.SUBSCRIBE,
        "id": "5",
    }

    POLL = {
        "channel": CHANNELS.CONNECT,
        "connectionType": "long-polling",
        "id": "6"
    }

    def __getattr__(self, name):
        result = object.__getattribute__(self, name)
        return copy.deepcopy(result)
