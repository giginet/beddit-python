import unittest
import os
import json
import datetime
from tests.compatibility import patch, Mock
from beddit.client import BedditClient
from beddit.sleep import Sleep
from beddit.session import Session
from beddit.user import User
from beddit.group import Group

BASE_DIR = os.path.dirname(__file__)


def authenticated(testcase):
    def _inner(self, *args, **kwargs):
        response = Mock()
        response.json.side_effect = lambda: {'user': 10000, 'access_token': 'dummytoken'}
        response.status_code = 200
        payload = {
            'grant_type': 'password',
            'username': 'username',
            'password': 'password'
        }
        with patch('requests.post', return_value=response) as post:
            retval = testcase(self, *args, **kwargs)
            post.assert_called_with(BedditClient.build_full_path('api/v1/auth/authorize'), data=payload)
            return retval
    return _inner


class BedditClientTest(unittest.TestCase):
    @property
    def _default_client(self):
        return BedditClient('username', 'password')

    @authenticated
    def test_authenticate(self):
        client = self._default_client

        self.assertEqual(client.user_id, 10000)
        self.assertEqual(client.access_token, 'dummytoken')

    def test_authentication_error(self):
        response = Mock()
        response.status_code = 400
        response.json.side_effect = lambda: {'description': 'auth_error'}
        with patch('requests.post', return_value=response):
            self.assertRaises(BedditClient.AuthError, BedditClient, 'username', 'password')

    def test_argument_error(self):
        self.assertRaises(BedditClient.ArgumentError, BedditClient, 'username')

    @authenticated
    def test_get_sleep(self):
        client = self._default_client
        timestamp = 1471761649

        endpoint = BedditClient.build_full_path('/api/v1/user/10000/sleep')
        response = Mock()
        response.status_code = 200
        sleep_object = json.load(open(os.path.join(BASE_DIR, 'fixtures/sleep.json')))
        response.json = lambda: sleep_object
        with patch('requests.get', return_value=response) as get:
            sleeps = client.get_sleeps(
                start=datetime.datetime.utcfromtimestamp(timestamp),
                end=datetime.datetime.utcfromtimestamp(timestamp),
                limit=10,
                reverse=True
            )
            self.assertEqual(len(sleeps), 1)
            self.assertEqual(type(sleeps[0]), Sleep)

            args, kwargs = get.call_args
            self.assertEqual(args[0], endpoint)
            self.assertDictEqual(kwargs['params'], {
                'start_date': '2016-08-21',
                'end_date': '2016-08-21',
                'limit': 10,
                'reverse': 'yes'
            })

    @authenticated
    def test_get_session(self):
        client = self._default_client
        timestamp = 1471761649

        endpoint = BedditClient.build_full_path('/api/v1/user/10000/session')
        response = Mock()
        response.status_code = 200
        session_object = json.load(open(os.path.join(BASE_DIR, 'fixtures/session.json')))
        response.json = lambda: session_object
        dt = datetime.datetime.fromtimestamp(timestamp)
        with patch('requests.get', return_value=response) as get:
            sessions = client.get_sessions(updated_after=dt)
            self.assertEqual(len(sessions), 1)
            self.assertEqual(type(sessions[0]), Session)

            args, kwargs = get.call_args
            self.assertEqual(args[0], endpoint)
            self.assertDictEqual(kwargs['params'], {
                'updated_after': timestamp
            })

    @authenticated
    def test_get_session_with_invalid_argument(self):
        client = self._default_client
        self.assertRaises(BedditClient.ArgumentError, client.get_sessions)
        self.assertRaises(BedditClient.ArgumentError, client.get_sessions, start=datetime.datetime.now)
        self.assertRaises(BedditClient.ArgumentError, client.get_sessions, end=datetime.datetime.now)

    def test_reset_password(self):
        response = Mock()
        response.status_code = 200
        with patch('requests.post', return_value=response) as post:
            result = BedditClient.reset_password('new@example.com')
            self.assertTrue(result)

            post.assert_called_once_with(BedditClient.build_full_path('/api/v1/user/password_reset'),
                                         data={'email': 'new@example.com'})

    @authenticated
    def test_get_user(self):
        client = self._default_client

        endpoint = BedditClient.build_full_path('/api/v1/user/10000')
        response = Mock()
        response.status_code = 200
        user_object = json.load(open(os.path.join(BASE_DIR, 'fixtures/user.json')))
        response.json = lambda: user_object
        with patch('requests.get', return_value=response) as get:
            user = client.get_user()
            self.assertEqual(type(user), User)

            args = get.call_args[0]
            self.assertEqual(args[0], endpoint)

    @authenticated
    def test_update_user(self):
        client = self._default_client

        endpoint = BedditClient.build_full_path('/api/v1/user/10000')
        response = Mock()
        response.status_code = 200
        user_object = json.load(open(os.path.join(BASE_DIR, 'fixtures/user.json')))
        response.json = lambda: user_object
        with patch('requests.put', return_value=response) as put:
            user = client.update_user(name='foo')
            self.assertEqual(type(user), User)

            args = put.call_args[0]
            self.assertEqual(args[0], endpoint)

    @authenticated
    def test_get_group(self):
        client = self._default_client

        endpoint = BedditClient.build_full_path('/api/v1/user/10000/group')
        response = Mock()
        response.status_code = 200
        group_object = json.load(open(os.path.join(BASE_DIR, 'fixtures/group.json')))
        response.json = lambda: [group_object]
        with patch('requests.get', return_value=response) as get:
            groups = client.get_groups()
            self.assertEqual(type(groups[0]), Group)

            args = get.call_args[0]
            self.assertEqual(args[0], endpoint)

    @authenticated
    def test_invite_to_group(self):
        client = self._default_client

        endpoint = BedditClient.build_full_path('/api/v1/group/new/invite')
        response = Mock()
        response.status_code = 200
        group_object = json.load(open(os.path.join(BASE_DIR, 'fixtures/group.json')))
        response.json = lambda: [group_object]
        with patch('requests.post', return_value=response) as post:
            groups = client.invite_to_group(email="user@example.com")
            self.assertEqual(type(groups[0]), Group)

            args, kwargs = post.call_args
            self.assertEqual(args[0], endpoint)
            self.assertDictEqual(kwargs['data'], {
                'email': 'user@example.com'
            })

    @authenticated
    def test_remove_group_invite(self):
        client = self._default_client

        endpoint = BedditClient.build_full_path('/api/v1/group/200/member/10000/remove')
        response = Mock()
        response.status_code = 200
        group_object = json.load(open(os.path.join(BASE_DIR, 'fixtures/group.json')))
        response.json = lambda: [group_object]
        with patch('requests.post', return_value=response) as post:
            groups = client.remove_group_invite(group_id=200, user_id=10000)
            self.assertEqual(type(groups[0]), Group)

            args = post.call_args[0]
            self.assertEqual(args[0], endpoint)
