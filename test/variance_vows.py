""" Check generated tokens are all different """

# pylint: disable=wrong-import-order
from test.common import payload, priv_keys, algs
from test import jwt
from datetime import timedelta
from pyvows import Vows, expect

#pylint: disable=W0621
def check_different(alg, priv_type):
    """ Check all different for an algorith and private key """
    privk = priv_keys[alg][priv_type]
    @Vows.batch
    #pylint: disable=unused-variable
    class Variance(Vows.Context):
        """ Checks tokens are different """
        def topic(self):
            """ Generate 10 tokens """
            #pylint: disable=W0201
            self.tokens = {}
            for _ in range(10):
                #pylint: disable=W0631
                yield jwt.generate_jwt(payload, privk, alg, timedelta(seconds=5))

        def tokens_should_be_different(self, sjwt):
            """ Check token isn't in table """
            expect(self.tokens).Not.to_include(sjwt)
            self.tokens[sjwt] = True

        def teardown(self):
            """ Check table contains 10 tokens """
            expect(len(self.tokens)).to_equal(10)

for alg in algs:
    for priv_type in priv_keys[alg]:
        check_different(alg, priv_type)
