from aiogram import F, Router
from aiogram.types import Message

from tele_bot.data import text
from tele_bot.keyboards import kb_user_profile

router = Router()


@router.message(F.text.in_({"Выйти в меню", "Главное меню"}))
async def menu(msg: Message):
    await msg.answer(text=text.close_all_keyboards, reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text.menu, reply_markup=kb_user_profile.main_menu())
