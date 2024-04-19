"""
Сборник реакций на сообщения пользователя в состояниях относящихся к прогнозу погоды
"""

from aiogram import Router, flags
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tele_bot.data import db_funcs, text
from tele_bot.data.models import User, Gender, ChannelCom, City, FavouriteCity
from tele_bot.keyboards import kb_user_profile, kb_weather
from tele_bot.states.states import StateMenu, StateWeatherMenu, StateGen
from tele_bot.utils import easy_funcs
from tele_bot.utils.API import weather

router = Router()


@router.message(StateMenu.weather_menu)
@flags.chat_action("typing")
async def weather_menu(msg: Message, state: FSMContext):
    """Меню прогноза погоды"""
    prompt = msg.text
    user = User.select(User.city).where(User.user_id == msg.from_user.id).get()
    if user:
        city_name = City.select().where(City.id == user.city).get()
    else:
        city_name = "Выберите город"
    if prompt == "Отмена":
        await mess.answer(text=text.menu, reply_markup=kb_user_profile.main_menu())
    elif prompt == "Погода на день":
        city_name = user.city.name
        await weather_data_with_prompt(msg=msg, prompt=city_name, state=state)
    elif prompt == "Погода на завтра":
        await weather_period(msg=msg, count_days=1, state=state)
    elif prompt == "{city_name}".format(city_name=city_name.name):
        await msg.answer(text=text.weather_update_location,
                         reply_markup=kb_weather.weather_update_location(text.weather_update_location))
        await state.set_state(StateWeatherMenu.weather_city_now)
    elif prompt == "Избранные города":
        await msg.answer(text=text.weather_favourite_city,
                         reply_markup=kb_weather.weather_favorite_city(user_id=msg.from_user.id))
        await state.set_state(StateWeatherMenu.weather_favourite_city)
    elif prompt == "Главное меню":
        await msg.answer(text=text.close_all_keyboards, reply_markup=kb_weather.ReplyKeyboardRemove())
        await msg.answer(text=text.menu, reply_markup=kb_user_profile.main_menu())
        await state.set_state(StateGen.menu)


@router.message(StateWeatherMenu.weather_city_now)
@flags.chat_action("typing")
async def weather_enter_city(msg: Message, state: FSMContext):
    """Выбор города"""
    prompt = msg.text
    geolocation = msg.location
    if geolocation:
        mess = await msg.answer(text.weather_request_wait)
        lat = geolocation.latitude
        lon = geolocation.longitude
        weather_data = weather.request_weather_period_day(latitude=lat, longitude=lon)
        city_name = weather_data['city']
        city_data = db_funcs.city_check_db(city_name)
        db_funcs.user_update_data(user_id=msg.from_user.id, column_datas='city', data=city_data)
        await mess.answer(text=text.weather_datas_day.format(**weather_data),
                          reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                    user_id=msg.from_user.id))
        await state.set_state(StateMenu.weather_menu)
    elif prompt != 'Отмена':
        await weather_data_with_prompt(msg=msg, prompt=prompt, state=state)
    else:
        await msg.answer(text=text.weather_menu,
                         reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                   user_id=msg.from_user.id))
    await state.set_state(StateMenu.weather_menu)


async def weather_data_with_prompt(msg: Message, prompt: str, state: FSMContext):
    """
    Функция прогноза погоды на данное время
    """
    mess = await msg.answer(text.weather_request_wait)
    weather_data = weather.request_weather_period_day(city=prompt)
    if isinstance(weather_data, str):
        await mess.answer(text=weather_data,
                          reply_markup=kb_weather.weather_main_menu(user_id=msg.from_user.id))
    else:
        city_data = db_funcs.city_check_db(weather_data['city'])
        if isinstance(city_data, int):
            db_funcs.user_update_data(user_id=msg.from_user.id, column_datas='city', data=city_data)
            await mess.answer(text=text.weather_datas_day.format(**weather_data),
                              reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                        user_id=msg.from_user.id))

        else:
            city_name = weather_data['city']
            city_data = db_funcs.city_check_db(city_name)
            db_funcs.user_update_data(user_id=msg.from_user.id, column_datas='city', data=city_data)
            await mess.answer(text=text.weather_datas_day.format(**weather_data),
                              reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                        user_id=msg.from_user.id))
    await state.set_state(StateMenu.weather_menu)


async def weather_period(msg: Message, state: FSMContext, count_days: int = 1):
    """Функция прогноза погоды на период.

    :param msg: Сообщение пользователя.
    :param state: Состояние.
    :param count_days: Количество дней для прогноза погоды, default == 1.
    """
    city_name = City.select().join(User).where(User.user_id == 204984112).get().name
    weather_data = weather.request_weather_period(city=city_name, count_days=count_days)
    if isinstance(weather_data, str):
        await msg.answer(text=weather_data,
                         reply_markup=kb_weather.weather_main_menu(user_id=msg.from_user.id))
    elif isinstance(weather_data, dict):
        await msg.answer(text=weather_data['city'])
        for data in weather_data['list_datas']:
            await msg.answer(text=text.weather_period.format(**data))
    else:
        await msg.answer(text=text.api_err_request)
    await state.set_state(StateMenu.weather_menu)


@router.message(StateWeatherMenu.weather_favourite_city)
@flags.chat_action("typing")
async def weather_enter_favorite_city(msg: Message, state: FSMContext):
    """Выбор города из избранных.
    Также возможно добавление города в список и удаление города из списка избранных
    """
    prompt = msg.text
    list_commands = []
    cnt_fav_city = 0
    user = User.select().where(User.user_id == msg.from_user.id).get()
    city_favorites = FavouriteCity.select().where(FavouriteCity.user_id == user.id)
    for city in city_favorites:
        cnt_fav_city += 1
        list_commands.append(city.city.name)
    if prompt in list_commands:
        city_data = City.select().where(City.name == prompt).get()
        db_funcs.user_update_data(user_id=msg.from_user.id, column_datas='city', data=city_data.id)
        weather_data = weather.request_weather_period_day(city=city_data.name)
        await msg.answer(text=text.weather_datas_day.format(**weather_data),
                         reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                   user_id=msg.from_user.id))
        await state.set_state(StateMenu.weather_menu)
    elif prompt == "Назад":
        await msg.answer(text=text.weather_menu,
                         reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                   user_id=msg.from_user.id))
        await state.set_state(StateMenu.weather_menu)
    elif prompt == "Удалить из списка":
        await msg.answer(text=text.weather_delete_favourite_city,
                         reply_markup=kb_weather.weather_delete_favorite_city(user_id=msg.from_user.id))
        await state.set_state(StateWeatherMenu.weather_delete_favourite_city)
    elif prompt.title() in ["Добавить активный город".title(), user.city.name]:
        if cnt_fav_city < 6:
            for city in city_favorites:
                if city.city.name == user.city.name:
                    await msg.answer(text=text.weather_add_favourite_city_false)
                    await state.set_state(StateWeatherMenu.weather_favourite_city)
            else:
                FavouriteCity.create(user_id=user.id, city_id=user.city)

                await msg.answer(text=text.weather_add_favourite_city_true,
                                 reply_markup=kb_weather.weather_favorite_city(prompt=text.weather_favourite_city,
                                                                               user_id=msg.from_user.id))
                await state.set_state(StateWeatherMenu.weather_favourite_city)
        else:
            await msg.answer(text=text.weather_add_favorite_city_stop,
                             reply_markup=kb_weather.weather_favorite_city(prompt=text.weather_favourite_city,
                                                                           user_id=msg.from_user.id))
            await state.set_state(StateWeatherMenu.weather_favourite_city)
    else:
        weather_data = weather.request_weather_period_day(city=prompt)
        if isinstance(weather_data, str):
            await msg.answer(text=weather_data,
                             reply_markup=kb_weather.weather_favorite_city(user_id=msg.from_user.id))
        else:
            city_data = db_funcs.city_check_db(weather_data['city'])
            if isinstance(city_data, int):
                if not FavouriteCity.select().where(FavouriteCity.user_id == user.id,
                                                    FavouriteCity.city_id == city_data):
                    FavouriteCity.create(user_id=user.id, city_id=city_data)
                    await msg.answer(text=text.weather_add_favourite_city_true,
                                     reply_markup=kb_weather.weather_favorite_city(prompt=text.weather_favourite_city,
                                                                                   user_id=msg.from_user.id))
                else:
                    await msg.answer(text=text.weather_city_not_found,
                                     reply_markup=kb_weather.weather_favorite_city(prompt=text.weather_favourite_city,
                                                                                   user_id=msg.from_user.id))
            else:
                city_name = weather_data['city']
                city_data = db_funcs.city_check_db(city_name)
                FavouriteCity.create(user_id=user.id, city_id=city_data)
                await mess.answer(text=text.weather_add_favourite_city_true,
                                  reply_markup=kb_weather.weather_favorite_city(prompt=text.weather_favourite_city,
                                                                                user_id=msg.from_user.id))
        await state.set_state(StateWeatherMenu.weather_favourite_city)


@router.message(StateWeatherMenu.weather_delete_favourite_city)
@flags.chat_action("typing")
async def weather_delete_favourite_city(msg: Message, state: FSMContext):
    """
    Удаление города из списка избранных городов.
    """
    prompt = msg.text
    list_commands = []
    user = User.select().where(User.user_id == msg.from_user.id).get()
    city_favorites = FavouriteCity.select().where(FavouriteCity.user_id == user.id)
    for city in city_favorites:
        list_commands.append(city.city.name)
    if prompt in list_commands:
        city_id = City.select().where(City.name == prompt).get().id
        fvr_city = FavouriteCity.delete().where(FavouriteCity.city_id == city_id,
                                                FavouriteCity.user_id == user.id)
        fvr_city.execute()
        await msg.answer(text=text.weather_favourite_city,
                         reply_markup=kb_weather.weather_favorite_city(user_id=msg.from_user.id))
        await state.set_state(StateWeatherMenu.weather_favourite_city)
    elif prompt == "Назад":
        await msg.answer(text=text.weather_menu,
                         reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                   user_id=msg.from_user.id))
        await state.set_state(StateMenu.weather_menu)
    else:
        await msg.answer(text=text.weather_city_not_found,
                         reply_markup=kb_weather.weather_delete_favorite_city())
        await state.set_state(StateWeatherMenu.weather_delete_favourite_city)
