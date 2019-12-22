# coding: utf-8

import peewee as pw

from .model import Model
from .database_factory import DatabaseFactory


db = DatabaseFactory.instance().get_conn('write')


class MessageModel(Model):
    user_id = pw.FixedCharField(max_length=32, null=False)
    sender = pw.FixedCharField(max_length=32, default=None, null=True)
    sender_nick = pw.FixedCharField(max_length=32, default=None, null=True)
    group_id = pw.FixedCharField(max_length=32, null=False)
    group_name = pw.FixedCharField(max_length=32, default=None, null=True)
    receiver = pw.FixedCharField(max_length=32, default=None, null=True)
    message_id = pw.FixedCharField(max_length=32, null=False)
    type = pw.SmallIntegerField(null=False)
    question = pw.SmallIntegerField(null=False)
    status = pw.SmallIntegerField(null=False, default=0)
    answer = pw.FixedCharField(max_length=32, null=True)
    content = pw.TextField(null=False)
    extension = pw.FixedCharField(max_length=2048, null=True)
    create_time = pw.IntegerField(null=False)
    receive_time = pw.IntegerField(null=False)

    class Meta:
        database = db
        table_name = 'messages'
