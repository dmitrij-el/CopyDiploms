import datetime
import logging

from peewee import (CharField, DateTimeField, SqliteDatabase, DateField,
                    IntegerField, BooleanField, ForeignKeyField)
from peewee import Model, InternalError, PrimaryKeyField


def create_models() -> None:
    """
    Создание БД
    :return: None
    """
    try:
        data_gender = [
            {'name': 'men', 'symbol': '♂️'},
            {'name': 'women', 'symbol': '♀️'}
        ]
        data_channels = [
            {'name': 'Telegram'},
            {'name': 'Whatsapp'},
            {'name': 'Viber'},
            {'name': 'Телефон', 'symbol': '📞'}
        ]
        data_video_channels = [
            {'name': 'Telegram'},
            {'name': 'Whatsapp'},
            {'name': 'GoogleMeet'}
        ]

        Gender.create_table()
        User.create_table()
        ChannelCom.create_table()
        VideoChannelCom.create_table()
        City.create_table()
        FavouriteCity.create_table()
        Winter.create_table()

        with db_beahea.atomic():
            for gender in Gender.select():
                gender.delete_instance()
            for channel in ChannelCom.select():
                channel.delete_instance()
            for video_channel in VideoChannelCom.select():
                video_channel.delete_instance()
            for data_dict in data_gender:
                Gender.create(**data_dict)
            for data_dict in data_channels:
                ChannelCom.create(**data_dict)
            for data_dict in data_video_channels:
                VideoChannelCom.create(**data_dict)
    except InternalError as pw:
        logging.error(pw)


db_beahea = SqliteDatabase('C:/Users/100Noutbukov/PycharmProjects/python_basic_diploma/tele_bot/data/database.db')


class BaseUserModel(Model):
    class Meta:
        database = db_beahea
        order_by = 'id'


class Gender(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)
    symbol = CharField(unique=True)

    class Meta:
        db_table = "gender"


class ChannelCom(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)
    symbol = CharField(null=True)

    class Meta:
        db_table = "channel_com"


class VideoChannelCom(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)
    symbol = CharField(null=True)

    class Meta:
        db_table = "video_channel_com"


class City(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)

    class Meta:
        db_table = "city"


class User(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    creation_time = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True)
    user_id = CharField(unique=True)
    username = CharField(null=True)
    name = CharField(max_length=63, null=True)
    surname = CharField(max_length=63, null=True)
    patronymic = CharField(max_length=63, null=True)
    date_birth = DateField(null=True)
    gender = ForeignKeyField(Gender, backref='user', null=True)
    height = IntegerField(null=True)
    weight = IntegerField(null=True)
    phone = CharField(unique=True, index=True, null=True)
    email = CharField(unique=True, index=True, null=True)
    communication_channels = ForeignKeyField(ChannelCom, backref='user', null=True)
    city = ForeignKeyField(City, backref='user', null=True)

    class Meta:
        db_table = "user"


class FavouriteCity(BaseUserModel):
    city = ForeignKeyField(City, backref='favourite_city', null=True)
    user = ForeignKeyField(User, backref='favourite_city', null=True)

    class Meta:
        db_table = "favourite_city"
        indexes = (
            (('user', 'city'), True),
        )


class Winter(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    creation_time = DateTimeField(default=datetime.datetime.now)
    city = ForeignKeyField(City, backref='winter', null=True)
    user = ForeignKeyField(User, backref='winter', null=True)
    date = DateField(null=True)
    temp_like = CharField(null=True)
    temp_min = CharField(null=True)
    temp_max = CharField(null=True)
    humidity = CharField(null=True)

    class Meta:
        db_table = "winter"


