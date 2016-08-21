from datetime import datetime
from .user import User


class PendingInvite(object):
    def __init__(self, response_object):
        self.created = datetime.utcfromtimestamp(response_object['created'])
        self.created_by = response_object['created_by']
        self.email = response_object['email']


class Group(object):
    def __init__(self, response_object):
        self.id = int(response_object['id'])
        self.created = datetime.utcfromtimestamp(response_object['created'])
        self.members = [User(user) for user in response_object['members']]
        self.pending_invites = [PendingInvite(invitation) for invitation in response_object['pending_invites']]
