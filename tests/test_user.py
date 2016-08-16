import unittest
import json
import os
from datetime import datetime, timedelta
from beddit.user import User, Sex


BASE_DIR = os.path.dirname(__file__)


class UserTest(unittest.TestCase):
    @property
    def user_response(self):
        return json.load(open(os.path.join(BASE_DIR, 'fixtures/user.json')))

    def test_user(self):
        user = User(self.user_response)
        self.assertEqual(user.id, 10000)
        self.assertEqual(user.updated, datetime.utcfromtimestamp(1471356194))
        self.assertEqual(user.weight, 60.0)
        self.assertEqual(user.height, 175.0)
        self.assertEqual(user.sleep_time_goal, timedelta(seconds=27000))
        self.assertIn('general', user.tip_audiences)
        self.assertEqual(user.sex, Sex.Unknown)
        self.assertEqual(user.date_of_birth, datetime(1990, 1, 1))
        self.assertEqual(user.email, 'beddit@example.com')
        self.assertEqual(user.created, datetime.utcfromtimestamp(1468327763))
