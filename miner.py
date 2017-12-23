from abc import ABCMeta
from abc import abstractmethod

class Miner(object):
    __metaclass__ = ABCMeta

    DOWN = 'miner_down'
    BAD_RESPONSE = 'miner_bad_response'

    def __init__(self, host, port, miner_name):
        self._host = host
        self._port = port

        self.name = miner_name

    def name(self):
        return self.name

    @abstractmethod
    def host(self):
        pass

    @abstractmethod
    def config(self):
        pass

    @abstractmethod
    def work_summary(self):
        pass

    @abstractmethod
    def gpus(self):
        pass
