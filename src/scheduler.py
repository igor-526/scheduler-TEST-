import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import pandas as pd

import requests

from settings import (DATE_PATTERN,
                      DEFAULT_API_URL,
                      TIME_PATTERN,
                      URL_PATTERN)


class Scheduler:
    """Работа с таймслотами на основе API.

    Attributes:
        api_url (str): URL для API запроса.
        schedule_data (Dict[str, List[Dict[str, str | int]]]):
            ответ API на запрос.
        selected_date (datetime.datetime): Выбранная для обработки дата.
    """
    api_url: str
    schedule_data: Dict[str, List[Dict[str, str | int]]] | None
    selected_date: datetime | None

    class SchedulerError(Exception):
        """Вызывается в случае возникновения ошибок в работе библиотеки."""

        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None

        def __str__(self):
            return self.message if self.message else \
                "Unexcepted error in Schedule library"

    def __init__(self,
                 api_url: str = DEFAULT_API_URL,
                 auto_fetch: bool = True):
        self.api_url = api_url
        self.selected_date = None
        self._validate_url()
        if auto_fetch:
            self.schedule_data = self._fetch_schedule_data()
        else:
            self.schedule_data = None

    def _fetch_schedule_data(self) \
            -> Dict[str, List[Dict[str, str | int]]]:
        """
        Служебная функция для получения данных из запроса к API.

        Returns:
            Dict[str, List[Dict[str, str | int]]]
            {
                "days": [{"date": "2025-02-15",
                          "end": "21:00",
                          "id": 1,
                          "start": "09:00"}],
                "timeslots": [{"day_id": 1,
                               "end": "20:00",
                               "id": 1,
                               "start": "17:30"}]
            }

        Example:
            >> self.schedule_data = self._fetch_schedule_data()
        """
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response.json()

    def _validate_url(self) -> None:
        """
        Служебная функция для валидации URL.

        Raises:
            SchedulerError: если URL отсутствует.
            ValueError: если URL не является строкой.

        Example:
            >> self._validate_url()
        """
        if self.api_url is None:
            raise self.SchedulerError("API URL must be set")
        if not isinstance(self.api_url, str):
            raise ValueError("API URL must be a string")
        if not re.fullmatch(URL_PATTERN, self.api_url):
            raise ValueError("API URL is invalid")

    def _validate_date(
            self, date_string: str
    ) -> None:
        """
        Служебная функция для валидации даты.

        Args:
            date_string (str, example="2025-02-17"): Входные данные.

        Raises:
            SchedulerError: если date_string отсутствует.
            ValueError: если date_string не является строкой.
            ValueError: если date_string не прошёл валидацию.

        Example:
            >> self._validate_date("2025-02-17")
        """
        if date_string is None:
            raise self.SchedulerError("date must be set")
        if not isinstance(date_string, str):
            raise ValueError("date must be a string")
        if not re.fullmatch(DATE_PATTERN, date_string):
            raise ValueError(
                "Invalid date string. Must be in format YYYY-MM-DD"
            )

    def _validate_time(
            self, time_string: str
    ):
        """
        Служебная функция для валидации времени.

        Args:
            time_string (str, example="13:25"): Входные данные.

        Raises:
            SchedulerError: если time_string отсутствует.
            ValueError: если time_string не является строкой.
            ValueError: если time_string не прошёл валидацию.

        Example:
            >> self._validate_time("13:25")
        """
        if time_string is None:
            raise self.SchedulerError("time must be set")
        if not isinstance(time_string, str):
            raise ValueError("time must be a string")
        if not re.fullmatch(TIME_PATTERN, time_string):
            raise ValueError("Invalid time string. Must be in format HH:MM")

    def _get_df_days(
            self, to_dt=True
    ) -> pd.DataFrame:
        """
        Служебная функция для получения DataFrame состоящий
            из информации о днях работы.

        Args:
            to_dt (bool, default=True): Необходимо ли преобразовать
                поля date, start, end в Timestamp.

        Raises:
            SchedulerError: если нет данных из запроса.

        Returns:
            pd.DataFrame

        Example:
            >> df_days = self._get_df_days(to_dt=False)
        """
        if self.schedule_data is None:
            raise self.SchedulerError("Schedule data didn't fetched")
        df = pd.DataFrame(self.schedule_data["days"])
        if to_dt:
            df["start"] = pd.to_datetime(df["start"], format='%H:%M')
            df["end"] = pd.to_datetime(df["end"], format='%H:%M')
            df["date"] = pd.to_datetime(df["date"])
        if self.selected_date:
            df = df[df["date"] == self.selected_date]
        return df

    def _get_df_timeslots(
            self, to_dt=True
    ) -> pd.DataFrame:
        """
        Служебная функция для получения DataFrame состоящий из
            информации о занятых таймслотах.

        Args:
            to_dt (bool, default=True): Необходимо ли преобразовать
                поля date, start, end в Timestamp.

        Raises:
            SchedulerError: если нет данных из запроса.

        Returns:
            pd.DataFrame

        Example:
            >> df_timeslots = self._get_df_timeslots(to_dt=False)
        """
        if self.schedule_data is None:
            raise self.SchedulerError("Schedule data didn't fetched")
        df = pd.merge(pd.DataFrame(self.schedule_data["timeslots"]),
                      self._get_df_days()[["id", "date"]],
                      left_on='day_id',
                      right_on='id').drop(
            ["day_id", "id_x", "id_y"], axis=1
        )
        if to_dt:
            df["start"] = pd.to_datetime(df["start"], format='%H:%M')
            df["end"] = pd.to_datetime(df["end"], format='%H:%M')
        return df

    def _check_is_available(
            self, free_slots: List[List[str]],
            time_start: str, time_end: str
    ) -> bool:
        """
        Служебная функция для проверки слота на предмет занятости.

        Args:
            free_slots (List[List[str]]): список свободных слотов.
            time_start (datetime.datetime): время начала таймслота
                для проверки
            time_end (datetime.datetime): время окончания таймслота
                для проверки

        Returns:
            bool. True - если слот доступен, False - если не доступен

        Example:
            >> self._check_is_available(free_slots, '17:30', '20:30')
        """
        for timeslot in free_slots:
            if (datetime.strptime(timeslot[0], "%H:%M") <= time_start and
                    datetime.strptime(timeslot[1], "%H:%M") >= time_end):
                return True
        return False

    def get_busy_slots(
            self, date: Optional[str] = None
    ) -> List[List[str]]:
        """
        Функция для получения занятых таймслотов.

        Args:
            date (Optional[str], default=None, example="2025-02-17"):
                Дата для получения занятых слотов.

        Raises:
            SchedulerError: если нет данных для анализа или date отсутствует.
            ValueError: если date не является строкой или не прошёл валидацию.

        Returns:
            List[List[str]]
            [['2025-02-15', '17:30', '20:00']] (date is None)
            ['17:30', '20:00'] (date is not None)

        Example:
            >> scheduler = Scheduler()
            >> scheduler.get_busy_slots(date="2025-02-17")
        """
        if date:
            self._validate_date(date)
            self.selected_date = datetime.strptime(date, "%Y-%m-%d")
        timeslots = self._get_df_timeslots(False)
        if date:
            return timeslots.drop(["date"], axis=1).reindex(
                columns=["start", "end"]
            ).values.tolist()
        timeslots["date"] = timeslots["date"].dt.strftime("%Y-%m-%d")
        return timeslots.reindex(
            columns=["date", "start", "end"]
        ).values.tolist()

    def get_free_slots(
            self, date: Optional[str] = None
    ) -> List[Tuple[str, str, str] | Tuple[str, str]]:
        """
        Функция для получения свободных слотов.

        Args:
            date (Optional[str], default=None, example="2025-02-17"):
                Дата для получения свободных таймслотов.

        Raises:
            SchedulerError: если нет данных для анализа или date отсутствует.
            ValueError: если date не является строкой или не прошёл валидацию.

        Returns:
            List[Tuple[str, str, str]]
            [('2025-02-15', '17:30', '20:00')] (date is None)

            List[Tuple[str, str]]
            [('17:30', '20:00')] (date is not None)

        Example:
            >> scheduler = Scheduler()
            >> scheduler.get_free_slots(date="2025-02-17")
        """
        if date:
            self._validate_date(date)
            self.selected_date = datetime.strptime(date, "%Y-%m-%d")
        timeslots_df = self._get_df_timeslots()
        timeslots_df = timeslots_df.sort_values(
            ['date', 'start'] if date else 'start'
        )
        selected_days_df = self._get_df_days()
        for i in selected_days_df.index.values:
            start_ts = {'start': pd.to_datetime('00:00', format='%H:%M'),
                        'end': selected_days_df.loc[i].start,
                        'date': selected_days_df.loc[i].date}
            end_ts = {'start': selected_days_df.loc[i].end,
                      'end': pd.to_datetime('23:59', format='%H:%M'),
                      'date': selected_days_df.loc[i].date}
            timeslots_df = pd.concat([timeslots_df,
                                      pd.DataFrame([start_ts, end_ts])])
        timeslots_df = timeslots_df.sort_values(['date', 'start'])
        timeslots_df = timeslots_df.set_index(
            keys=pd.RangeIndex(start=1, stop=len(timeslots_df)+1)
        )
        free_slots = []
        for i in range(1, len(timeslots_df)):
            free_start = timeslots_df.iloc[i - 1]['end']
            free_end = timeslots_df.iloc[i]['start']
            if (free_start < free_end and
                    timeslots_df.iloc[i - 1]['date'] ==
                    timeslots_df.iloc[i]['date']):
                if date:
                    free_slots.append(
                        (free_start.strftime('%H:%M'),
                         free_end.strftime('%H:%M'))
                    )
                else:
                    free_slots.append(
                        (timeslots_df.iloc[i]['date'].strftime("%Y-%m-%d"),
                         free_start.strftime('%H:%M'),
                         free_end.strftime('%H:%M'))
                    )
        return free_slots

    def is_available(
            self, date: str, time_start: str, time_end: str
    ) -> bool:
        """
        Функция для проверки слота на предмет занятости.

        Args:
            date (str, example='2025-02-18'): список свободных слотов.
            time_start (str, example='17:30'): время начала таймслота
                для проверки
            time_end (str, example='20:30'): время окончания таймслота
                для проверки

        Raises:
            SchedulerError: если нет данных для анализа.
            SchedulerError: если date, time_start или time_end отсутствует.
            ValueError: если date, time_start или time_end не является
                строкой или не прошёл валидацию.

        Returns:
            bool. True - если слот доступен, False - если не доступен

        Example:
            >> scheduler = Scheduler()
            >> scheduler.is_available("2025-02-17", "17:30", "20:30")
        """
        self._validate_date(date)
        self._validate_time(time_start)
        self._validate_time(time_end)
        free_slots = self.get_free_slots(date)
        time_start = datetime.strptime(time_start, "%H:%M")
        time_end = datetime.strptime(time_end, "%H:%M")
        if time_start >= time_end:
            raise ValueError("Start time must be before end time")
        return self._check_is_available(free_slots, time_start, time_end)

    def find_slot_for_duration(
            self, duration_minutes: int
    ) -> Tuple[str, str, str] | None:
        """
        Функция для проверки слота на предмет занятости.

        Args:
            duration_minutes (int, example=120): количество минут,
            для которых необходимо найти свободный таймслот.

        Raises:
            SchedulerError: если нет данных для анализа.
            SchedulerError: если duration_minutes отсутствует.
            ValueError: duration_minutes не является int или менее 1.

        Returns:
            Tuple[str, str, str]. ('2025-02-15', '12:00', '17:30')
            None. Если свободный таймслот не найден

        Example:
            >> scheduler = Scheduler()
            >> scheduler.find_slot_for_duration(480)
        """
        if duration_minutes is None:
            raise self.SchedulerError("duration_minutes must be set")
        if not isinstance(duration_minutes, int):
            raise ValueError("duration_minutes must be an integer")
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be "
                             "positive and more than 0")
        free_slots = self.get_free_slots()
        for time_slot in free_slots:
            if (datetime.strptime(time_slot[1], "%H:%M") +
                    timedelta(minutes=duration_minutes) <=
                    datetime.strptime(time_slot[2], "%H:%M")):
                return time_slot
        return None
