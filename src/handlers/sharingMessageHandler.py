# -*- coding: utf-8 -*-

import json
import wxpy
import logging

from .handler import Handler
from ..conf import setting
from ..orm.message_model import MessageModel
from ..util import util

from playhouse.shortcuts import model_to_dict


class SharingMessageHandler(Handler):
    def __init__(self):
        super(SharingMessageHandler, self).__init__()

    def process(self, message):
        sender = message.sender
        if isinstance(message.sender, wxpy.Group):
            sender = message.member

        createTime = util.datetime2timestamp(message.create_time)
        receiveTime = util.datetime2timestamp(message.receive_time)
        extension = {
            'url': message.url,
            'desc': util.message_desc(message.raw.content)
        }
        messageModel = MessageModel(
                user_id=sender.puid,
                sender=sender.name,
                sender_nick=sender.nick_name,
                group_name=message.sender.name,
                receiver=message.receiver.name,
                message_id=message.id,
                type=setting.MSG_TYPES.index(message.type),
                content=message.text,
                create_time=createTime,
                receive_time=receiveTime,
                extension=json.dumps(extension, ensure_ascii=False),
                )
        logging.info(model_to_dict(messageModel))
        messageModel.save()

        return message
