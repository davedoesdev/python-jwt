""" Test verification of tokens with algorithms none """

# pylint: disable=wrong-import-order
from test.common import payload, generated_key
from test import jwt
from datetime import timedelta
from pyvows import Vows, expect

# JWT from @timmclean
jwt_alg_none = "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpYXQiOjAsIm5iZiI6MCwiZXhwIjoxZTIwfQ."

@Vows.batch
class AlgNoneVerification(Vows.Context):
    """ Check we get an error when verifying token that has alg none with
        a public key """
    def topic(self):
        """ Return the token """
        return jwt_alg_none

    class VerifyJWTNoPublicKeyNoneAllowed(Vows.Context):
        """ Verify token without specifying public key and allowing none alg """
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'])

        def token_should_verify(self, r):
            """ Should verify """
            expect(r).to_be_instance_of(tuple)

    class VerifyJWTPublicKeyNoneAllowed(Vows.Context):
        """ Verify token with public key and specify none alg is allowed """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token with some public key and none alg allowed """
            return jwt.verify_jwt(topic, 'anysecrethere', ['none'])

        def token_should_verify(self, r):
            """ Should not verify because python-jws doesn't support none alg """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('"none" not implemented.')

    class VerifyJWTPublicKeyNoneNotAllowed(Vows.Context):
        """ Verify token with public key """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token with some public key """
            return jwt.verify_jwt(topic, 'anysecrethere')

        def token_should_fail_to_verify_when_pub_key_specified(self, r):
            """ Check it doesn't verify because alg is none """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('algorithm not allowed: none')

    class VerifyJWTNoPublicKeyNoneNotAllowed(Vows.Context):
        """ Verify token with no public key """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token with no public key """
            return jwt.verify_jwt(topic)

        def token_should_fail_to_verify_when_pub_key_specified(self, r):
            """ Check it doesn't verify because alg is none """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('algorithm not allowed: none')

@Vows.batch
class AlgNoneVerification2(Vows.Context):
    """ Check we get an error when verifying token that has alg RS256 with
        no public key """
    def topic(self):
        """ Generate the token """
        return jwt.generate_jwt(payload, generated_key, 'RS256', timedelta(seconds=10))

    class VerifyJWTNoPublicKeyAlgButNotNoneAllowed(Vows.Context):
        """ Verify token with no public key """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify token with no public key and allow RS256 """
            return jwt.verify_jwt(topic, None, ['RS256'])

        def token_should_fail_to_verify_when_pub_key_specified(self, r):
            """ Check it doesn't verify because alg none not allowed """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('no key but none alg not allowed')
