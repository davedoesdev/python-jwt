#!/usr/bin/env python

""" Benchmark verifying a JWT """

# pylint: disable=wrong-import-position,wrong-import-order
from datetime import timedelta
from unitbench import Benchmark
from test.fixtures import payload, priv_keys, priv_key, pub_keys, pub_key, algs
from bench.reporter import Reporter
import jwt

class VerifyTokenBenchmark(Benchmark):
    """ Verify JWT benchmark """

    def input(self):
        """ Name of benchmark """
        return ["Verify Token"]

    def repeats(self):
        """ Iterations """
        return 1000

#pylint: disable=W0621
def make_bench_verify_token(alg):
    """ Return function which will generate token for particular algorithm """
    privk = priv_keys[alg].get('default', priv_key)
    token = jwt.generate_jwt(payload, privk, alg, timedelta(days=1))
    def f(_):
        """ Verify token """
        pubk = pub_keys[alg].get('default', pub_key)
        jwt.verify_jwt(token, pubk, [alg])
    return f

for alg in algs:
    name = 'bench_' + alg
    f = make_bench_verify_token(alg)
    f.__name__ = name
    setattr(VerifyTokenBenchmark, name, f)

if __name__ == "__main__":
    #pylint: disable=W0402
    import string
    string.capwords = lambda x: x
    VerifyTokenBenchmark().run(reporter=Reporter())
