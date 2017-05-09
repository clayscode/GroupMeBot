import time
import requests
from .const import EXCEPTIONS, JSON, ENDPOINTS, SUBSCRIPTIONS

class SessionException(Exception):
    """ Something went wrong with the session """

class Session(object):

    """Takes in settings"""
    def __init__(self, settings, connection):
        self._connection = connection
        self._settings = settings
        self._clientId = None
        if not settings.valid:
            raise SessionException(EXCEPTIONS.BAD_SESSION_SETTINGS)

    @property 
    def connection(self):
        return self._connection

    def _sign(self, payload):
        for instance in payload:
            instance["clientId"] = self._clientId
            instance["ext"] = {
                "access_token": self._settings.accessToken,
                "timestamp": time.time()
              }

        print(payload) # Swap to logging
        return payload


    #TODO: Add error handling
    #TODO: Add other endpoints
    def establishHandshake(self):
        # Get initial client ID
        r = self.connection.post(ENDPOINTS.FAYE, json=[JSON.HANDSHAKE])
        data = r.json().pop()
        print(data) # Swap to logging
        self._clientId = data['clientId']

    def poll(self):
        payload = JSON.POLL
        payload["clientId"] = self._clientId
        r = self.connection.post(ENDPOINTS.FAYE, json=[payload])
        print(r.json()) # Swap to logging
        return r.status_code == requests.codes.ok

    def _authenticate(F):
        def wrapper(self, *args):
            if self._clientId == None:
                raise SessionException(EXCEPTIONS.CONNECTIONLESS)

            return F(self, *args)

        return wrapper

    @_authenticate
    def subscribeUser(self, userId):
        payload = JSON.SUBSCRIBE_USER
        payload["subscription"] = SUBSCRIPTIONS.USER.format(userId)
        r = self.connection.post(ENDPOINTS.FAYE, json=self._sign([payload]))
        print(r.json()) # Swap to logging
        return r.status_code == requests.codes.ok

    @_authenticate
    def subscribeGroup(self, groupId):
        payload = JSON.SUBSCRIBE_GROUP
        payload["subscription"] = SUBSCRIPTIONS.GROUP.format(groupId)
        r = self.connection.post(ENDPOINTS.FAYE, json=self._sign([payload]))
        print(r.json()) # Swap to logging
        return r.status_code == requests.codes.ok