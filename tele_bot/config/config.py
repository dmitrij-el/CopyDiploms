"""
Конфигурационный файл для защиты ключей.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    exit('BOT_TOKEN отсутствует в переменных окружения')

ADMIN_LIST = os.getenv('ADMIN_LIST')
if ADMIN_LIST is None:
    exit('ADMIN_LIST отсутствует в переменных окружения')

SIS_ADMIN_LIST = os.getenv('SIS_ADMIN_LIST')
if SIS_ADMIN_LIST is None:
    exit('SIS_ADMIN_LIST отсутствует в переменных окружения')

API_KEY_RAPID = os.getenv('API_KEY_RAPID')
if API_KEY_RAPID is None:
    exit('API_KEY_RAPID отсутствует в переменных окружения')

API_URL_GIPHY = os.getenv('API_URL_GIPHY')
if API_URL_GIPHY is None:
    exit('API_URL_GIPHY отсутствует в переменных окружения')

API_KEY_OPEN_WEATHER = os.getenv('API_KEY_OPEN_WEATHER')
if API_KEY_OPEN_WEATHER is None:
    exit('API_KEY_OPEN_WEATHER отсутствует в переменных окружения')

API_HOST_RAPID_MICROSOFT_AZURE = "microsoft-translator-text.p.rapidapi.com"
API_URL_GIPHY = ''
API_URL_OPEN_WEATHER = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={latitude}&lon={longitude}&'
        'appid=' + API_KEY_OPEN_WEATHER + '&units=metric'
)
