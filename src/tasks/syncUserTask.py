# -*- coding: utf-8 -*-

import time
import logging

from .task import Task
from ..conf import setting
from ..util.dynamic_import import Container


class SyncUserTask(Task):
    def __init__(self, bot):
        super(SyncUserTask, self).__init__()
        self.userHandler = (Container.instance()
                            .singletens(setting.handlers['user']))[0]
        self.bot = bot

    def process(self):
        for group in self.bot.groups():
            if group.puid in setting.sync_groups:
                self.sync_group_users(group)

    def sync_group_users(self, group):
        for member in group.members:
            self.sync_user(member)

    def sync_user(self, member):
        try:
            self.userHandler.save(member)
            time.sleep(1)
        except Exception:
            logging.exception('sync user[{}] fail'.format(member.name))
