import pytest

from scheduler import Scheduler


def test_nodata(scheduler_nodata: Scheduler):
    assert scheduler_nodata.schedule_data is None


def test_validation_date(scheduler_nodata: Scheduler):
    with pytest.raises(Scheduler.SchedulerError,
                       match="date must be set"):
        scheduler_nodata._validate_date(None)
    with pytest.raises(ValueError,
                       match="date must be a string"):
        scheduler_nodata._validate_date(15)
        scheduler_nodata._validate_date(True)
        scheduler_nodata._validate_date(False)
    with pytest.raises(ValueError,
                       match="Invalid date string. "
                             "Must be in format YYYY-MM-DD"):
        scheduler_nodata._validate_date("")
        scheduler_nodata._validate_date("15")
        scheduler_nodata._validate_date("0000-12-12")
        scheduler_nodata._validate_date("25-07-07")
        scheduler_nodata._validate_date("2025-7-7")
        scheduler_nodata._validate_date("2024-13-13")
        scheduler_nodata._validate_date("2024-04-32")
        scheduler_nodata._validate_date("40-25")


def test_validation_time(scheduler_nodata: Scheduler):
    with pytest.raises(Scheduler.SchedulerError,
                       match="time must be set"):
        scheduler_nodata._validate_time(None)
    with pytest.raises(ValueError,
                       match="time must be a string"):
        scheduler_nodata._validate_time(15)
        scheduler_nodata._validate_time(True)
        scheduler_nodata._validate_time(False)
    with pytest.raises(ValueError,
                       match="Invalid time string. Must be in format HH:MM"):
        scheduler_nodata._validate_time("")
        scheduler_nodata._validate_time("13:60")
        scheduler_nodata._validate_time("24:05")
        scheduler_nodata._validate_time("13-05")
        scheduler_nodata._validate_time("13 20")
        scheduler_nodata._validate_time("13")


def test_validation_url(scheduler_nodata: Scheduler):
    with pytest.raises(Scheduler.SchedulerError,
                       match="API URL must be set"):
        scheduler_nodata.api_url = None
        scheduler_nodata._validate_url()
    with pytest.raises(ValueError,
                       match="API URL must be a string"):
        ex_list = [True, False, 15]
        for ex in ex_list:
            scheduler_nodata.api_url = ex
            scheduler_nodata._validate_url()
    with pytest.raises(ValueError,
                       match="API URL is invalid"):
        invalid_urls = [
            "example.com",
            "www.example.com",
            "ftp://example.com",
            "http://",
            "https://.com",
            "http://example..com",
            "http://-example.com",
            "http://example-.com",
            "http://256.256.256.256",
            "http://1.2.3",
            "http://1.2.3.4.5",
            "http://example.com:abc",
            "http://example.com:123456",
            "http://example.com/ space",
            "http://example.com/?query=<>",
            "http://example.com/\n",
            "javascript:alert(1)",
            "data:text/html,<script>alert(1)</script>",
            ""
        ]
        for inv_url in invalid_urls:
            scheduler_nodata.api_url = inv_url
            scheduler_nodata._validate_url()


def test_validarion_dur_min(scheduler_nodata: Scheduler):
    with pytest.raises(Scheduler.SchedulerError,
                       match="duration_minutes must be set"):
        scheduler_nodata.find_slot_for_duration(None)
    with pytest.raises(ValueError,
                       match="duration_minutes must be an integer"):
        scheduler_nodata.find_slot_for_duration("a")
        scheduler_nodata.find_slot_for_duration(True)
        scheduler_nodata.find_slot_for_duration(False)
        scheduler_nodata.find_slot_for_duration(0.15)
    with pytest.raises(ValueError,
                       match="duration_minutes must be "
                             "positive and more than 0"):
        scheduler_nodata.find_slot_for_duration(0)
        scheduler_nodata.find_slot_for_duration(-1)


def test_no_fetched_data(scheduler_nodata: Scheduler):
    with pytest.raises(Scheduler.SchedulerError,
                       match="Schedule data didn't fetched"):
        scheduler_nodata.get_busy_slots()
        scheduler_nodata.get_free_slots()
        scheduler_nodata.is_available("2025-02-17",
                                      "17:30",
                                      "20:30")
        scheduler_nodata.find_slot_for_duration(60)
