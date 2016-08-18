from datetime import datetime, timedelta
from enum import Enum
from pytz import timezone


class SensorStatus(Enum):
    Operational = 1
    Interference = 2
    Unclear = 3


class SampledTrack(object):
    def __init__(self, obj):
        self.samples_per_frame = obj['samples_per_frame']
        self.data_url = obj.get('data_url', None)


class Session(object):
    def __init__(self, response_object):
        self.timezone = timezone(response_object['timezone'])
        self.id = response_object['id']
        self.start = datetime.fromtimestamp(response_object['start_timestamp'], tz=self.timezone)
        self.end = datetime.fromtimestamp(response_object['end_timestamp'], tz=self.timezone)

        self.hardware = response_object.get("hardware", None)

        self.software = response_object["software"]
        self.frame_length = response_object.get("frame_length", None)
        self.error_code = response_object.get("error_code", None)
        self.sampled_tracks = [SampledTrack(obj) for obj in response_object.get('sampled_tracks', [])]

        time_value_tracks = response_object['time_value_tracks']

        def parse(name, initializer=float):
            if name in time_value_tracks:

                def datetime_from_start(timestamp):
                    td = timedelta(seconds=timestamp)
                    return self.start + td

                value = {datetime_from_start(float(timestamp)): initializer(v)
                         for timestamp, v in time_value_tracks[name]['items']}
                setattr(self, name, value)
            else:
                setattr(self, name, [])
        parse('respiration_cycle_amplitudes')
        parse('heartbeat')
        parse('heart_rate')
        parse('signal_high_percentile')
        parse('repiration_cycles')
        parse('events')
        parse('actigram')
        parse('sensor_status', initializer=SensorStatus)
        parse('snoring_events')
        parse('activity_segment_length')
        parse('high_activity_intervals')
        parse('activity_segment_variation')

        self.updated = datetime.fromtimestamp(response_object['updated'], tz=self.timezone)
