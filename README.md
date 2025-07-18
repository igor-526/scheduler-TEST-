<div id="header" align="center">
  <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHc5YmZmNjNhZjdxbWltdzhyZzVlb2I4a29wbjJubm4yYWRtOGRsNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Xa5hvKCuiZqV7ldUyV/giphy.gif" width="200"/>
</div>

<div id="badges" align="center">
  <a href="https://t.me/devil_on_the_wheel">
    <img src="https://img.shields.io/badge/telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Badge"/>
  </a>
  <a href="https://wa.me/+79117488008">
    <img src="https://img.shields.io/badge/whatsapp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="Whatsapp Badge"/>
  </a>
  <a href="https://www.linkedin.com/in/igor526/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge"/>
  </a>
  <a href="igor-526@yandex.ru">
    <img src="https://img.shields.io/badge/email-orange?style=for-the-badge&logo=mail.ru&logoColor=white" alt="Email Badge"/>
  </a>
</div>

<div id="view_counter" align="center">
  <img src="https://komarev.com/ghpvc/?username=igor-526&color=blue&style=for-the-badge&label=ПРОСМОТРЫ ПРОФИЛЯ"/>
</div>

# 🕒 Schedule Manager

Библиотека для работы с таймслотами в расписании, полученным по API

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white&style=for-the-badge&labelColor=3776AB&colorA=2C3E50)
![Pandas](https://img.shields.io/badge/Data_Analysis-Pandas-130654?style=for-the-badge&logo=pandas)
![Pytest](https://img.shields.io/badge/Testing(Cov=91%25)-Pytest-0A9EDC?style=for-the-badge&logo=pytest)

---

## 📅 Функционал

- **🔴 Просмотр всех занятых таймслотов**
- **🟢 Просмотр всех свободных таймслотов**
- **✅ Проверка таймслота на доступность**
- **🔍 Определение первого свободного таймслота**

---

## 🚀 Запуск проекта

### 1. 📦 Установка зависимостей (UV)
**Windows**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
**MacOS and Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. ⎇ Клонирование проекта
```bash
git clone https://github.com/igor-526/scheduler-TEST-.git
```

### 3. 🏗️ Настройка окружения
```bash
cd scheduler-TEST-
uv sync
.venv\Scripts\activate    # для Windows
source myenv/bin/activate # для MacOS или Linux
```

### ⚙️ 3. Настройки (/src/settings.py)
```ini
DEFAULT_API_URL     # API Endpoint для получения расписания по умолчанию
DATE_PATTERN        # Паттерн для валидации строки даты
TIME_PATTERN        # Паттерн для валидации строки времени
URL_PATTERN         # Паттерн для валидации URL адреса
```

### 🧪 4. Запуск тестов (91% покрытия)
**Тестирование функционала Scheduler**
```bash
    pytest tests/test_scheduler.py -v
```
**Тестирование исключений Scheduler**
```bash
    pytest tests/test_scheduler_exceptions.py -v
```
**Тестирование API на корректную работу**
```bash
    pytest tests/test_api.py -v
```
**Комплексное тестирование**
```bash
    pytest -v
```

### 5. 🔄 Смена окружения
```bash
    uv sync --no-dev
```

## 📚 Документация
#### 📄 [Инструкция по использованию](./docs/usage_instruction.md)



