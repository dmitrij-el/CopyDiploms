"""Сборник текстов для интерфейса взаимодействия с пользователем"""
before_greet = (
    '🧑‍⚕️Я - бот-помощник ')
greet = '{name}, давайте знакомиться!\n'
greet_cont = 'Я тестовый бот. В данный момент могу делать прогноз погоды и хранить ваши данные.'
command_found = 'Команда "{command}" выполнена'
close_all_keyboards = "Закрываем ненужные кнопки"
menu = "📍 Главное меню"
err = "🚫 К сожалению произошла ошибка, попробуйте позже"
api_err_request = 'Ошибка запроса к API. Попробуйте позже.'

account_menu_1 = 'Ваш профиль.'
account_menu_2 = 'Для изменения нажмите на соответствующую кнопку'
account_rec_datas = 'Подождите, данные записываются.'
clear_account_question = 'Хотите сбросить профиль?'
clear_account_true = 'Аккаунт очищен.'
clear_account_wait = 'Идет удаление аккаунта...'
clear_account_cancel = 'Очистка аккаунта отменена.'
update_profile_wait = 'Идет обновление данных...'
update_account_true = 'Обновление данных прошло успешно.'
update_account_false = 'При обновлении данных произошла ошибка.'
update_profile_enter_data = 'Введите новые данные.'
update_account_cancel = 'Изменение данных отменено.'
update_gender = 'Выберите ваш пол.'
update_communication_channels = 'Выберите предпочтительный канал связи.'
update_phone = 'Поделитесь своим контактом или введите номер телефона вручную.'
update_email = 'Введите email.'
profile_name = 'Ваше имя {user_name}'
profile_surname = 'Ваша фамилия {user_surname}'
profile_patronymic = 'Ваше отчество {user_patronymic}'
profile_date_birth = 'Ваша дата рождения {date_birth}'
profile_gender = 'Ваш пол {gender}'
profile_height = 'Ваш рост {height} см'
profile_weight = 'Ваш вес {weight} кг'
profile_email = 'Ваш email {email}'
profile_phone = 'Ваш телефон {phone}'
profile_communication_channel = 'Канал связи {communication_channel}'

err_err_change = '\nЕсли вы считаете что ошибки нету, просим написать администратору в личку.'
err_change_name = 'Ошибка. Для имени можно использовать любой набор символов менее 64 букв.' + err_err_change
err_change_date_birth = 'Ошибка. Дата рождения в формате ДД.ММ.ГГГГ или ДД/ММ/ГГГГ.' + err_err_change
err_change_gender = ('Ошибка. Для выбора пола воспользуйтесь кнопками ниже, или введите: '
                     '\n"men" - мужской, '
                     '\n"woman" - женский' + err_err_change
                     )
err_change_height = 'Ошибка. Укажите рост в сантиметрах.' + err_err_change
err_change_weight = 'Ошибка. Укажите вес в килограммах.' + err_err_change
err_change_email = 'Ошибка. Формат адреса электронной почты user@host.domain' + err_err_change
err_change_phone = 'Ошибка. Некорректный номер телефона' + err_err_change
err_change_communication_channels = ('Ошибка. Для выбора пола воспользуйтесь кнопками ниже, или введите: '
                                     '\n"telegram" - Telegram'
                                     '\n"discord" - Дискорд'
                                     '\n"email" - Почта'
                                     '\n"phone" - Мобильная связь' + err_err_change
                                     )

weather_menu = 'Выберите команду'
weather_datas_day = ('{city}\n'
                     'Температура: {temp} C\n'
                     'Ощущается: {temp_like} C\n'
                     'Влажность: {humidity} %\n'
                     'Скорость ветра: {wind_speed} м/с\n'
                     'Направление ветра: {wind_deg}\n')
weather_period = ('{time}\n'
                  'Температура: {temp} C\n'
                  'Ощущается: {temp_like} C\n'
                  'Влажность: {humidity} %\n'
                  'Скорость ветра: {wind_speed} м/с\n'
                  'Направление ветра: {wind_deg}\n')
weather_update_location = 'Поделитесь геолокацией или введите название города вручную.'
weather_enter_city = 'Введите название города.'
weather_city_not_found = 'Город с таким названием не обнаружен'
weather_get_data_false = 'Ошибка загрузки данных.'
weather_request_wait = 'Идет загрузка данных...'
weather_request_true = 'Загрузка данных прошла успешно.'
weather_request_false = 'При загрузке данных произошла ошибка.'
weather_favourite_city = 'Выберите город из списка.\nТакже вы можете добавить новый город.'
weather_delete_favourite_city = 'Выберите город для удаления из списка.'
weather_add_favourite_city_false = 'Город уже есть в списке избранных.'
weather_add_favourite_city_true = 'Город добавлен в список избранных.'
weather_add_favorite_city_stop = 'Достигнут лимит избранных городов.'

