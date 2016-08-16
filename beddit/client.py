import requests
import time
from urllib.parse import urljoin
import json
from .user import User
from .group import Group
from .sleep import Sleep
from .session import Session


def auth_required(func):
    def _is_logged_in(self, *args, **kwargs):
        if not self.access_token or not self.user_id:
            raise BedditClient.AuthError('authentication is required')
        return func(self, *args, **kwargs)
    return _is_logged_in


def datetime_to_timestamp(datetime):
    return time.mktime(datetime.timetuple())


class BedditClient(object):
    class ArgumentError(BaseException):
        pass

    class AuthError(BaseException):
        pass

    class APIError(BaseException):
        pass

    BASE_URL = 'https://cloudapi.beddit.com'
    access_token = None
    user_id = None

    def __init__(self, username = None, password = None, access_token = None):
        if access_token:
            self.access_token = access_token
        elif username and password:
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
        else:
            raise BedditClient.ArgumentError('you must either use the access_token or both username and password')

    @property
    def _headers(self):
        return {'Authorization': "UserToken {}".format(self.access_token)}

    def _get_with_auth(self, path, params={}):
        endpoint = urljoin(self.BASE_URL, path)
        r = requests.get(endpoint,
                         params=params,
                         headers=self._headers)
        return r

    def _post_with_auth(self, path, params={}):
        endpoint = urljoin(self.BASE_URL, path)
        r = requests.post(endpoint,
                          data=params,
                          headers=self._headers)
        return r

    def _put_with_auth(self, path, params={}):
        endpoint = urljoin(self.BASE_URL, path)
        r = requests.put(endpoint,
                         data=params,
                         headers=self._headers)
        return r

    @auth_required
    def get_sleeps(self, start=None, end=None, updated_after=None, limit=None, reverse=False):
        params = {}
        if start:
            params['start_date'] = start.strftime('%Y-%m-%d')
        if end:
            params['end_date'] = end.strftime('%Y-%m-%d')
        if updated_after:
            params['updated_after'] = updated_after.timestamp()
        if limit:
            params['limit'] = limit
        if reverse:
            params['reverse'] = 'yes'

        path = "/api/v1/user/{}/sleep".format(self.user_id)
        r = self._get_with_auth(path, params=params)
        if r.status_code == 200:
            return [Sleep(sleep) for sleep in r.json()]
        else:
            raise BedditClient.APIError(r.json()['description'])

    @auth_required
    def get_sessions(self, start=None, end=None, updated_after=None):
        params = {}

        if updated_after and not start and not end:
            params['updated_after'] = datetime_to_timestamp(updated_after)
        elif not updated_after and start and end:
            params['start_timestamp'] = datetime_to_timestamp(start)
            params['end_timestamp'] = datetime_to_timestamp(end)
        else:
            raise BedditClient.ArgumentError('you must either use the updated_after or both start and end.')

        path = "/api/v1/user/{}/session".format(self.user_id)
        r = self._get_with_auth(path, params=params)
        if r.status_code == 200:
            return [Session(session) for session in r.json()]
        else:
            raise BedditClient.APIError(r.json()['description'])

    @staticmethod
    def reset_password(email):
        path = "/api/v1/user/password_reset"
        r = requests.post(path, data={'email': email})
        if r.status_code == 200:
            return True
        else:
            raise BedditClient.APIError(r.status_code)

    @auth_required
    def get_user(self, user_id=None):
        if not user_id:
            user_id = self.user_id

        path = "/api/v1/user/{}".format(user_id)
        r = self._get_with_auth(path)
        if r.status_code == 200:
            return User(r.json())
        else:
            raise BedditClient.APIError(r.json()['description'])

    @auth_required
    def update_user(self, user_id=None, **params):
        if not user_id:
            user_id = self.user_id

        path = "/api/v1/user/{}".format(user_id)
        r = self._put_with_auth(path, params=json.dumps(params))
        if r.status_code == 200:
            return User(r.json())
        else:
            raise BedditClient.APIError(r.json()['description'])

    @auth_required
    def get_groups(self, user_id=None):
        if not user_id:
            user_id = self.user_id

        path = "/api/v1/user/{}/group".format(user_id)
        r = self._get_with_auth(path)
        if r.status_code == 200:
            return [Group(group) for group in r.json()]
        else:
            raise BedditClient.APIError(r.json()['description'])

    @auth_required
    def invite_to_group(self, email, group_id=None):
        if group_id:
            path = "/api/v1/group/{}/invite".format(group_id)
        else:
            path = "/api/v1/group/invite"

        r = self._post_with_auth(path, params={'email': email})
        if r.status_code == 200:
            return [Group(group) for group in r.json()]
        elif r.status_code == 400:
            raise BedditClient.APIError(r.json()['code'])

    @auth_required
    def accept_group_invite(self, group_id, invite_code):
        path = '/api/v1/group/{}/invite/{}/invite'.format(group_id, invite_code)
        r = self._post_with_auth(path)
        if r.status_code == 200:
            return True
        else:
            raise BedditClient.APIError(r.json()['code'])

    @auth_required
    def remove_group_invite(self, group_id, invite_code):
        path = '/api/v1/group/{}/invite/{}/remove'.format(group_id, invite_code)
        r = self._post_with_auth(path)
        if r.status_code == 200:
            return [Group(group) for group in r.json()]
        else:
            raise BedditClient.APIError(r.json()['code'])
