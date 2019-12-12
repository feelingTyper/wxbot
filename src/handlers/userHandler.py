import wxpy
import json
import time
import logging

from .handler import Handler
from ..orm.user_model import UserModel
from ..conf import setting

from playhouse.shortcuts import model_to_dict


class UserHandler(Handler):
    def __init__(self):
        super(UserHandler, self).__init__()

    def process(self, message):
        sender = message.sender
        if isinstance(message.sender, wxpy.Group):
            sender = message.member
        try:
            UserModel.select().where(
                    UserModel.user_id == sender.puid).get()
        except Exception:
            avatar_url = '{path}/pics/{puid}_{nick}.jpg'.format(
                    path=setting.app_path,
                    puid=sender.puid,
                    nick=sender.nick_name
            )
            sender.get_avatar(save_path=avatar_url)

            userModel = UserModel(
                user_id=sender.puid,
                nick_name=sender.nick_name,
                remark_name=sender.remark_name,
                avatar_url=avatar_url,
                type=setting.robot,
                extension=json.dumps(sender.raw),
                create_time=int(time.time()),
                update_time=int(time.time()),
            )
            logging.info(model_to_dict(userModel))
            logging.info('insert new user')
            print(model_to_dict(userModel))
            userModel.save()
