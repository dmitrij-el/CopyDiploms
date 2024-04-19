"""
Сборник реакций на сообщения пользователя в состояниях относящихся к аккаунту
"""
from aiogram import Router
from aiogram import flags
from aiogram.types import Message

from tele_bot.data import db_funcs, text
from tele_bot.data.models import User, Gender, ChannelCom
from tele_bot.keyboards import kb_user_profile
from tele_bot.states.states import StateMenu, StateUserProfile
from tele_bot.utils import easy_funcs

router = Router()


@router.message(StateMenu.profile)
@flags.chat_action("typing")
async def profile(msg: Message):
    """Меню аккаунта"""
    await msg.answer(text=text.account_menu_1, reply_markup=kb_user_profile.user_profile(msg.from_user.id))


@router.message(StateUserProfile.clear_profile)
async def clear_profile(msg: Message):
    """Очистка аккаунта"""
    prompt = msg.text
    if prompt == "Да":
        mess = await msg.answer(text.clear_account_wait)
        delete_acc = db_funcs.user_delete_datas(msg.from_user.id)
        if delete_acc:
            acc_dict = {
                'user_id': msg.from_user.id,
                'name': msg.from_user.first_name,
                'surname': msg.from_user.last_name,
                'username': msg.from_user.username
            }
            db_funcs.user_rec_datas_in_reg(acc_dict)
            await mess.answer(text=text.clear_account_true, reply_markup=kb_user_profile.ReplyKeyboardRemove())
        else:
            await mess.answer(text=text.err, reply_markup=kb_user_profile.ReplyKeyboardRemove())
        await mess.answer(text=text.menu, reply_markup=kb_user_profile.clear_profile_menu())
    elif prompt == "Нет":
        await msg.answer(text=text.clear_account_cancel, reply_markup=kb_user_profile.ReplyKeyboardMarkup())
        await msg.answer(text=text.menu, reply_markup=kb_user_profile.clear_profile_menu())


@router.message(StateUserProfile.change_name)
@flags.chat_action("typing")
async def change_name(msg: Message):
    """Изменение имени"""
    await change_datas(msg, change_data='name')


@router.message(StateUserProfile.change_surname)
@flags.chat_action("typing")
async def change_surname(msg: Message):
    """Изменение фамилии"""
    await change_datas(msg, change_data='surname')


@router.message(StateUserProfile.change_patronymic)
@flags.chat_action("typing")
async def change_patronymic(msg: Message):
    """Изменение отчества"""
    await change_datas(msg, change_data='patronymic')


@router.message(StateUserProfile.change_date_birth)
@flags.chat_action("typing")
async def change_date_birth(msg: Message):
    """Изменение даты рождения"""
    await change_datas(msg=msg, change_data='date_birth')


@router.message(StateUserProfile.change_gender)
@flags.chat_action("typing")
async def change_gender(msg: Message):
    """Изменение пола"""
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text.update_account_cancel, reply_markup=kb_user_profile.ReplyKeyboardRemove())
        await msg.answer(text=text.account_menu_1,
                         reply_markup=kb_user_profile.user_profile(user_id=msg.from_user.id))
    else:
        mess = await msg.answer(text.update_profile_wait)
        user = User.select().where(User.user_id == msg.from_user.id).get()
        genders = Gender.select()
        for data in [(gender.name, gender.symbol) for gender in genders]:
            if prompt in data:
                user.gender = Gender.select(Gender.id).where(Gender.name == data[0]).get()
                user.save()
                await mess.answer(text=text.update_account_true, reply_markup=kb_user_profile.ReplyKeyboardRemove())
                break
        else:
            await mess.answer(text=text.err_change_gender,
                              reply_markup=kb_user_profile.ReplyKeyboardRemove())
        await msg.answer(text.account_menu_1, reply_markup=kb_user_profile.user_profile(user_id=msg.from_user.id))


@router.message(StateUserProfile.change_height)
@flags.chat_action("typing")
async def change_height(msg: Message):
    """Изменение роста"""
    await change_datas(msg=msg, change_data='height')


@router.message(StateUserProfile.change_weight)
@flags.chat_action("typing")
async def change_weight(msg: Message):
    """Изменение веса"""
    await change_datas(msg=msg, change_data='weight')


@router.message(StateUserProfile.change_email)
@flags.chat_action("typing")
async def change_email(msg: Message):
    """Изменение адреса почты"""
    await change_datas(msg=msg, change_data='email')


@router.message(StateUserProfile.change_phone)
@flags.chat_action("typing")
async def change_phone(msg: Message):
    """Изменение номера телефона"""
    prompt = msg.text
    contact = msg.contact
    print(contact)
    if prompt:
        await change_datas(msg=msg, change_data='phone')
    elif contact:
        pass
    else:
        await msg.answer(text=text.err, reply_markup=kb_user_profile.ReplyKeyboardRemove())
        await msg.answer(text=text.account_menu_1, reply_markup=kb_user_profile.user_profile(msg.from_user.id))


@router.message(StateUserProfile.change_communication_channels)
@flags.chat_action("typing")
async def change_channel(msg: Message):
    """Изменение канала связи"""
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text.update_account_cancel, reply_markup=kb_user_profile.ReplyKeyboardRemove())
        await msg.answer(text=text.account_menu_1,
                         reply_markup=kb_user_profile.user_profile(user_id=msg.from_user.id))
    else:
        mess = await msg.answer(text.update_profile_wait)
        user = User.select().where(User.user_id == msg.from_user.id).get()
        channels = ChannelCom.select()
        for data in [channel.name for channel in channels]:
            if prompt in data:
                user.communication_channels = ChannelCom.select(ChannelCom.id).where(ChannelCom.name == prompt).get()
                user.save()
                await msg.answer(text=text.update_account_true, reply_markup=kb_user_profile.ReplyKeyboardRemove())
                break
        else:
            await mess.answer(text=text.err_change_gender,
                              reply_markup=kb_user_profile.ReplyKeyboardRemove())
        await msg.answer(text.account_menu_1_1, reply_markup=kb_user_profile.user_profile(user_id=msg.from_user.id))


async def change_datas(msg, change_data: str):
    """
    Асинхронная функция является центральной при изменении данных профиля пользователем.
    Она производит проверку данных с помощью electoral_func.
    Также предлагает отменить с помощью кнопки действие.

    :param msg: Чат
    :param change_data: Имя изменяемых данных

    :rtype:
    """
    prompt = msg.text

    if prompt == 'Отмена':
        await msg.answer(text.update_account_cancel, reply_markup=kb_user_profile.ReplyKeyboardRemove())
        await msg.answer(text=text.account_menu_1,
                         reply_markup=kb_user_profile.user_profile(user_id=msg.from_user.id))
    else:
        check_data_func = easy_funcs.check_data_func(electoral=change_data, mess=prompt)
        if check_data_func[0]:
            mess = await msg.answer(text=text.update_profile_wait)
            user_id = msg.from_user.id
            update_func = db_funcs.user_update_data(user_id=user_id, column_datas=change_data, data=prompt)
            if update_func:
                await mess.answer(text=text.update_account_true,
                                  reply_markup=kb_user_profile.ReplyKeyboardRemove())
            else:
                await mess.answer(text=text.update_account_false,
                                  reply_markup=kb_user_profile.ReplyKeyboardRemove())
            await msg.answer(text.account_menu_1, reply_markup=kb_user_profile.user_profile(user_id=msg.from_user.id))
        else:
            await msg.answer(text=check_data_func[1], reply_markup=kb_user_profile.ReplyKeyboardRemove())
            await msg.answer(text=text.account_menu_1, reply_markup=kb_user_profile.user_profile(user_id=msg.from_user.id))
