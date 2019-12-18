# coding: utf-8

import os
import wxpy


handlers = {
    'user': 'src.handlers.userHandler.UserHandler'
}

MSG_HANDLERS = {
    wxpy.TEXT: [
        'src.handlers.textMessageHandler.TextMessageHandler',
        'src.handlers.userHandler.UserHandler',
        'src.handlers.groupHandler.GroupHandler'
    ],
    wxpy.MAP: 'src.handlers.mapMessageHandler.MapMessageHandler',
    wxpy.CARD: [
        'src.handlers.friendsMessageHandler.FriendsMessageHandler',
        'src.handlers.userHandler.UserHandler'
    ],
    wxpy.NOTE: 'src.handlers.groupHandler.GroupHandler',
    wxpy.SHARING: 'src.handlers.sharingMessageHandler.SharingMessageHandler',
    wxpy.PICTURE: 'src.handlers.pictureMessageHandler.PictureMessageHandler',
    wxpy.RECORDING: 'src.handlers.voiceMessageHandler.VoiceMessageHandler',
    wxpy.ATTACHMENT: 'src.handlers.fileMessageHandler.FileMessageHandler',
    wxpy.VIDEO: 'src.handlers.videoMessageHandler.VideoMessageHandler',
    wxpy.FRIENDS: [
        'src.handlers.friendsMessageHandler.FriendsMessageHandler',
        'src.handlers.userHandler.UserHandler'
    ],
}

robot = 4
answer_limit = 100

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
            'port': 3306,
            'charset': 'utf8mb4'
        }
    }
}


app_path = os.path.abspath(os.path.dirname(__file__)).split('src')[0]

question_pattern = ('\\?,？,谁是,吗,哪,怎么,如何,到底,究竟,是不是,能不能,'
                    '可不可以,多少,多久,多远,多快,哪些,还要,如何,咋回事')

search_url = ('https://songguojiankang.com/community/'
              'search?word={}')

article_url = 'https://h5.xiangyujiankang.com/community/article-share/{}'
answer_template = '【帮您找到了{}篇病友在相愈社区分享的经验】\n\n {}'
no_answer = '【很抱歉没有找到相关经验和问答】'

short_service = 'https://dwz.cn/admin/v2/create'
short_service = 'http://dwz.wailian.work/api.php'
dwz_header = {
    'Host': 'https://dwz.wailian.work',
    'Referer': 'http://dwz.wailian.work/',
}

sync_groups = {
    '454c1ad2': '8群|微医-女性乳腺健康交流群'
}

search_type_name = ['动态', '经验', '自媒体', '提问', '回答', '评论']
