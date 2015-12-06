""" test interop with node-jsjws """

# pylint: disable=wrong-import-order
from test.common import pub_keys, priv_keys, algs, pub_pem, priv_pem
import json
from datetime import datetime, timedelta
from subprocess import Popen, PIPE
from calendar import timegm
from test import jwt_spec
from threading import Lock

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
        return json.loads(stdout) if parse_json else stdout
    else:
        raise Exception(stderr if stderr else ('exited with {}'.format(p.returncode)))
    #pylint: enable=E1101

#pylint: disable=W0621
def generate(alg):
    """ return function which can generate token using node-jsjws """
    key = priv_keys[alg].get('default', priv_pem)
    def f(claims, alg, lifetime=None, expires=None, not_before=None):
        """ generate token using node-jsjws """
        now = datetime.utcnow()
        return spawn(
            "fixtures.generate({now}, {header}, {claims}, {expires}, {not_before}, {key})".format(
                now=timegm(now.utctimetuple()),
                header=json.dumps({'alg': alg}),
                claims=json.dumps(claims),
                expires=timegm(((now + lifetime) if lifetime else expires).utctimetuple()),
                not_before=timegm((not_before or now).utctimetuple()),
                key=json.dumps(key)),
            False)
    return f

def verify(alg):
    """ return function which can verify token using node-jsjws """
    key = pub_keys[alg].get('default', pub_pem)
    def f(sjwt, iat_skew=timedelta()):
        """ verify token using node-jsjws """
        r = spawn(
            "fixtures.verify({now}, {sjwt}, {iat_skew}, {key}, {alg})".format(
                now=timegm(datetime.utcnow().utctimetuple()),
                sjwt=json.dumps(sjwt),
                iat_skew=iat_skew.total_seconds(),
                key=json.dumps(key),
                alg=json.dumps(alg)),
            True)
        return tuple(r)
    return f

for alg in algs:
    priv_keys[alg]['node_jsjws'] = generate(alg)
    pub_keys[alg]['node_jsjws'] = verify(alg)

jwt_spec.setup(['HS256', 'HS512', 'RS256', 'RS512', 'PS256', 'PS512'])

for alg in algs:
    del priv_keys[alg]['node_jsjws']
    del pub_keys[alg]['node_jsjws']
