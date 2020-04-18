""" test interop with jose for node """

# pylint: disable=wrong-import-order
from test.common import pub_keys, priv_keys, algs, pub_key, priv_key
from test import jwt_spec
from datetime import datetime, timedelta
from subprocess import Popen, PIPE
from calendar import timegm
from threading import Lock
from jwcrypto.common import base64url_decode, json_encode, json_decode

lock = Lock()

def spawn(cmd, parse_json):
    """ run node command """
    #pylint: disable=E1101
    with lock:
        p = Popen(["node", "-e", "fixtures=require('./test/fixtures');" + cmd],
                  stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if p.returncode == 0:
        return json_decode(stdout) if parse_json else stdout
    raise Exception(stderr if stderr else ('exited with {}'.format(p.returncode)))
    #pylint: enable=E1101

#pylint: disable=W0621
def generate(alg):
    """ return function which can generate token using jose """
    key = priv_keys[alg].get('default', priv_key)
    def f(claims, alg, lifetime=None, expires=None, not_before=None):
        """ generate token using jose """
        now = datetime.utcnow()
        return spawn(
            "fixtures.generate({now}, {header}, {claims}, {expires}, {not_before}, {key})".format(
                now=timegm(now.utctimetuple()),
                header=json_encode({'alg': alg}),
                claims=json_encode(claims),
                expires=timegm(((now + lifetime) if lifetime else expires).utctimetuple()),
                not_before=timegm((not_before or now).utctimetuple()),
                key=json_encode(base64url_decode(json_decode(key.export())['k']) if key.is_symmetric else key.export_to_pem(True, None))),
            False)
    return f

def verify(alg):
    """ return function which can verify token using jose """
    key = pub_keys[alg].get('default', pub_key)
    def f(sjwt, iat_skew=timedelta()):
        """ verify token using jose """
        r = spawn(
            "fixtures.verify({now}, {sjwt}, {iat_skew}, {key}, {alg})".format(
                now=timegm(datetime.utcnow().utctimetuple()),
                sjwt=json_encode(sjwt),
                iat_skew=iat_skew.total_seconds(),
                key=json_encode(base64url_decode(json_decode(key.export())['k']) if key.is_symmetric else key.export_to_pem()),
                alg=json_encode(alg)),
            True)
        return tuple(r)
    return f

for alg in algs:
    priv_keys[alg]['jose'] = generate(alg)
    pub_keys[alg]['jose'] = verify(alg)

jwt_spec.setup(['HS256', 'HS512', 'RS256', 'RS512', 'PS256', 'PS512'])

for alg in algs:
    del priv_keys[alg]['jose']
    del pub_keys[alg]['jose']
