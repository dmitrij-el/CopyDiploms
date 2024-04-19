"""
Для удобства работы с ботом реализуется клавиатура.
Интерфейс прогноза погоды.
"""
import logging

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

from tele_bot.data import db_funcs, text
from tele_bot.utils import easy_funcs
from tele_bot.data.models import User, Gender, ChannelCom, City, db_beahea, FavouriteCity, Winter


def weather_main_menu(user_id, prompt=text.weather_menu) -> ReplyKeyboardMarkup:
    user = User.select().where(User.user_id == user_id).get()
    city_data = City.select().where(City.id == user.city).get()
    if city_data:
        city_name = city_data.name
    else:
        city_name = 'Выберите город'
    weather_menu_buttons = [
        [KeyboardButton(text="Погода на день"),
         KeyboardButton(text="Погода на завтра"),
         # KeyboardButton(text="Погода на 3 дня")
         ],
        [KeyboardButton(text=f"{city_name}"),
         KeyboardButton(text="Избранные города")],
        [KeyboardButton(text="Главное меню")]
    ]

    weather_menu_keyboard = ReplyKeyboardMarkup(keyboard=weather_menu_buttons,
                                                resize_keyboard=True,
                                                input_field_placeholder=prompt)
    return weather_menu_keyboard


def weather_update_location(prompt=text.weather_update_location) -> ReplyKeyboardMarkup:
    weather_menu_buttons = [
        [KeyboardButton(text="Поделиться геолокацией", request_location=True),
         KeyboardButton(text="Отмена")]
    ]

    weather_menu_keyboard = ReplyKeyboardMarkup(keyboard=weather_menu_buttons,
                                                resize_keyboard=True,
                                                input_field_placeholder=prompt)
    return weather_menu_keyboard


def weather_favorite_city(user_id, prompt=text.weather_favourite_city) -> ReplyKeyboardMarkup:
    count = 0
    weather_menu_buttons = []
    user = User.select().where(User.user_id == user_id).get()
    city_favorites = FavouriteCity.select().where(FavouriteCity.user_id == user.id)
    for city in city_favorites:
        if count % 2 == 0:
            weather_menu_buttons.append([])
        cnt_list = count // 2
        weather_menu_buttons[cnt_list].append(KeyboardButton(text=city.city.name))
        count += 1
    menu_buttons = [KeyboardButton(text="Добавить активный город"),
                    KeyboardButton(text="Удалить из списка"),
                    KeyboardButton(text="Назад")]
    weather_menu_buttons.append(menu_buttons)
    weather_menu_keyboard = ReplyKeyboardMarkup(keyboard=weather_menu_buttons,
                                                resize_keyboard=True,
                                                input_field_placeholder=prompt)
    return weather_menu_keyboard


def weather_delete_favorite_city(user_id, prompt=text.weather_delete_favourite_city) -> ReplyKeyboardMarkup:
    count = 0
    weather_menu_buttons = []
    user = User.select().where(User.user_id == user_id).get()
    city_favorites = FavouriteCity.select().where(FavouriteCity.user_id == user.id)
    for city in city_favorites:
        if count % 2 == 0:
            weather_menu_buttons.append([])
        cnt_list = count // 2
        weather_menu_buttons[cnt_list].append(KeyboardButton(text=city.city.name))
        count += 1
    menu_buttons = [KeyboardButton(text="Назад")]
    weather_menu_buttons.append(menu_buttons)
    weather_menu_keyboard = ReplyKeyboardMarkup(keyboard=weather_menu_buttons,
                                                resize_keyboard=True,
                                                input_field_placeholder=prompt)
    return weather_menu_keyboard
