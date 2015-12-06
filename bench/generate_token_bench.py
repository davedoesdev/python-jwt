#!/usr/bin/env python

""" Benchmark generating a JWT """

# pylint: disable=wrong-import-position,wrong-import-order
from datetime import timedelta
from unitbench import Benchmark
from test.fixtures import payload, priv_keys, priv_key, algs
from bench.reporter import Reporter
import jwt

class GenerateTokenBenchmark(Benchmark):
    """ Generate JWT benchmark """

    def input(self):
        """ Nme of benchmark """
        return ["Generate Token"]

    def repeats(self):
        """ Iterations """
        return 1000

#pylint: disable=W0621
def make_bench_generate_token(alg):
    """ Return function which will generate token for particular algorithm """
    def f(_):
        """ Generate token """
        privk = priv_keys[alg].get('default', priv_key)
        jwt.generate_jwt(payload, privk, alg, timedelta(seconds=5))
    return f

for alg in algs:
    name = 'bench_' + alg
    f = make_bench_generate_token(alg)
    f.__name__ = name
    setattr(GenerateTokenBenchmark, name, f)

if __name__ == "__main__":
    #pylint: disable=W0402
    import string
    string.capwords = lambda x: x
    GenerateTokenBenchmark().run(reporter=Reporter())
