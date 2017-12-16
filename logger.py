import uuid

from time import sleep
from datetime import datetime
from threading import Thread

class Logger(Thread):
    def __init__(self, interval, miner, es):
         Thread.__init__(self)

         self.interval = interval
         self.miner = miner
         self.es = es

         self.es.indices.create(index='{}-gpus'.format(self.miner.name), ignore=400)
         self.es.indices.create(index='{}-work-summary'.format(self.miner.name), ignore=400)

    def run(self):
        self._run_loop()

    def _run_loop(self):
        sleep(self.interval)
        self._log()
        self._runLoop()

    def _log(self):
        gpus = self.miner.gpus()
        summary = self.miner.work_summary()

        for gpu in gpus:
            gpu['timestamp'] = datetime.now()

            self.es.create(
                index='{}-gpus'.format(self.miner.name),
                doc_type='gpu',
                id=str(uuid.uuid4()),
                body=gpu
            )

        summary['timestamp'] = datetime.now()
        self.es.create(
            index='{}-work-summary'.format(self.miner.name),
            doc_type='summary',
            id=str(uuid.uuid4()),
            body=summary
        )
