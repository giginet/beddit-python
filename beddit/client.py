import requests
from urllib.parse import urljoin
from .sleep import Sleep


class BedditClient(object):
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

    def get_sleep(self):
        path = "/api/v1/user/{}/sleep".format(self.user_id)
        r = self._request_with_header(path)
        return [Sleep(sleep) for sleep in r.json()]
