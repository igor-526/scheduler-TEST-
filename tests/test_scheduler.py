import pandas as pd

from scheduler import Scheduler


def test_mock_data(scheduler_mock: Scheduler,
                   response_mock_data: dict):
    assert scheduler_mock.schedule_data == response_mock_data["data"]


def test__get_df_days(scheduler_mock: Scheduler):
    """Тест на корректность DataFrame"""
    df_days = scheduler_mock._get_df_days()
    assert isinstance(df_days["date"][0], pd.Timestamp)
    assert isinstance(df_days["start"][0], pd.Timestamp)
    assert isinstance(df_days["end"][0], pd.Timestamp)
    df_days = scheduler_mock._get_df_days(to_dt=False)
    assert isinstance(df_days["date"][0], str)
    assert isinstance(df_days["start"][0], str)
    assert isinstance(df_days["end"][0], str)
    assert len(df_days) == 5
    scheduler_mock.selected_date = "2025-02-17"
    df_days = scheduler_mock._get_df_days()
    assert len(df_days) == 1


def test__get_df_timeslots(scheduler_mock: Scheduler):
    """Тест на корректность DataFrame"""
    df_timeslots = scheduler_mock._get_df_timeslots()
    assert isinstance(df_timeslots["start"][0], pd.Timestamp)
    assert isinstance(df_timeslots["end"][0], pd.Timestamp)
    df_timeslots = scheduler_mock._get_df_timeslots(to_dt=False)
    assert isinstance(df_timeslots["start"][0], str)
    assert isinstance(df_timeslots["end"][0], str)
    assert len(df_timeslots) == 9
    scheduler_mock.selected_date = "2025-02-18"
    df_timeslots = scheduler_mock._get_df_timeslots()
    assert len(df_timeslots) == 4


def test_get_busy_slots(scheduler_mock: Scheduler):
    """Тест на корректность данных занятых таймслотов"""
    assert scheduler_mock.get_busy_slots() == [
        ['2025-02-15', '17:30', '20:00'],
        ['2025-02-15', '09:00', '12:00'],
        ['2025-02-16', '14:30', '18:00'],
        ['2025-02-16', '09:30', '11:00'],
        ['2025-02-17', '12:30', '18:00'],
        ['2025-02-18', '10:00', '11:00'],
        ['2025-02-18', '11:30', '14:00'],
        ['2025-02-18', '14:00', '16:00'],
        ['2025-02-18', '17:00', '18:00']
    ]
    assert scheduler_mock.get_busy_slots("2025-02-15") == [
        ['17:30', '20:00'],
        ['09:00', '12:00']
    ]
    assert scheduler_mock.get_busy_slots("2025-02-16") == [
        ['14:30', '18:00'],
        ['09:30', '11:00']
    ]
    assert scheduler_mock.get_busy_slots("2025-02-17") == [['12:30', '18:00']]
    assert scheduler_mock.get_busy_slots("2025-02-18") == [
        ['10:00', '11:00'],
        ['11:30', '14:00'],
        ['14:00', '16:00'],
        ['17:00', '18:00']
    ]
    assert scheduler_mock.get_busy_slots("2025-02-19") == []


def test_get_free_slots(scheduler_mock: Scheduler):
    """Тест на корректность данных свободных таймслотов"""
    assert scheduler_mock.get_free_slots() == [
        ('2025-02-15', '12:00', '17:30'),
        ('2025-02-15', '20:00', '21:00'),
        ('2025-02-16', '08:00', '09:30'),
        ('2025-02-16', '11:00', '14:30'),
        ('2025-02-16', '18:00', '22:00'),
        ('2025-02-17', '09:00', '12:30'),
        ('2025-02-18', '11:00', '11:30'),
        ('2025-02-18', '16:00', '17:00'),
        ('2025-02-19', '09:00', '18:00')
    ]
    assert scheduler_mock.get_free_slots("2025-02-15") == [
        ('12:00', '17:30'),
        ('20:00', '21:00')
    ]
    assert scheduler_mock.get_free_slots("2025-02-16") == [
        ('08:00', '09:30'),
        ('11:00', '14:30'),
        ('18:00', '22:00')
    ]
    assert scheduler_mock.get_free_slots("2025-02-17") == [('09:00', '12:30')]
    assert scheduler_mock.get_free_slots("2025-02-18") == [
        ('11:00', '11:30'),
        ('16:00', '17:00')
    ]
    assert scheduler_mock.get_free_slots("2025-02-19") == [('09:00', '18:00')]


def test_is_available(scheduler_mock: Scheduler):
    """Тест на корректность данных проверки свободного таймслота"""
    assert scheduler_mock.is_available("2025-02-15",
                                       "13:00",
                                       "17:00") is True
    assert scheduler_mock.is_available("2025-02-15",
                                       "12:00",
                                       "17:30") is True
    assert scheduler_mock.is_available("2025-02-15",
                                       "11:59",
                                       "17:30") is False
    assert scheduler_mock.is_available("2025-02-15",
                                       "12:00",
                                       "17:31") is False


def test_find_slot_for_duration(scheduler_mock: Scheduler):
    """Тест на корректность данных первого свободного таймслота"""
    assert scheduler_mock.find_slot_for_duration(120) == ('2025-02-15',
                                                          '12:00',
                                                          '17:30')
    assert scheduler_mock.find_slot_for_duration(480) == ('2025-02-19',
                                                          '09:00',
                                                          '18:00')
    assert scheduler_mock.find_slot_for_duration(600) is None
