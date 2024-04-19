import pymorphy3
import re

from tele_bot.data import text, models
from tele_bot.data.models import Gender, ChannelCom, db_beahea


def gender_func(*args: list) -> str | None:
    """
    Функция принимает данные для определения пола человека с помощью библиотеки pymorphy3
    :param args: Список с данными для определения пола

    :return: Одно из двух значений (men - мужской пол, women - женский). Если пол не определен, то возвращает None
    """
    masc = 0
    femn = 0
    for name in args:
        if name is not None:
            parsed_word = pymorphy3.MorphAnalyzer().parse(name)[0].tag.gender
            if parsed_word == "masc":
                masc += 1
            elif parsed_word == "femn":
                femn += 1
    if masc > femn:
        return "men"
    elif masc < femn:
        return "women"
    else:
        return None


def text_buttons_profile(user_data: models.User) -> dict:
    """
    Функция для формирования текстового интерфейса клавиатуры в меню профиля

    :param user_data: Вводные данные из базы данных
    :return: Текстовый интерфейс клавиатуры в меню
    """

    user_data_dict = user_data.__dict__['__data__']

    gender_id = user_data.gender
    genders_id = [gender.id for gender in Gender.select(Gender.id)]
    if gender_id == None:
        user_data_dict['gender'] = 'Пол'
    elif gender_id.id in genders_id:
        with db_beahea:
            gender = Gender.get(Gender.id == user_data.gender)
            gender_symbol = gender.symbol
            user_data_dict['gender'] = gender_symbol

    if user_data.name == None:
        user_data_dict['name'] = 'Имя'

    if user_data.surname == None:
        user_data_dict['surname'] = 'Фамилия'

    if user_data.patronymic == None:
        user_data_dict['patronymic'] = 'Отчество'

    if user_data.date_birth == None:
        user_data_dict['date_birth'] = 'Дата рождения'

    if user_data.height == None:
        user_data_dict['height'] = 'Рост'

    if user_data.weight == None:
        user_data_dict['weight'] = 'Вес'

    if user_data.email == None:
        user_data_dict['email'] = 'Email'

    if user_data.phone == None:
        user_data_dict['phone'] = 'Телефон'

    channel_id = user_data.communication_channels
    channels_id = [channel.id for channel in ChannelCom.select(ChannelCom.id)]
    if channel_id == None:
        user_data_dict['communication_channels'] = 'Канал связи'
    elif channel_id.id in channels_id:
        with db_beahea:
            channel = ChannelCom.get(ChannelCom.id == user_data.communication_channels)
            channel_name = channel.name
            user_data_dict['communication_channels'] = channel_name

    return user_data_dict


def check_data_func(electoral: str | int, mess: str) -> [bool, str]:
    """
    Функция проверки ввода данных аккаунта

    :param electoral: Название метода проверки
    
    :param mess: Текстовое сообщение для проверки на соответствие

    :return: Объект с информацией о результате проверки
    """

    if electoral in ['name', 'surname', 'patronymic']:
        if len(mess) > 63:
            return False, text.err_change_name
    elif electoral == 'date_birth':
        return checking_data_expression(date_birth=mess), text.err_change_date_birth
    elif electoral == 'height':
        print(mess)
        if int(mess) > 300 or int(mess) < 1:
            return False, text.err_change_height
    elif electoral == 'weight':
        if int(mess) < 1 or int(mess) > 300:
            return False, text.err_change_weight
    elif electoral == 'email':
        return checking_data_expression(email=mess), text.err_change_email
    elif electoral == 'phone':
        return checking_data_expression(phone_number=mess), text.err_change_phone
    return True, text.update_account_true


def checking_data_expression(phone_number: str | bool = False,
                             email: str | bool = False,
                             date_birth: str | bool = False) -> bool:
    """
    Проверка данных с помощью регулярных выражений. Выберите переменную из списка\n
    Номера телефона: phone_number\n
    Адреса электронной почты: email\n
    Имени пользователя: user_name

    :param phone_number: Номер телефона пользователя

    :param email: Адрес электронной почты пользователя

    :param date_birth: Дата рождения пользователя

    :return: Сравнивает и возвращает True или False
    """

    expressions_dir = {
        'date_birth':
            r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d',
        'phone_number':
            r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
        'email':
            r'^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$',
        'number_credit_card':
            r'[0-9]{13,16}',
        'weather_3_hours':
            r'\B'
    }
    expression = ''
    data = ''

    if date_birth:
        expression = expressions_dir["date_birth"]
        data = date_birth
    elif phone_number:
        expression = expressions_dir["phone_number"]
        data = phone_number
    elif email:
        expression = expressions_dir["email"]
        data = email

    result = re.compile(expression)
    if result.search(str(data)):
        return True
    else:
        return False
