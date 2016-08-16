from datetime import datetime
from enum import Enum
from pytz import timezone


class SleepStage(Enum):
    Away = 65
    Sleep = 83
    RestlessSleep = 82
    Awake = 87
    NoSignal = 78
    GapInMeasurement = 71


class Presence(Enum):
    Away = 65
    Present = 80
    End = 78


class Sleep(object):
    class Property(object):
        def __init__(self, properties):
            for p in properties:
                score = int(properties[p])
                setattr(self, p, score)

    def __init__(self, response_object):
        self.timezone = timezone(response_object['timezone'])
        self.date = datetime.strptime(response_object['date'], '%Y-%m-%d').replace(tzinfo=self.timezone)
        self.start = datetime.fromtimestamp(response_object['start_timestamp'], tz=self.timezone)
        self.end = datetime.fromtimestamp(response_object['end_timestamp'], tz=self.timezone)
        self.session_range_start = datetime.fromtimestamp(response_object['session_range_start'], tz=self.timezone)
        self.session_range_end = datetime.fromtimestamp(response_object['session_range_end'], tz=self.timezone)
        self.updated = datetime.fromtimestamp(response_object['updated'], tz=self.timezone)

        # properties
        self.property = self.Property(response_object['properties'])

        time_value_tracks = response_object['time_value_tracks']
        self.actigram = {datetime.fromtimestamp(float(timestamp), tz=self.timezone): float(value)
                         for timestamp, value in time_value_tracks['actigram_epochwise']['items']}
        self.sleep_event = {datetime.fromtimestamp(float(timestamp), tz=self.timezone): SleepStage(value)
                            for timestamp, value in time_value_tracks['sleep_stages']['items']}
        self.presence = {datetime.fromtimestamp(float(timestamp), tz=self.timezone): Presence(value)
                         for timestamp, value in time_value_tracks['presence']['items']}
        self.snoring_episodes = {datetime.fromtimestamp(float(timestamp), tz=self.timezone): value
                                 for timestamp, value in time_value_tracks['presence']['items']}

        self.nap_periods = {datetime.fromtimestamp(float(timestamp), tz=self.timezone): float(value)
                            for timestamp, value in time_value_tracks['nap_periods']['items']}
        self.heart_rate_curve = {datetime.fromtimestamp(float(timestamp), tz=self.timezone): float(value)
                                 for timestamp, value in time_value_tracks['heart_rate_curve']['items']}
        self.sleep_cycles = {datetime.fromtimestamp(float(timestamp), tz=self.timezone): float(value)
                             for timestamp, value in time_value_tracks['sleep_cycles']['items']}
