from abc import ABCMeta
from abc import abstractmethod

class Miner(object):
    __metaclass__ = ABCMeta

    def __init__(self, host, port, miner_name):
        self._host = host
        self._port = port

        self.name = miner_name

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
