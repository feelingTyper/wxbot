# -*- coding: utf-8 -*-

from .handler import Handler


class FriendsMessageHandler(Handler):
    def __init__(self):
        super(FriendsMessageHandler, self).__init__()

    def process(self, message):
        message.sender = message.card
        return message
