import json

from miners import MINER_TYPES
from api import API
from watchdog import Watchdog

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

    push_service = Pushover(config['push_user_token'], config['push_app_token'])

    Watchdog(config.get('watchdog_interval', 60), miner, es, push_service).start()

    API(
        config.get('api_port', 3000),
        config['api_username'],
        config['api_password'],
        config['ssl_cert'],
        config['ssl_key'],
        miner
    ).serve()
