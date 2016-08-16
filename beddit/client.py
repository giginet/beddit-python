import requests
import time
from urllib.parse import urljoin
from .sleep import Sleep
from .session import Session


class BedditClient(object):
    class ArgumentError(BaseException):
        pass

    BASE_URL = 'https://cloudapi.beddit.com'
    access_token = None
    user_id = None

    def __init__(self, username, password):
        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password
        }
        endpoint = urljoin(self.BASE_URL, '/api/v1/auth/authorize')
        r = requests.post(endpoint, data=payload)
        if r.status_code == 200:
            response_object = r.json()
            self.access_token = response_object['access_token']
            self.user_id = response_object['user']

    def _request_with_header(self, path, params = {}):
        endpoint = urljoin(self.BASE_URL, path)
        r = requests.get(endpoint,
                         params=params,
                         headers={'Authorization': "UserToken {}".format(self.access_token)})
        return r

    def get_sleeps(self):
        path = "/api/v1/user/{}/sleep".format(self.user_id)
        r = self._request_with_header(path)
        return [Sleep(sleep) for sleep in r.json()]

    def get_sessions(self, start=None, end=None, updated_after=None):
        params = {}

        def datetime_to_timestamp(datetime):
            return time.mktime(datetime.timetuple())

        if updated_after and not start and not end:
            params['updated_after'] = datetime_to_timestamp(updated_after)
        elif not updated_after and start and end:
            params['start_timestamp'] = datetime_to_timestamp(start)
            params['end_timestamp'] = datetime_to_timestamp(end)
        else:
            raise BedditClient.ArgumentError('you must either use the updated_after or both start and end.')

        path = "/api/v1/user/{}/session".format(self.user_id)
        r = self._request_with_header(path, params=params)
        return [Session(session) for session in r.json()]
