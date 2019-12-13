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
    # wxpy.NOTE: 'src.handlers.noteMessageHandler.NoteMessageHandler',
    wxpy.SHARING: 'src.handlers.sharingMessageHandler.SharingMessageHandler',
    wxpy.PICTURE: 'src.handlers.pictureMessageHandler.PictureMessageHandler',
    wxpy.RECORDING: 'src.handlers.voiceMessageHandler.VoiceMessageHandler',
    wxpy.ATTACHMENT: 'src.handlers.fileMessageHandler.FileMessageHandler',
    wxpy.VIDEO: 'src.handlers.videoMessageHandler.VideoMessageHandler',
    wxpy.FRIENDS: 'src.handlers.friendsMessageHandler.FriendsMessageHandler',
}

robot = 4
answer_limit = 100

MSG_TYPES = [
    wxpy.TEXT,
    wxpy.MAP,
    wxpy.CARD,
    # wxpy.NOTE,
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


app_path = os.path.abspath(os.path.dirname(__file__)).split('src')[0]

question_pattern = r'[?,？,什么,么,谁,吗,哪,怎么,如何,到底,究竟,是不是,能不能,可不可以,呢, \
多少,多久,多远,多快,哪些,还要,如何]'

search_url = ('https://songguojiankang.com/community/'
              'search?word={}&type=1')

article_url = 'https://songguojiankang.com/community/page/{}'
answer_template = '【帮您找到了{}篇病友在相遇社区分享的经验】\n\n {}'
no_answer = '【很抱歉没有找到相关经验和问答】'

short_service = 'https://dwz.cn/admin/v2/create'
short_service = 'http://dwz.wailian.work/api.php'
dwz_header = {
    'Cookie': 'PHPSESSID=816os662g51881vvmvp34grq91; Hm_lvt_fd97a926d52ef868e2d6a33de0a25470=1576223005; Hm_lpvt_fd97a926d52ef868e2d6a33de0a25470=1576223005; __tins__19242943=%7B%22sid%22%3A%201576223004616%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201576224804616%7D; __51cke__=; __51laig__=1',
    'Host': 'https://dwz.wailian.work',
    'Referer': 'http://dwz.wailian.work/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
