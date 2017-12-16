import uuid

from flask import Flask
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer

class API(object):

    def __init__(self, port, api_username, api_password, cert, key, miner):
        self.port = port
        self.miner = miner
        self.api_username = api_username
        self.api_password = api_password

        self.cert = cert
        self.key = key

        self.jwt = TimedJSONWebSignatureSerializer(str(uuid.uuid4()), expires_in=60*60*8)

    def serve(self):
        self._get_router().run(host='0.0.0.0', port=self.port, ssl_context=(self.cert, self.key))

    def _get_router(self):
        api = Flask(__name__)

        api_auth = HTTPBasicAuth()
        token_auth = HTTPTokenAuth('Bearer')

        @token_auth.verify_token
        def verify_token(token):
            return True
            try:
                sig = self.jwt.loads(token)
                print sig
            except:
                return False

            return sig.get('token_creator') == 'mstack-miner'

        @api_auth.verify_password
        def verify_creds(username, password):
            return username if username == self.api_username and password == self.api_password else None

        @api.route('/host')
        @token_auth.login_required
        def host():
            return self.miner.host()

        @api.route('/config')
        @token_auth.login_required
        def config():
            return jsonify(self.miner.config())

        @api.route('/work_summary')
        @token_auth.login_required
        def work_summary():
            return jsonify(self.miner.work_summary())

        @api.route('/gpus')
        @token_auth.login_required
        def gpus():
            return jsonify(self.miner.gpus())

        @api.route('/token')
        @api_auth.login_required
        def token():
            return self.jwt.dumps({'token_creator': 'mstack-miner'})

        return api
