# -*- coding: utf-8 -*-

import time
import logging
import threading

from ..tasks.task import Task


class Timer(threading.Thread):
    def __init__(self, task, seconds, loop=True):
        self.__runTime = seconds
        self.__task = task
        self.__loop = loop
        self.__elapsed = -1.0
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        threading.Thread.__init__(self)
        assert isinstance(task, Task), "tasks.task.Task type required"

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            time.sleep(0.1)
            self.__elapsed = self.__elapsed + 0.1
            if self.__elapsed > self.__runTime:
                self.__run()
                self.__elapsed = 0.0

    def __run(self):
        try:
            self.__task.run()
        except Exception:
            logging.exception('task running error')
        if not self.__loop:
            self.stop()

    def pause(self):
        self.__flag.clear()

    def is_pause(self):
        return self.__flag.isSet() is False

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()
        self.__elapsed = -1.0
        logging.info('timer is stopping')
