# -*- coding: utf-8 -*-

import re
import wxpy
import logging

from .handler import Handler
from ..conf import setting
from ..orm.message_model import MessageModel
from ..util import util

from playhouse.shortcuts import model_to_dict


class TextMessageHandler(Handler):
    def __init__(self):
        super(TextMessageHandler, self).__init__()
        self.messages = {}

    def process(self, message):
        sender = message.sender
        if isinstance(message.sender, wxpy.Group):
            sender = message.member

        target, content = self.pure(message)

        createTime = util.datetime2timestamp(message.create_time)
        receiveTime = util.datetime2timestamp(message.receive_time)
        messageModel = MessageModel(
            user_id=sender.puid,
            sender=sender.name,
            sender_nick=sender.nick_name,
            group_name=message.sender.name,
            receiver=target,
            message_id=message.id,
            type=setting.MSG_TYPES.index(message.type),
            question=util.question(message.text),
            answer=self.answer(message),
            content=content,
            create_time=createTime,
            receive_time=receiveTime,
            )
        logging.info(model_to_dict(messageModel))
        logging.info(
                'question answers: {}'.
                format(self.messages[message.sender.puid]))
        messageModel.save()

        return message

    def answer(self, message):
        question, answers = \
                self.messages.setdefault(message.sender.puid, [0, 0])
        answers += 1

        if answers > setting.answer_limit:
            question = 0
            answers = 0

        if util.question(message.text):
            question = message.id
            answers = 0

        self.messages[message.sender.puid] = [question, answers]

        return question

    def pure(self, message):
        target = message.receiver.puid

        if not re.search(r'@', message.text) or \
           not hasattr(message.sender, 'members'):
            return target, message.text

        members = message.sender.members
        for user in members:
            if re.search(user.name, message.text) or \
               re.search(user.nick_name, message.text):
                target = user.puid
                (message.text.replace(user.name, '')
                        .replace(user.nick_name, '')
                        .replace('@', ''))
                break
        return target, message.text
