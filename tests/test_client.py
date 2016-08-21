import unittest
from unittest.mock import patch, Mock, MagicMock
from beddit.client import BedditClient


def authenticated(testcase):
    def _inner(self, *args, **kwargs):
        response = MagicMock()
        response.json.side_effect = lambda: {'user': 10000, 'access_token': 'dummytoken'}
        response.status_code = 200
        payload = {
            'grant_type': 'password',
            'username': 'username',
            'password': 'password'
        }
        with patch('requests.post', return_value=response) as post:
            retval = testcase(self, *args, **kwargs)
            post.assert_called_with('https://cloudapi.beddit.com/api/v1/auth/authorize', data=payload)
            return retval
    return _inner


class BedditClientTest(unittest.TestCase):
    @authenticated
    def test_authenticate(self):
        client = BedditClient('username', 'password')

        self.assertEqual(client.user_id, 10000)
        self.assertEqual(client.access_token, 'dummytoken')

    def test_authentication_error(self):
        response = MagicMock()
        response.status_code = 400
        response.json.side_effect = lambda: {'description': 'auth_error'}
        with patch('requests.post', return_value=response):
            self.assertRaises(BedditClient.AuthError, BedditClient, 'username', 'password')

    def test_argument_error(self):
        self.assertRaises(BedditClient.ArgumentError, BedditClient, 'username')

