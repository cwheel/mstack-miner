import socket
import json

from miner import Miner

SOCKET_READ_LENGTH = 4096

class SgMiner(Miner):

    def _get_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._host, self._port))

        return sock

    def _run_command(self, cmd, expect_multiple = False):
        payload = { 'command': cmd }

        sock = self._get_socket()
        sock.send(
            json.dumps(payload)
        )

        try:
            resp = sock.recv(SOCKET_READ_LENGTH)

            while True:
                next_resp = sock.recv(SOCKET_READ_LENGTH)

                if not next_resp:
                    break
                else:
                    resp += next_resp
        except socket.timeout:
            return {}

        if expect_multiple:
            return json.loads(resp[:-1])[cmd.upper()]
        else:
            return json.loads(resp[:-1])[cmd.upper()][0]

    def host(self):
        return self._run_command('version')['Miner']

    def config(self):
        config = self._run_command('config')

        return {
            'os': config['OS'],
            'pool_count': config['Pool Count'],
            'gpu_count': config['GPU Count']
        }

    def work_summary(self):
        summary = self._run_command('summary')

        return {
            'difficulty': summary['Difficulty Accepted'],
            'hash_rate_5s': summary['KHS 5s'],
            'hash_rate_avg': summary['KHS av'],
            'rejected_shares_percent': summary['Pool Rejected%'],
            'found_blocks': summary['Found Blocks'],
            'stale_shares_percent': summary['Pool Stale%'],
            'hardware_errors': summary['Hardware Errors'],
            'accepted_shares': summary['Accepted']
        }

    def gpus(self):
        devs_raw = self._run_command('devs',  expect_multiple = True)
        devs = []

        for dev in devs_raw:
            devs.append({
                'hash_rate_5s': dev['KHS 5s'],
                'temperature': dev['Temperature'],
                'clock_freq': dev['GPU Clock'],
                'status': dev['Status'],
                'fan_percent': dev['Fan Percent'],
                'accepted_shares': dev['Accepted'],
                'rejected_shares': dev['Rejected'],
                'raw_intensity': dev['RawIntensity']
            })

        return devs
