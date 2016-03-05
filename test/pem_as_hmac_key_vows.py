""" test using PEM as key - we shouldn't validate a HMAC token instead """
# pylint: disable=wrong-import-order
from test.common import payload, pub_pem, pub_key
from test import jwt
from datetime import timedelta
from pyvows import Vows, expect

@Vows.batch
class PEMAsHMACKey(Vows.Context):
    """ setup tests """
    def topic(self):
        """ Generate token """
        return jwt.generate_jwt(payload, pub_pem, 'HS256', timedelta(seconds=60))

    class VerifyTokenUsingPublicPEMNoAllowedAlgsSpecified(Vows.Context):
        """ Verify token, allowed algorithms not specified """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, pub_pem)

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('algorithm not allowed: HS256')

    class VerifyTokenUsingPublicPEMHS256AlgAllowed(Vows.Context):
        """ Verify token, specifiy allowed alg """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, pub_pem, ['HS256'])

        def token_should_verify(self, r):
            """ Should verify """
            expect(r).to_be_instance_of(tuple)

    class VerifyTokenUsingPublicPEMRS256AlgAllowed(Vows.Context):
        """ Verify token, specifiy allowed alg """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, pub_pem, ['RS256'])

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('algorithm not allowed: HS256')

    class VerifyTokenUsingPublicKey(Vows.Context):
        """ Verify token using public key """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, pub_key)

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
