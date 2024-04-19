"""Набор функций для работы с базами данных"""

import logging
from typing import Tuple, Any

from tele_bot.data.models import User, City, db_beahea


def check_user_datas(user_id: int) -> bool:
    """Проверка БД на наличие пользователя

    :param user_id: ID пользователя
    :return: True если юзера есть в БД, иначе False
    """
    try:
        with db_beahea:
            user = User.select().where(User.user_id == user_id).get()
            if user:
                return True
            else:
                return False
    except Exception as exp:
        logging.error(f'В процессе проверки на наличие пользователя произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False


def user_get_data(user_id: int) -> User:
    """Подкачка данных пользователя из БД по ключу"""
    try:
        with db_beahea:
            user = User.select().where(User.user_id == user_id).get()
            return user
    except Exception as exp:
        logging.error(f'В процессе загрузки данных пользователя {user_id} произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')


def user_rec_datas_in_reg(acc_dict: dict) -> None:
    """Запись данных профиля в БД при регистрации

    :param acc_dict: Данные профиля
    :return: None
    """
    try:
        with db_beahea.atomic():
            User.create(**acc_dict)
    except Exception as exp:
        logging.error(f'В процессе записи пользователя {acc_dict["user_id"]} в БД произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')


def user_delete_datas(user_id: int) -> bool:
    """Удаление данных пользователя из БД

    :param user_id: ID пользователя
    :return: True при удачном удалении, иначе False
    """
    try:
        with db_beahea:
            user = User.get(User.user_id == user_id)
            user.delete_instance()
    except Exception as exp:
        logging.error(f'В процессе удаления пользователя {user_id} произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False
    try:
        user = User.select().where(User.user_id == user_id).get()
        if user:
            return False
        else:
            return True

    except Exception as exp:
        logging.error(exp)
        return True


def user_update_data(user_id: int, column_datas: str, data: str | int | bool) -> bool:
    """
    Функция обновления данных пользователя с фильтрами.

    :param user_id: ID пользователя
    :param column_datas: Имя обновляемой колонки
    :param data: Новые данные
    :return: True при удачном обновление, иначе False
    """
    try:
        with db_beahea:

            user = User.update({column_datas: data}).where(User.user_id == user_id)
            user.execute()
        return True
    except Exception as exp:
        logging.error(f'В процессе обновления данных пользователя {user_id} по ключу произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False


def city_check_in_user(user_id: int) -> str | bool:
    """Проверка юзера на наличие выбранного города.

    :param user_id: ID пользователя
    :return: Имя города если найден, иначе False
    """
    try:
        with db_beahea:
            user = User.select().where(User.user_id == user_id).get()
            if user:
                city_data = City.select().where(City.id == user.city).get()
                city_name = city_data.name
                return city_name
            else:
                return False
    except Exception as exp:
        logging.error(
            f'В процессе проверки на наличие города у пользователя {user_id} произошла непредвиденная ошибка\n'
            f'Ошибка: {exp}')
        return False


def city_check_db(city_name: str) -> int | str:
    """ Проверка на наличие города в БД, в случае отсутствия города в БД добавляем город.

    :param city_name: Название города
    :return: Идентификатор города если город есть, иначе False

    """
    try:
        city_name = city_name
        with db_beahea:
            city = City.select().where(City.name == city_name)
            if city:
                return city.get().id
            else:
                City.create(name=city_name)
                city = City.select().where(City.name == city_name).get()
                return city.id
    except Exception as exp:
        logging.error(f'Ошибка при проверке и добавлении города в БД: {exp}')
