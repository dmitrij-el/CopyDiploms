from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tele_bot.keyboards import kb_user_profile, kb_weather
from tele_bot.data import db_funcs, text
from tele_bot.states.states import StateGen, StateWeatherMenu, StateMenu

router = Router()


@router.message(Command('start'))
async def reg_profile(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'start'. При вызове проверяет на наличие юзера.
    Если юзера нет записывает данные пользователя в БД.
    Если есть, предлагает обнулить данные.


    :param msg: Сообщение от пользователя
    :param state: Состояние бота

    """

    user_id = msg.from_user.id

    if db_funcs.check_user_datas(user_id=user_id):
        await msg.answer(text.greet_cont.format,
                         reply_markup=kb_user_profile.main_menu()
                         )
        await state.set_state(StateGen.menu)

    else:
        acc_dict = {
            'user_id': msg.from_user.id,
            'name': msg.from_user.first_name,
            'surname': msg.from_user.last_name,
            'username': msg.from_user.username
        }
        db_funcs.user_rec_datas_in_reg(acc_dict)
        if db_funcs.check_user_datas(user_id):
            await msg.answer(text.greet.format(name=msg.from_user.first_name))
            await msg.answer(text=text.greet_cont,
                             reply_markup=kb_user_profile.user_profile(user_id=user_id))
            await state.set_state(StateMenu.profile)
        else:
            await msg.answer('Произошла критическая ошибка при регистрации. Уведомите пожалуйста администратора.\n'
                             'Следующее сообщение будет отправлено администратору.')
            prompt = msg.text
            await msg.answer(text=prompt, reply_markup=kb_user_profile.main_menu())


@router.message(Command('hellow-world'))
async def reg_profile(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'hellow-world'. Отправляет приветственное сообщение и
    возвращает в главное меню.

    :param msg: Сообщение от пользователя
    :param state: Состояние бота
    """
    await msg.answer(text=text.greet.format(name=msg.from_user.first_name),
                     reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text=text.menu,
                     reply_markup=kb_user_profile.main_menu())
    await state.set_state(StateGen.menu)


@router.message(Command('main_menu'))
async def reg_profile(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'main_menu'. При вызове отправляет в главное меня.

    :param msg: Сообщение от пользователя
    :param state: Состояние бота
    """
    await msg.answer(text=text.command_found.format('"main_menu"'), reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text=text.menu, reply_markup=kb_user_profile.main_menu())
    await state.set_state(StateGen.menu)


@router.message(Command('weather_menu'))
async def reg_profile(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'weather_menu'. При вызове выводит меню прогноза погоды.

    :param msg: Сообщение от пользователя
    :param state: Состояние бота
    """
    await msg.answer(text=text.command_found.format('"weather_menu"'),
                     reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text=text.weather_menu, reply_markup=kb_weather.weather_main_menu(user_id=msg.from_user.id))
    await state.set_state(StateMenu.weather_menu)


@router.message(Command('help'))
async def send_help(msg: Message):
    """
    Отправляет список команд для использования.

    :param msg: Сообщение от пользователя
    """
    await msg.answer(text="Вот список команд для использования", reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text="""
/start - Запуск бота. Автоматически создается аккаунт. При повторном вызове предлагает сбросить профиль.
/main_menu - Выводит главное меню.
/weather_menu - Выводит меню прогноза погоды.
/hellow-world - Приветствие.
/help - Список команд
/info - вызов чата со службой поддержки.
Обратите внимание! Тех. поддержка не отвечает.".
""",
                     reply_markup=kb_user_profile.main_menu())


