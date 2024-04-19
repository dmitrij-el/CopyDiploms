"""
Здесь хранятся колбэки прогноза погоды.
Они вводят состояние, которое определяет поведение бота.
Также каждый колбэк после вызова сразу выполняет заложенный в него функционал,
до получения сообщения от пользователя.
"""
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tele_bot.data import text, db_funcs
from tele_bot.data.models import User, City
from tele_bot.utils.API import weather
from tele_bot.keyboards import kb_weather
from tele_bot.states.states import (StateMenu,
                                    StateWeatherMenu)

router = Router()


@router.callback_query(F.data == "weather_menu")
async def clear_profile(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк меню прогноза погоды
    """
    city_check = db_funcs.city_check_in_user(user_id=clbck.from_user.id)
    if isinstance(city_check, str):
        weather_data = weather.request_weather_period_day(city=city_check)
        await clbck.message.answer(text=text.weather_datas_day.format(**weather_data),
                                   reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                             user_id=clbck.from_user.id))
        await state.set_state(StateMenu.weather_menu)
    else:
        await clbck.message.answer(text=text.weather_update_location,
                                   reply_markup=kb_weather.weather_update_location(prompt=text.weather_update_location))
        await state.set_state(StateWeatherMenu.weather_city_now)
