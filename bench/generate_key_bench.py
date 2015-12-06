#!/usr/bin/env python

""" Benchmark generating an RSA key """

# pylint: disable=wrong-import-position,wrong-import-order
import Crypto.PublicKey.RSA as RSA
from unitbench import Benchmark
from bench.reporter import Reporter

class GenerateKeyBenchmark(Benchmark):
    """ Generate key benchmark """

    def input(self):
        """ Name of benchmark """
        return ["Generate Key"]

    def repeats(self):
        """ Iterations """
        return 100

    def bench_RSA(self):
        """ Generate key """
        RSA.generate(2048)

if __name__ == "__main__":
    #pylint: disable=W0402
    import string
    string.capwords = lambda x: x
    GenerateKeyBenchmark().run(reporter=Reporter())
