import uuid

from time import sleep
from datetime import datetime
from threading import Thread

from miner import Miner

class Watchdog(Thread):
    def __init__(self, interval, miner, es, push_service):
         Thread.__init__(self)

         self.interval = interval
         self.miner = miner
         self.es = es
         self.push_service = push_service

         self.es.indices.create(index='{}-gpus'.format(self.miner.name), ignore=400)
         self.es.indices.create(index='{}-work-summary'.format(self.miner.name), ignore=400)

    def run(self):
        self._run_loop()

    def _run_loop(self):
        sleep(self.interval)
        self._watch()
        self._run_loop()

    def _watch(self):
        gpus = self.miner.gpus()
        summary = self.miner.work_summary()

        if gpus.get('error') or summary.get('error'):
            self._notify_error(gpus.get('error', summary.get('error')))

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

    def _notify_error(self, errored_response):
        if errored_response.get('error') == Miner.DOWN:
            self.push_service.send_notification(
                'Miner {} appears to be unreachable'.format(self.miner.name()),
            )
        elif errored_response.get('error') == Miner.BAD_RESPONSE:
            self.push_service.send_notification(
                'Miner {} is issuing invalid API responses or none at all'.format(self.miner.name()),
            )
