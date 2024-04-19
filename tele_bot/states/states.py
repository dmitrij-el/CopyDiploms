from aiogram.fsm.state import StatesGroup, State


"""
Стадии взаимодействия с ботом.

"""


class StateGen(StatesGroup):
    menu = State()


class StateMenu(StatesGroup):
    weather_menu = State()
    translator = State()
    profile = State()


class StateWeatherMenu(StatesGroup):
    weather_period_day = State()
    weather_city_now = State()
    weather_favourite_city = State()
    weather_delete_favourite_city = State()


class StateTranslator(StatesGroup):
    choosing_language = State()


class StateUserProfile(StatesGroup):
    change_name = State()
    change_surname = State()
    change_patronymic = State()
    change_date_birth = State()
    change_gender = State()
    change_height = State()
    change_weight = State()
    change_email = State()
    change_phone = State()
    change_communication_channels = State()
    clear_profile = State()




