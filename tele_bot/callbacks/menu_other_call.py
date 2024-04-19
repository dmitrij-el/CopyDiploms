"""
Здесь хранятся колбэки главного меню, которые реагируют на вызовы из telebot/keyboards/kb_user_profile.py.
Они вводят состояние, которое определяет поведение бота.
Также каждый колбэк после вызова сразу выполняет заложенный в него функционал,
до получения сообщения от пользователя.


"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tele_bot.keyboards import kb_user_profile
from tele_bot.data import text


from tele_bot.states.states import StateGen

router = Router()


@router.callback_query(F.data == "menu")
async def menu(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк Главного меню.
    """
    await state.set_state(StateGen.menu)
    await clbck.message.answer(text=text.close_all_keyboards, reply_markup=ReplyKeyboardRemove())
    await clbck.message.answer(text.menu, reply_markup=kb_user_profile.main_menu())
