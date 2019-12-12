# coding: utf-8

import peewee


class DatabaseWrite(peewee.MySQLDatabase):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrite, self).__init__(
                host=kwargs['hostname'],
                user=kwargs['user'],
                passwd=kwargs['password'],
                database=kwargs['database'],
                port=kwargs['port'],
                charset='utf8')
