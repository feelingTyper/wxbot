# coding: utf8

import wxpy
from src import log
from src.conf import setting
from src.util.timer import Timer
from src.util.dynamic_import import Container
from src.tasks.keepAliveTask import KeepAliveTask


log.init_log('log/process')


def login_callback():
    pass
    # bot.file_helper.send_message('Hello')


def logout_callback():
    pass
    # bot.file_helper.send_message('Bye')


message = None
container = Container.instance()

bot = wxpy.Bot(
        cache_path=True,
        console_qr=True,
        login_callback=login_callback,
        logout_callback=logout_callback)
bot.enable_puid()


@bot.register(
        chats=[wxpy.Group],
        msg_types=setting.MSG_TYPES,
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


@bot.register(
        chats=[bot.file_helper],
        # msg_types=setting.MSG_TYPES,
        except_self=False,
        run_async=True)
def file_helper(msg):
    global message
    message = msg
    print(msg.text, msg.type)
    msg_handlers = [
        'src.handlers.textMessageHandler.TextMessageHandler',
        'src.handlers.userHandler.UserHandler',
        'src.handlers.searchArticleHandler.SearchArticleHandler'
    ]
    msg_handlers = container.singletens(msg_handlers)
    for msg_handler in msg_handlers:
        msg_handler.run(message)


task = KeepAliveTask(bot)
timer = Timer(task, 1200, True)
timer.start()


wxpy.embed()

timer.stop()
