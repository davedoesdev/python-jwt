#!/usr/bin/env python

""" Benchmark loading an RSA key from a PEM string """

# pylint: disable=wrong-import-position,wrong-import-order
import Crypto.PublicKey.RSA as RSA
from unitbench import Benchmark
from test.fixtures import priv_pem
from bench.reporter import Reporter

class LoadKeyBenchmark(Benchmark):
    """ Load key benchmark """

    def input(self):
        """ Name of benchmark """
        return ["Load Key"]

    def repeats(self):
        """ Iterations """
        return 10000

    def bench_RSA(self):
        """ Import key """
        RSA.importKey(priv_pem)

if __name__ == "__main__":
    #pylint: disable=W0402
    import string
    string.capwords = lambda x: x
    LoadKeyBenchmark().run(reporter=Reporter())
