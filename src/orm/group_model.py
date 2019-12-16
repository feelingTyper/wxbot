# coding: utf-8

import peewee as pw

from .model import Model
from .database_factory import DatabaseFactory


db = DatabaseFactory.instance().get_conn('write')


class GroupModel(Model):
    group_id = pw.FixedCharField(max_length=32, null=False)
    user_id = pw.FixedCharField(max_length=32, null=False)
    group_name = pw.FixedCharField(max_length=120, null=False)
    user_display = pw.FixedCharField(max_length=120, default=None, null=True)
    extension = pw.FixedCharField(max_length=1024, null=True)
    create_time = pw.IntegerField(null=False)
    update_time = pw.IntegerField(null=False)

    class Meta:
        database = db
        table_name = 'groups'
