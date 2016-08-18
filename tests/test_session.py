import unittest
import json
import os
from datetime import datetime
from pytz import timezone
from beddit.session import Session


BASE_DIR = os.path.dirname(__file__)


class SessionTest(unittest.TestCase):
    @property
    def session_response(self):
        return json.load(open(os.path.join(BASE_DIR, 'fixtures/session.json')))

    def test_session(self):
        raw = self.session_response[0]
        session = Session(raw)
        jst = timezone('Asia/Tokyo')
        self.assertEqual(session.timezone, jst)
        self.assertEqual(session.id, raw['id'])
        self.assertEqual(session.start, datetime.fromtimestamp(raw['start_timestamp'], tz=jst))
        self.assertEqual(session.end, datetime.fromtimestamp(raw['end_timestamp'], tz=jst))
        self.assertEqual(session.updated, datetime.fromtimestamp(raw['updated'], tz=jst))
        self.assertEqual(session.hardware, raw['hardware'])
        self.assertEqual(session.frame_length, raw['frame_length'])
        self.assertEqual(session.error_code, raw['error_code'])
        self.assertEqual(session.sampled_tracks, [])

        self.assertEqual(len(session.respiration_cycle_amplitudes), 7976)
        self.assertEqual(len(session.heartbeat), 5963)
        self.assertEqual(len(session.heart_rate), 460)
        self.assertEqual(len(session.signal_high_percentile), 544)
        self.assertEqual(len(session.repiration_cycles), 0)
        self.assertEqual(len(session.events), 2)
        self.assertEqual(len(session.actigram), 744)
        self.assertEqual(len(session.sensor_status), 1)
        self.assertEqual(len(session.snoring_events), 10)
        self.assertEqual(len(session.activity_segment_length), 303)
        self.assertEqual(len(session.high_activity_intervals), 113)
        self.assertEqual(len(session.activity_segment_variation), 303)
