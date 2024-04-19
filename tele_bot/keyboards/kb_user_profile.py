"""
Для удобства работы с ботом реализуется клавиатура.

Интерфейс главного меню.
Интерфейс навигации по профилю

"""

import logging

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

from tele_bot.data import db_funcs
from tele_bot.utils import easy_funcs
from tele_bot.data.models import User, Gender, ChannelCom, City, db_beahea


def main_menu() -> InlineKeyboardMarkup:
    menu_buttons = [
        [InlineKeyboardButton(text="Погода ", callback_data="weather_menu")],
        [InlineKeyboardButton(text="👤 Профиль ", callback_data="user_profile")]
    ]
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
    return menu_keyboard


def user_profile(user_id: int) -> InlineKeyboardMarkup:
    user_data = db_funcs.user_get_data(user_id=user_id)
    if user_data is None:
        logging.error(f'Не найдет профиль {user_id}')
        user_profile_buttons = [
            [InlineKeyboardButton(text="Что-то пошло не так, аккаунт не найден", callback_data="create_error_profile")]]

    else:
        filter_user_datas = easy_funcs.text_buttons_profile(user_data=user_data)
        user_profile_buttons = [
            [InlineKeyboardButton(text="{name}".format(name=filter_user_datas['name']), callback_data="change_name"),
             InlineKeyboardButton(text="{surname}".format(surname=filter_user_datas['surname']),
                                  callback_data="change_surname"),
             InlineKeyboardButton(text="{patronymic}".format(patronymic=filter_user_datas['patronymic']),
                                  callback_data="change_patronymic")],
            [InlineKeyboardButton(text="{date_birth}".format(date_birth=filter_user_datas['date_birth']),
                                  callback_data="change_date_birth"),
             InlineKeyboardButton(text="{gender}".format(gender=filter_user_datas['gender']),
                                  callback_data="change_gender"),
             InlineKeyboardButton(text="{height} (см)".format(height=filter_user_datas['height']),
                                  callback_data="change_height"),
             InlineKeyboardButton(text="{weight} (кг)".format(weight=filter_user_datas['weight']),
                                  callback_data="change_weight")],
            [InlineKeyboardButton(text="{email}".format(email=filter_user_datas['email']),
                                  callback_data="change_email"),
             InlineKeyboardButton(text="{phone}".format(phone=filter_user_datas['phone']),
                                  callback_data="change_phone"),
             InlineKeyboardButton(text="{communication_channels}".format(
                 communication_channels=filter_user_datas['communication_channels']),
                 callback_data="change_communication_channels")],
            [InlineKeyboardButton(text="Главное меню", callback_data="menu")]
        ]

    user_profile_keyboard = InlineKeyboardMarkup(inline_keyboard=user_profile_buttons)
    return user_profile_keyboard


def update_profile_menu() -> InlineKeyboardMarkup:
    update_profile_menu_buttons = [
        [InlineKeyboardButton(text="Главное меню", callback_data="menu"),
         InlineKeyboardButton(text="Отменить", callback_data="user_profile")]
    ]
    update_profile_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=update_profile_menu_buttons)
    return update_profile_menu_keyboard


def clear_profile_menu() -> InlineKeyboardMarkup:
    clear_profile_menu_buttons = [
        [InlineKeyboardButton(text="Главное меню", callback_data="menu"),
         InlineKeyboardButton(text="Профиль 👥", callback_data="user_profile")]
    ]
    clear_profile_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=clear_profile_menu_buttons)
    return clear_profile_menu_keyboard


def choice_delete_account(prompt) -> ReplyKeyboardMarkup:
    choice_delete_account_buttons = [[KeyboardButton(text="Да"),
                                      KeyboardButton(text="Нет")]]
    choice_delete_account_keyboard = ReplyKeyboardMarkup(keyboard=choice_delete_account_buttons,
                                                         resize_keyboard=True,
                                                         input_field_placeholder=prompt)
    return choice_delete_account_keyboard


def back_button(prompt) -> ReplyKeyboardMarkup:
    back_button_buttons = [[KeyboardButton(text="Отмена")]]
    back_button_keyboard = ReplyKeyboardMarkup(keyboard=back_button_buttons,
                                               resize_keyboard=True,
                                               input_field_placeholder=prompt)
    return back_button_keyboard


def choose_phone(prompt) -> ReplyKeyboardMarkup:
    choose_phone_buttons = [[KeyboardButton(text="📞 Отправить телефон", request_contact=True),
                             KeyboardButton(text="Отмена")]]
    choose_phone_keyboard = ReplyKeyboardMarkup(keyboard=choose_phone_buttons,
                                                resize_keyboard=True,
                                                input_field_placeholder=prompt)
    return choose_phone_keyboard


def choose_communication_channels(prompt) -> ReplyKeyboardMarkup:
    button_channels = [[]]
    with db_beahea:
        channels = ChannelCom.select()
        for channel in channels:
            button_channels[0].append(KeyboardButton(text=channel.name))
    button_channels.append([KeyboardButton(text='Отмена')])

    button_channels = ReplyKeyboardMarkup(keyboard=button_channels,
                                          resize_keyboard=True,
                                          input_field_placeholder=prompt)
    return button_channels


def choose_gender(prompt) -> ReplyKeyboardMarkup:
    button_gender = [[]]
    with db_beahea:
        genders = Gender.select()
        for gender in genders:
            button_gender[0].append(KeyboardButton(text=gender.symbol))
    button_gender.append([KeyboardButton(text='Отмена')])

    button_gender_keyboard = ReplyKeyboardMarkup(keyboard=button_gender,
                                                 resize_keyboard=True,
                                                 input_field_placeholder=prompt)
    return button_gender_keyboard


iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
