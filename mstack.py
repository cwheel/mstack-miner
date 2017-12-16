import json

from miners import MINER_TYPES
from api import API
from logger import Logger

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    config = json.load(open('config.json'))
    Miner = MINER_TYPES[config['miner']]

    es = Elasticsearch([config['elastic_host']])

    miner = Miner(
        config['miner_host'],
        config['miner_port'],
        config.get('miner_name', 'mstack-miner'),
    )

    Logger(config.get('log_interval', 60), miner, es).start()

    API(
        config.get('api_port', 3000),
        config['api_username'],
        config['api_password'],
        miner
    ).serve()
