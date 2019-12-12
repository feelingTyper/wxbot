# coding: utf-8

import os
import wxpy


MSG_HANDLERS = {
    wxpy.TEXT: [
        'src.handlers.textMessageHandler.TextMessageHandler',
        'src.handlers.userHandler.UserHandler'
    ],
    wxpy.MAP: 'src.handlers.mapMessageHandler.MapMessageHandler',
    wxpy.CARD: 'src.handlers.cardMessageHandler.CardMessageHandler',
    wxpy.NOTE: 'src.handlers.noteMessageHandler.NoteMessageHandler',
    wxpy.SHARING: 'src.handlers.sharingMessageHandler.SharingMessageHandler',
    wxpy.PICTURE: 'src.handlers.pictureMessageHandler.PictureMessageHandler',
    wxpy.RECORDING: 'src.handlers.voiceMessageHandler.VoiceMessageHandler',
    wxpy.ATTACHMENT: 'src.handlers.fileMessageHandler.FileMessageHandler',
    wxpy.VIDEO: 'src.handlers.videoMessageHandler.VideoMessageHandler',
    wxpy.FRIENDS: 'src.handlers.friendsMessageHandler.FriendsMessageHandler',
}

robot = 4

MSG_TYPES = [
    wxpy.TEXT,
    wxpy.MAP,
    wxpy.CARD,
    wxpy.NOTE,
    wxpy.SHARING,
    wxpy.PICTURE,
    wxpy.RECORDING,
    wxpy.ATTACHMENT,
    wxpy.VIDEO,
    wxpy.FRIENDS,
]


database = {
    'write': {
        'name': 'src.orm.database_write.DatabaseWrite',
        'config': {
            'hostname': 'localhost',
            'user': 'root',
            'password': 'zhangliang',
            'timeout': 10,
            'database': 'wx_spider',
            'port': 3306
        }
    }
}


app_path = (os.path.abspath(os.path.dirname(__file__)).split('src')[0]
            + 'downloads')
