import logging
from typing import Dict, Any
import datetime

import requests

from tele_bot.config.config import API_KEY_OPEN_WEATHER
from tele_bot.data import text
from tele_bot.data.text import err


def request_weather_period_day(city: str | None = None,
                               longitude: float | None = None,
                               latitude: float | None = None) -> dict[str, Any] | Any:
    """
    Получение информации о погоде на один день по городу или координатам.

    :param city: Название города
    :param longitude: Широта
    :param latitude: Долгота

    :return: Словарь с информацией о погоде на один день.
    """
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'type': 'like',
            'units': 'metric',
            'lang': 'ru',
            'APPID': API_KEY_OPEN_WEATHER
        }

        if city:
            params['q'] = city
        elif latitude and longitude:
            params['lon'] = longitude
            params['lat'] = latitude
        else:
            raise ValueError("Не указано название города или координат")
        req = requests.get(url=url, params=params)
        if req.status_code == 200:
            data = req.json()
            direction_degrees = wind_deg(int(data['wind']['deg']))
            answer = {
                "conditions": data['weather'][0]['description'],
                "temp": round(data['main']['temp'], 1),
                "temp_like": round(data['main']['feels_like'], 1),
                "temp_min": round(data['main']['temp_min'], 1),
                "temp_max": round(data['main']['temp_max'], 1),
                "humidity": data['main']['humidity'],
                "wind_speed": round(data['wind']['speed'], 1),
                "wind_deg": direction_degrees,
                "city": data['name']
            }
            return answer
        elif req.status_code == 404:
            if req.json()['message'] == 'city not found':
                return text.weather_city_not_found
            else:
                raise APIError(f"Ошибка при запросе к API: {req.text}")
        else:
            raise APIError(f"Ошибка при запросе к API: {req.status_code}")
    except Exception as error:
        logging.error(error)
        return None


def request_weather_period(city: str | None = None,
                           longitude: float | None = None,
                           latitude: float | None = None,
                           count_days: int = 1) -> dict[str, Any] | Any:
    """
    Получение информации о погоде на несколько дней, начиная с завтрашнего по городу или координатам.

    :param city: Название города
    :param longitude: Широта
    :param latitude: Долгота
    :param count_days: Количество дней, начиная с завтрашнего

    :return: Словарь с информацией о погоде.
    """
    try:
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'type': 'like',
            'units': 'metric',
            'lang': 'ru',
            'APPID': API_KEY_OPEN_WEATHER
        }

        if city:
            params['q'] = city
        elif latitude and longitude:
            params['lon'] = longitude
            params['lat'] = latitude
        else:
            raise ValueError("Не указано название города или координат")
        req = requests.get(url=url, params=params)
        if req.status_code == 200:
            datas = req.json()
            count = 0
            answer = {'city': datas['city']['name']}
            list_answer = []
            while True:
                data = datas['list'][count]
                date_time_now = datetime.datetime.now()
                count += 1
                date_time = datetime.datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
                days = date_time.date() - date_time_now.date()
                if date_time.hour in [6, 15, 21] and days.days <= count_days and days.days != 0:
                    direction_degrees = wind_deg(int(data['wind']['deg']))
                    list_answer.append({
                        "conditions": data['weather'][0]['description'],
                        "temp": round(data['main']['temp'], 1),
                        "temp_like": round(data['main']['feels_like'], 1),
                        "temp_min": round(data['main']['temp_min'], 1),
                        "temp_max": round(data['main']['temp_max'], 1),
                        "humidity": data['main']['humidity'],
                        "wind_speed": round(data['wind']['speed'], 1),
                        "wind_deg": direction_degrees,
                        "time": time_day(date_time),
                    })
                if count >= int(datas['list'].__len__() - 1):
                    break
            answer['list_datas'] = list_answer
            return answer
        elif req.status_code == 404:
            if req.json()['message'] == 'city not found':
                return text.weather_city_not_found
            else:
                raise APIError(f"Ошибка при запросе к API: {req.text}")
        else:
            raise APIError(f"Ошибка при запросе к API: {req.status_code}")
    except Exception as error:
        logging.error(error)
        return None


def wind_deg(direction_degrees: int) -> str:
    """
    Получение индекса ветра по углу

    :param direction_degrees: Угол ветра в градусах
    :return: Индекс ветра
    """

    wind_indirections = ("северный", "северо-восточный", "восточный", "юго-восточный",
                         "южный", "юго-западный", "западный", "северо-западный")
    direction = int((direction_degrees + 22.5) // 45 % 8)
    return wind_indirections[direction]


def time_day(date_time: datetime) -> str:
    """
    Функция преобразует время в виде datetime в период дня.

    :param date_time: Время в виде datetime
    :return: Период в виде строки
    """
    if date_time.hour == 6:
        return 'Утро'
    elif date_time.hour == 15:
        return 'День'
    elif date_time.hour == 21:
        return 'Вечер'
