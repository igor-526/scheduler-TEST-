import json
from pathlib import Path

import pytest

from scheduler import Scheduler

from settings import DEFAULT_API_URL


@pytest.fixture()
def response_mock_data():
    fixture_path = Path(__file__).parent / "fixtures" / "api_response.json"
    with open(fixture_path, "r") as f:
        data = json.load(f)
        return {"json": json.dumps(data),
                "data": data}


@pytest.fixture()
def scheduler_mock(response_mock, response_mock_data):
    with response_mock(f'GET {DEFAULT_API_URL} -> 200 :'
                       f'{response_mock_data["json"]}'):
        scheduler = Scheduler()
        return scheduler


@pytest.fixture()
def scheduler_nodata():
    scheduler = Scheduler(auto_fetch=False)
    return scheduler
