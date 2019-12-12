import time
import logging
import threading


class Timer(threading.Thread):
    def __init__(self, task):
        super(Timer, self).__init__()
        self.task = task
        self.loop = True

    def run(self):
        while self.loop:
            try:
                self.task.run()
            except Exception:
                logging.warning('task run error')
            time.sleep(1000)

    def start(self):
        self.run()

    def stop(self):
        logging.info('timer stopping')
        self.loop = False
