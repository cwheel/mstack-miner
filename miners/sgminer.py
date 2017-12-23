import socket
import json

from miner import Miner

SOCKET_READ_LENGTH = 4096

class SgMiner(Miner):

    def _get_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self._host, self._port))
        except:
            return { 'error': Miner.DOWN }

        return sock

    def _run_command(self, cmd, expect_multiple = False):
        payload = { 'command': cmd }

        sock = self._get_socket()

        if sock is None:
            return {}

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
        except:
            return { 'error': Miner.BAD_RESPONSE }

        if expect_multiple:
            return json.loads(resp[:-1])[cmd.upper()]
        else:
            return json.loads(resp[:-1])[cmd.upper()][0]

    def host(self):
        host = self._run_command('version')

        if host.get('error'):
            return host

        return {
            'miner': host.get('Miner')
        }

    def config(self):
        config = self._run_command('config')

        if config.get('error'):
            return config

        return {
            'os': config.get('OS'),
            'pool_count': config.get('Pool Count'),
            'gpu_count': config.get('GPU Count')
        }

    def work_summary(self):
        summary = self._run_command('summary')

        if summary.get('error'):
            return summary

        return {
            'difficulty': summary.get('Difficulty Accepted'),
            'hash_rate_5s': summary.get('KHS 5s'),
            'hash_rate_avg': summary.get('KHS av'),
            'rejected_shares_percent': summary.get('Pool Rejected%'),
            'found_blocks': summary.get('Found Blocks'),
            'stale_shares_percent': summary.get('Pool Stale%'),
            'hardware_errors': summary.get('Hardware Errors'),
            'accepted_shares': summary.get('Accepted')
        }

    def gpus(self):
        devs_raw = self._run_command('devs',  expect_multiple = True)
        devs = []

        if devs_raw.get('error'):
            return devs_raw

        for dev in devs_raw:
            devs.append({
                'hash_rate_5s': dev.get('KHS 5s'),
                'temperature': dev.get('Temperature'),
                'clock_freq': dev.get('GPU Clock'),
                'status': dev.get('Status'),
                'fan_percent': dev.get('Fan Percent'),
                'accepted_shares': dev.get('Accepted'),
                'rejected_shares': dev.get('Rejected'),
                'raw_intensity': dev.get('RawIntensity')
            })

        return devs
