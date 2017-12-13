import json

from miners import MINER_TYPES
from api import API

if __name__ == '__main__':
    config = json.load(open('config.json'))
    Miner = MINER_TYPES[config['miner']]

    miner = Miner(config['miner_host'], config['miner_port'])

    cmd_api = API(config['api_port'], miner)
    cmd_api.serve()
