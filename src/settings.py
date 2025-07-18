import re

DEFAULT_API_URL = 'https://ofc-test-01.tspb.su/test-task/'
DATE_PATTERN = r'(20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
TIME_PATTERN = r'([01]\d|2[0-3]):([0-5]\d)'
URL_PATTERN = re.compile(
    r'^https?://'
    r'(?:'
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    r')'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)?$',
    re.IGNORECASE
)
