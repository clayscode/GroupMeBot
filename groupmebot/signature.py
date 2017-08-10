import time
import pprint
from .utils import *


class Signature(object):
    """docstring for Signature"""
    def __init__(self, session):
        self._session = session

    def faye(self, payload):
        for instance in payload:
            instance["clientId"] = self._session._clientId
            instance["ext"] = {
                "access_token": self._session._settings.accessToken,
                "timestamp": time.time()
            }

        logging.debug("Outbound: \n" + pprint.pformat(payload))
        return payload

    def api(self, payload):
        payload["token"] = self._session._settings.accessToken
        logging.debug("Outbound: \n" + pprint.pformat(payload))
        return payload
