import unittest
import json
import os
from datetime import datetime
from pytz import timezone
from beddit.sleep import Sleep


BASE_DIR = os.path.dirname(__file__)


class SleepTest(unittest.TestCase):
    @property
    def sleep_response(self):
        return json.load(open(os.path.join(BASE_DIR, 'fixtures/sleep.json')))

    def test_sleep(self):
        raw = self.sleep_response[0]
        sleep = Sleep(raw)
        jst = timezone('Asia/Tokyo')
        self.assertEqual(sleep.timezone, jst)
        self.assertEqual(sleep.date, datetime(2016, 8, 16).replace(tzinfo=jst))
        self.assertEqual(sleep.start, datetime.fromtimestamp(raw['start_timestamp'], tz=jst))
        self.assertEqual(sleep.end, datetime.fromtimestamp(raw['end_timestamp'], tz=jst))
        self.assertEqual(sleep.session_range_start, datetime.fromtimestamp(raw['session_range_start'], tz=jst))
        self.assertEqual(sleep.session_range_end, datetime.fromtimestamp(raw['session_range_end'], tz=jst))
        self.assertEqual(sleep.updated, datetime.fromtimestamp(raw['updated'], tz=jst))

        self.assertEqual(len(sleep.actigram), 497)
        self.assertEqual(len(sleep.sleep_event), 21)
        self.assertEqual(len(sleep.presence), 20)
        self.assertEqual(len(sleep.snoring_episodes), 20)
        self.assertEqual(len(sleep.nap_periods), 0)
        self.assertEqual(len(sleep.heart_rate_curve), 89)
        self.assertEqual(len(sleep.sleep_cycles), 146)

        properties = [
            "sleep_latency",
            "sleep_time_target",
            "total_sleep_score",
            "sensor_status",
            "sleep_score_version",
            "short_term_average_respiration_rate",
            "primary_sleep_period_away_episode_duration",
            "primary_sleep_period_away_episode_count",
            "total_nap_duration",
            "average_respiration_rate",
            "total_snoring_episode_duration",
            "activity_index",
            "signal_amplitude",
            "short_term_resting_heart_rate",
            "evening_HRV_index",
            "stage_duration_W",
            "clipping_duration",
            "single_person_setup",
            "resting_heart_rate",
            "all_night_HRV_index",
            "stage_duration_N",
            "stage_duration_A",
            "stage_duration_G",
            "morning_HRV_index",
            "stage_duration_R",
            "stage_duration_S",
            "sleep_efficiency"
        ]
        for p in properties:
            self.assertTrue(hasattr(sleep.property, p))
