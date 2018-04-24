""" Other headers """

from datetime import timedelta
from test.common import payload, algs, generated_keys
from test import python_jwt as jwt
from pyvows import Vows, expect

def other_headers(alg, key):
    """ setup tests """
    @Vows.batch
    #pylint: disable=unused-variable
    class OtherHeaders(Vows.Context):
        """ Check extra header value is set in token """
        def topic(self):
            """ Generate token """
            return jwt.generate_jwt(payload, key, alg, timedelta(seconds=60),
                                    other_headers={'kid': '0123456789abcdef'})

        class Verify(Vows.Context):
            """ Verify token """
            def topic(self, topic):
                """ Verify token """
                return jwt.verify_jwt(topic, key, [alg])

            def token_should_verify_with_extra_header(self, r):
                """ Should verify and have kid header """
                expect(r).to_be_instance_of(tuple)
                header, _ = r
                expect(header).to_equal({
                    u'alg': alg,
                    u'typ': u'JWT',
                    u'kid': u'0123456789abcdef'
                })

    @Vows.batch
    #pylint: disable=unused-variable
    class RedefinedTypHeader(Vows.Context):
        """ Check typ other header raises exception """
        @Vows.capture_error
        def topic(self):
            """ Generate token """
            return jwt.generate_jwt(payload, key, alg, timedelta(seconds=60),
                                    other_headers={'typ': 'JWT'})

        def should_not_generated_token(self, r):
            """ Should not generate """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal("other_headers re-specified the headers: set(['typ'])")

    @Vows.batch
    #pylint: disable=unused-variable
    class RedefinedAlgHeader(Vows.Context):
        """ Check alg other header raises exception """
        @Vows.capture_error
        def topic(self):
            """ Generate token """
            return jwt.generate_jwt(payload, key, alg, timedelta(seconds=60),
                                    other_headers={'alg': 'JWT'})

        def should_not_generated_token(self, r):
            """ Should not generate """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal("other_headers re-specified the headers: set(['alg'])")

other_headers('none', None)
for _alg in algs:
    other_headers(_alg, generated_keys[_alg])
