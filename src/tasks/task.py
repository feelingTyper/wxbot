# -*- coding: utf-8 -*-

from ..util.util import logit


class Task:
    def __init__(self):
        pass

    @logit
    def run(self, *args, **kwargs):
        self.process(*args, **kwargs)

    def process(self, *args, **kwargs):
        raise NotImplementedError('method process in Task not implemented')
