import unittest
import json
import os
from datetime import datetime
from beddit.group import Group


BASE_DIR = os.path.dirname(__file__)


class GroupTest(unittest.TestCase):
    @property
    def group_response(self):
        return json.load(open(os.path.join(BASE_DIR, 'fixtures/group.json')))

    def test_group(self):
        group = Group(self.group_response)
        self.assertEqual(group.id, 1234)
        self.assertEqual(group.created, datetime.utcfromtimestamp(1371472503.646541))
        self.assertEqual(len(group.members), 1)
        self.assertEqual(len(group.pending_invites), 1)

        pending_invite = group.pending_invites[0]
        self.assertEqual(pending_invite.created, datetime.utcfromtimestamp(1371472503.646541))
        self.assertEqual(pending_invite.created_by, 132)
        self.assertEqual(pending_invite.email, 'example@beddit.com')
