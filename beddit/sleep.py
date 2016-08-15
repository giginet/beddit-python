from datetime import datetime
from pytz import timezone


class Sleep(object):
    class Property(object):
        def __init__(self, properties):
            for property in properties:
                score = int(properties[property])
                setattr(self, property, score)

    def __init__(self, response_object):
        self.timezone = timezone(response_object['timezone'])
        self.date = datetime.strptime(response_object['date'], '%Y-%m-%d')
        self.date = self.date.replace(tzinfo=self.timezone)
        self.start = datetime.fromtimestamp(response_object['start_timestamp'], tz=self.timezone)
        self.end = datetime.fromtimestamp(response_object['end_timestamp'], tz=self.timezone)
        self.session_range_start = datetime.fromtimestamp(response_object['session_range_start'], tz=self.timezone)
        self.session_range_end = datetime.fromtimestamp(response_object['session_range_end'], tz=self.timezone)
        self.updated = datetime.fromtimestamp(response_object['updated'], tz=self.timezone)

        # properties
        self.property = self.Property(response_object['properties'])
