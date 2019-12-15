# -*- coding: utf-8 -*-

from .task import Task


class KeepAliveTask(Task):
    def __init__(self, bot):
        super(KeepAliveTask, self).__init__()
        self.bot = bot

    def process(self):
        fileHelper = self.bot.file_helper
        fileHelper.send('keeping alive')
