from flask import Flask
from flask import jsonify

class API(object):

    def __init__(self, port, miner):
        self.port = port
        self.miner = miner

    def serve(self):
        self._get_router().run(host='0.0.0.0', port=self.port)

    def _get_router(self):
        api = Flask(__name__)

        @api.route('/host')
        def host():
            return self.miner.host()

        @api.route('/config')
        def config():
            return jsonify(self.miner.config())

        @api.route('/work_summary')
        def work_summary():
            return jsonify(self.miner.work_summary())

        @api.route('/gpus')
        def gpus():
            return jsonify(self.miner.gpus())

        return api
