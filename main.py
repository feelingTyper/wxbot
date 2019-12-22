# coding: utf8

import wxpy
from src import log
from src.conf import setting
from src.util.timer import Timer
from src.util.dynamic_import import Container
from src.tasks.keepAliveTask import KeepAliveTask
from src.tasks.syncUserTask import SyncUserTask


log.init_log('log/process')


timers = []
container = Container.instance()


def shutdown(signum, timers):
    for t in timers:
        t.stop()


# for s in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM, signal.SIGKILL]:
#     signal.signal(s, functools.partial(shutdown, s, timers))


def login_callback():
    pass
    # bot.file_helper.send_message('Hello')


def logout_callback():
    pass
    # bot.file_helper.send_message('Bye')


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
    msg_handlers = [
        'src.handlers.textMessageHandler.TextMessageHandler',
        'src.handlers.userHandler.UserHandler',
        'src.handlers.searchArticleHandler.SearchArticleHandler'
    ]
    msg_handlers = container.singletens(msg_handlers)
    for msg_handler in msg_handlers:
        msg_handler.run(msg)


timers.append(Timer(KeepAliveTask(bot), 1200, True))
timers.append(Timer(SyncUserTask(bot), 3600*3, True))

for t in timers:
    t.start()


bot.join()

shutdown(0, timers)
