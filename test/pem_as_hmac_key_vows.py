""" test using PEM as key - we shouldn't validate a HMAC token instead """
# pylint: disable=wrong-import-order
from test.common import payload, pub_pem, pub_key
from test import python_jwt as jwt
from datetime import timedelta
from pyvows import Vows, expect
from jwcrypto.jwk import JWK
from jwcrypto.common import base64url_encode

pem_key = JWK(kty='oct', k=base64url_encode(pub_pem))

@Vows.batch
class PEMAsHMACKey(Vows.Context):
    """ setup tests """
    def topic(self):
        """ Generate token """
        return jwt.generate_jwt(payload, pem_key, 'HS256', timedelta(seconds=60))

    class VerifyTokenUsingPublicPEMNoAllowedAlgsSpecified(Vows.Context):
        """ Verify token, allowed algorithms not specified """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, pem_key)

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('algorithm not allowed: HS256')

    class VerifyTokenUsingPublicPEMHS256AlgAllowed(Vows.Context):
        """ Verify token, specifiy allowed alg """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, pem_key, ['HS256'])

        def token_should_verify(self, r):
            """ Should verify """
            expect(r).to_be_instance_of(tuple)

    class VerifyTokenUsingPublicPEMRS256AlgAllowed(Vows.Context):
        """ Verify token, specifiy allowed alg """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, pem_key, ['RS256'])

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
