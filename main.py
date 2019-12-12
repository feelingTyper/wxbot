# coding: utf8

import wxpy
from src import log
from src.conf import setting
from src.util.dynamic_import import Container


log.init_log('log/process')


def login_callback():
    pass


def logout_callback():
    pass


message = None
container = Container.instance()

bot = wxpy.Bot(
        cache_path=True,
        console_qr=True,
        login_callback=login_callback,
        logout_callback=logout_callback)
bot.enable_puid()


@bot.register(
        chats=[wxpy.Group, wxpy.FRIENDS, bot.file_helper],
        # msg_types=MSG_TYPES,
        except_self=False,
        run_async=True)
def listen_message(msg):
    global message
    message = msg
    print(msg.text, msg.type)
    deal_message(msg)


def deal_message(message):
    """
    :param message
    run message handlers
    """
    msg_handlers = setting.MSG_HANDLERS.get(message.type)
    msg_handlers = container.singletens(msg_handlers)

    for msg_handler in msg_handlers:
        msg_handler.run(message)


wxpy.embed()
