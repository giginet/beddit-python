from datetime import datetime, timedelta
from enum import Enum


class Sex(Enum):
    Unknown = None
    Male = 'male'
    Female = 'female'


class User(object):
    def __init__(self, response_object):
        self.id = response_object['id']
        self.email = response_object['email']
        self.name = response_object['name']
        self.date_of_birth = datetime.strptime(response_object['date_of_birth'], '%Y-%m-%d')
        self.sex = Sex(response_object['sex'])
        self.weight = float(response_object['weight'])
        self.height = float(response_object['height'])
        self.sleep_time_goal = timedelta(seconds=response_object['sleep_time_goal'])
        self.tip_audiences = response_object['tip_audiences']
        self.created = datetime.utcfromtimestamp(response_object['created'])
        self.updated = datetime.utcfromtimestamp(response_object['updated'])
