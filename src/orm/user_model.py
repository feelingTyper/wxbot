# coding: utf-8

import peewee as pw

from .model import Model
from .database_factory import DatabaseFactory


db = DatabaseFactory.instance().get_conn('write')


class UserModel(Model):
    user_id = pw.FixedCharField(max_length=32, null=False)
    nick_name = pw.FixedCharField(max_length=120, null=False)
    remark_name = pw.FixedCharField(max_length=120, default=None, null=True)
    city = pw.FixedCharField(max_length=32, default=None, null=True)
    province = pw.FixedCharField(max_length=32, default=None, null=True)
    country = pw.FixedCharField(max_length=32, default=None, null=True)
    avatar_url = pw.FixedCharField(max_length=255, default=None, null=True)
    gender = pw.IntegerField(default=0, null=False)
    signature = pw.FixedCharField(max_length=255, default=None, null=True)
    type = pw.SmallIntegerField(default=None, null=False)
    extension = pw.FixedCharField(max_length=2048, null=True)
    create_time = pw.IntegerField(null=False)
    update_time = pw.IntegerField(null=False)

    class Meta:
        database = db
        table_name = 'user_info'
