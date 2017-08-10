import pprint
import requests
from .signature import Signature
from .utils import *
from .const import EXCEPTIONS, JSON, ENDPOINTS, SUBSCRIPTIONS, TARGETS


class SessionException(Exception):
    """ Something went wrong with the session """


class Session(object):

    """Takes in settings"""

    def __init__(self, settings, connection):
        self._connection = connection
        self._settings = settings
        self._clientId = None
        self._signer = Signature(self)
        if not settings.valid:
            raise SessionException(EXCEPTIONS.BAD_SESSION_SETTINGS)

    @property
    def connection(self):
        return self._connection

    # TODO: Add error handling
    def establishHandshake(self):
        # Get initial client ID
        r = self.connection.post(ENDPOINTS.FAYE, json=[JSON.HANDSHAKE])
        data = r.json().pop()
        logging.debug("Handshake: \n" + pprint.pformat(r.json()))
        self._clientId = data['clientId']

    def _authenticate(F):
        def wrapper(self, *args):
            if self._clientId is None:
                raise SessionException(EXCEPTIONS.CONNECTIONLESS)

            return F(self, *args)

        return wrapper

    def poll(self):
        payload = JSON.POLL
        payload["clientId"] = self._clientId
        r = self.connection.post(ENDPOINTS.FAYE, json=[payload])
        logging.debug("Poll: \n" + pprint.pformat(r.json()))
        return r.status_code == requests.codes.ok, r.json()

    @_authenticate
    def subscribeUser(self, userId):
        payload = JSON.SUBSCRIBE_USER
        payload["subscription"] = SUBSCRIPTIONS.USER.format(userId)
        r = self.connection.post(ENDPOINTS.FAYE,
                                 json=self._signer.faye([payload]))
        logging.debug("Subscribe User: \n" + pprint.pformat(r.json()))
        return r.status_code == requests.codes.ok, r.json()

    @_authenticate
    def subscribeGroup(self, groupId):
        payload = JSON.SUBSCRIBE_GROUP
        payload["subscription"] = SUBSCRIPTIONS.GROUP.format(groupId)
        r = self.connection.post(ENDPOINTS.FAYE,
                                 json=self._signer.faye([payload]))
        logging.debug("Subscribe Group: \n" + pprint.pformat(r.json()))
        return r.status_code == requests.codes.ok, r.json()

    def getGroupById(self, groupId):
        payload = JSON.SHOW
        endpoint = ENDPOINTS.API + TARGETS.GROUP.format(groupId)
        r = self.connection.get(endpoint, params=self._signer.api(payload))
        logging.debug("Getting Group: \n" + pprint.pformat(r.json()))
        return r.status_code == requests.codes.ok, r.json()
