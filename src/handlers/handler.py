from ..util.util import logit


class Handler:
    def __init__(self):
        pass

    @logit
    def run(self, message):
        return self.process(message)

    def process(self, message):
        raise NotImplementedError('not implemented')
