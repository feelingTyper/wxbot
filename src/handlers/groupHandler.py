import wxpy
import time
import logging

from .handler import Handler
from ..orm.group_model import GroupModel

from playhouse.shortcuts import model_to_dict


class GroupHandler(Handler):
    def __init__(self):
        super(GroupHandler, self).__init__()

    def process(self, message):
        sender = message.sender
        if not isinstance(message.sender, wxpy.Group):
            return message

        if message.type is wxpy.TEXT:
            self.save(sender)
        if message.type is wxpy.NOTE:
            self.update(sender)
        return message

    def save(self, group):
        try:
            GroupModel.select().where(
                    GroupModel.group_id == group.puid).get()
        except Exception:
            groups = []
            for member in group.members:
                groups.append(model_to_dict(GroupModel(
                    group_id=group.puid,
                    group_name=group.name,
                    user_id=member.puid,
                    user_display=member.name,
                    extension='',
                    create_time=int(time.time()),
                    update_time=int(time.time()),
                )))
            GroupModel.insert_many(groups).execute()
            logging.info('insert new group')

    def update(self, group):
        groups = []
        for member in group.members:
            try:
                (GroupModel.select()
                           .where(GroupModel.user_id == member.puid)
                           .where(GroupModel.group_id == group.puid)
                           .get())
            except Exception:
                groups.append(model_to_dict(GroupModel(
                    group_id=group.puid,
                    group_name=group.name,
                    user_id=member.puid,
                    user_display=member.name,
                    extension='',
                    create_time=int(time.time()),
                    update_time=int(time.time()),
                )))

        if len(groups):
            GroupModel.insert_many(groups).execute()
            logging.info('insert new group users')
