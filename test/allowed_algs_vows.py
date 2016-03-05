""" test checking against set of allowed algorithms when verifying tokens """
# pylint: disable=wrong-import-order
from test.common import payload, algs, generated_keys
from test import jwt
from datetime import timedelta
from pyvows import Vows, expect

all_algs = algs + ['none']

#pylint: disable=too-many-branches
def check_allowed(alg, key):
    """ setup tests """
    @Vows.batch
    #pylint: disable=unused-variable
    class GenerateJWT(Vows.Context):
        """ Checks algorithm is allowed when in set of allowed algorithms """
        def topic(self):
            """ Generate token """
            return jwt.generate_jwt(payload, key, alg, timedelta(seconds=60))

        class VerifyJWTNoAlgsSpecified(Vows.Context):
            """ Verify token, allowed algorithms not specified """
            @Vows.capture_error
            def topic(self, topic):
                """ Verify the token """
                return jwt.verify_jwt(topic, key)

            def token_should_not_verify(self, r):
                """ Should not verify """
                expect(r).to_be_an_error()
                expect(str(r)).to_equal('algorithm not allowed: ' + alg)

        class VerifyJWTAllAlgsAllowed(Vows.Context):
            """ Verify token, all algorithms allowed """
            def topic(self, topic):
                """ Verify the token """
                return jwt.verify_jwt(topic, key, all_algs)

            def token_should_verify(self, r):
                """ Should verify """
                expect(r).to_be_instance_of(tuple)
                header, _ = r
                expect(header).to_equal({'alg': alg, 'typ': 'JWT'})

        class VerifyJWTNoAlgsAllowed(Vows.Context):
            """ Verify token, no algorithms allowed """
            @Vows.capture_error
            def topic(self, topic):
                """ Verify the token """
                return jwt.verify_jwt(topic, key, [])

            def token_should_not_verify(self, r):
                """ Should not verify """
                expect(r).to_be_an_error()
                expect(str(r)).to_equal('algorithm not allowed: ' + alg)

        class VerifyJWTAlgAllowed(Vows.Context):
            """ Verify token, algorithm not allowed """
            @Vows.capture_error
            def topic(self, topic):
                """ Verify the token """
                return jwt.verify_jwt(topic, key, [a for a in all_algs if a != alg])

            def token_should_not_verify(self, r):
                """ Should not verify """
                expect(r).to_be_an_error()
                expect(str(r)).to_equal('algorithm not allowed: ' + alg)

check_allowed('none', None)
for _alg in algs:
    check_allowed(_alg, generated_keys[_alg])
