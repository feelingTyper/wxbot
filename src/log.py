import os
import logging
import logging.handlers

# logging.basicConfig(level=logging.INFO)


def init_log(log_path, level=logging.INFO, when="D", backup=7,
             formatter="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
             datefmt="%m-%d %H:%M:%S"):

    formatter = logging.Formatter(formatter, datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)

    dirname = os.path.dirname(log_path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
