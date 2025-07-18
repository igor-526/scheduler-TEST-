import re

import pytest

import requests

from settings import (DATE_PATTERN,
                      DEFAULT_API_URL,
                      TIME_PATTERN)

days_ids = []


def test_default_api():
    response = requests.get(DEFAULT_API_URL)
    assert response.status_code == 200
    if response.status_code != 200:
        pytest.skip("Дальнейшее прохождение теста нецелесообразно")
    schedule_data = response.json()
    assert "days" in schedule_data
    assert "timeslots" in schedule_data
    if "days" in schedule_data:
        for day in schedule_data["days"]:
            assert "id" in day
            assert "date" in day
            assert "start" in day
            assert "end" in day
            if "id" in day:
                assert isinstance(day["id"], int)
                assert day["id"] > 0
            days_ids.append(day["id"])
            if "date" in day:
                assert re.fullmatch(DATE_PATTERN, day["date"])
            if "start" in day:
                assert re.fullmatch(TIME_PATTERN, day["start"])
            if "end" in day:
                assert re.fullmatch(TIME_PATTERN, day["end"])
    if "timeslots" in schedule_data:
        for timeslot in schedule_data["timeslots"]:
            assert "id" in timeslot
            assert "day_id" in timeslot
            assert "start" in timeslot
            assert "end" in timeslot
            if "id" in timeslot:
                assert isinstance(timeslot["id"], int)
                assert timeslot["id"] > 0
            if "day_id" in timeslot:
                assert isinstance(timeslot["day_id"], int)
                assert timeslot["day_id"] > 0
                assert timeslot["day_id"] in days_ids
            if "start" in timeslot:
                assert re.fullmatch(TIME_PATTERN, timeslot["start"])
            if "end" in timeslot:
                assert re.fullmatch(TIME_PATTERN, timeslot["end"])
