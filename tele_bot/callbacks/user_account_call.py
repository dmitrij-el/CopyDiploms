"""
Здесь хранятся колбэки профиля, которые реагируют на вызовы из telebot/keyboards/kb_user_profile.py.
Они вводят состояние, которое определяет поведение бота.
Также каждый колбэк после вызова сразу выполняет заложенный в него функционал,
до получения сообщения от пользователя.



"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tele_bot.data import text, db_funcs
from tele_bot.keyboards import kb_user_profile
from tele_bot.states.states import (StateMenu,
                                    StateUserProfile)

router = Router()


@router.callback_query(F.data == "create_error_profile")
async def create_error_profile(clbck: CallbackQuery):
    """
    Колбэк регистрации аккаунта в случае ошибки.
    Возвращает в меню профиля.
    """
    acc_dict = {
        'user_id': clbck.from_user.id,
        'name': clbck.from_user.first_name,
        'surname': clbck.from_user.last_name,
        'username': clbck.from_user.username
    }
    db_funcs.user_rec_datas_in_reg(acc_dict)
    await clbck.message.answer(text.account_menu_1,
                               reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await clbck.message.answer(text.account_menu_2,
                               reply_markup=kb_user_profile.user_profile(user_id=clbck.from_user.id))
    await state.set_state(StateMenu.profile)


@router.callback_query(F.data == "user_profile")
async def user_profile(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк профиля аккаунта.
    Возвращает в меню профиля.
    """
    await clbck.message.answer(text.account_menu_1,
                               reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await clbck.message.answer(text.account_menu_2,
                               reply_markup=kb_user_profile.user_profile(user_id=clbck.from_user.id))
    await state.set_state(StateMenu.profile)


@router.callback_query(F.data == "clear_profile")
async def clear_profile(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк очистки аккаунта.
    """
    await state.set_state(StateUserProfile.clear_profile)
    await clbck.message.answer(text.clear_account_question,
                               reply_markup=kb_user_profile.choice_delete_account(text.clear_account_question))


@router.callback_query(F.data == "change_name")
async def change_name(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения имени.
    """
    await state.set_state(state=StateUserProfile.change_name)
    await clbck.message.answer(text.update_profile_enter_data,
                               reply_markup=kb_user_profile.back_button(text.update_profile_enter_data))


@router.callback_query(F.data == "change_surname")
async def change_surname(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения фамилии.
    """
    await clbck.message.answer(text.update_profile_enter_data,
                               reply_markup=kb_user_profile.back_button(text.update_profile_enter_data))
    await state.set_state(StateUserProfile.change_surname)


@router.callback_query(F.data == "change_patronymic")
async def change_patronymic(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения отчество.
    """
    await state.set_state(StateUserProfile.change_patronymic)
    await clbck.message.answer(text.update_profile_enter_data,
                               reply_markup=kb_user_profile.back_button(text.update_profile_enter_data))


@router.callback_query(F.data == "change_date_birth")
async def change_date_birth(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения даты рождения.
    """
    await state.set_state(StateUserProfile.change_date_birth)
    await clbck.message.answer(text.update_profile_enter_data,
                               reply_markup=kb_user_profile.back_button(text.update_profile_enter_data))


@router.callback_query(F.data == "change_gender")
async def change_gender(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения пола.
    """
    await state.set_state(StateUserProfile.change_gender)
    await clbck.message.answer(text.update_gender,
                               reply_markup=kb_user_profile.choose_gender(text.update_profile_enter_data))


@router.callback_query(F.data == "change_height")
async def change_height(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения роста.
    """
    await state.set_state(StateUserProfile.change_height)
    await clbck.message.answer(text.update_profile_enter_data,
                               reply_markup=kb_user_profile.back_button(text.update_profile_enter_data))


@router.callback_query(F.data == "change_weight")
async def change_weight(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения веса.
    """
    await state.set_state(StateUserProfile.change_weight)
    await clbck.message.answer(text.update_profile_enter_data,
                               reply_markup=kb_user_profile.back_button(text.update_profile_enter_data))


@router.callback_query(F.data == "change_email")
async def change_email(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения электронной почты.
    """
    await state.set_state(StateUserProfile.change_email)
    await clbck.message.answer(text.update_email,
                               reply_markup=kb_user_profile.back_button(text.update_profile_enter_data))


@router.callback_query(F.data == "change_phone")
async def change_phone(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения номера телефона.
    """
    await state.set_state(StateUserProfile.change_phone)
    await clbck.message.answer(text.update_phone,
                               reply_markup=kb_user_profile.choose_phone(text.update_profile_enter_data))


@router.callback_query(F.data == "change_communication_channels")
async def change_communication_channels(clbck: CallbackQuery, state: FSMContext):
    """
    Колбэк изменения канала связи.
    """
    await state.set_state(StateUserProfile.change_communication_channels)
    await clbck.message.answer(text.update_communication_channels,
                               reply_markup=kb_user_profile.choose_communication_channels(
                                   text.update_profile_enter_data))
