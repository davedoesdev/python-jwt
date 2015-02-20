""" Test verification of tokens with algorithms none """

from pyvows import Vows, expect
import jwt

# JWT from @timmclean
jwt_alg_none = "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpYXQiOjAsIm5iZiI6MCwiZXhwIjoxZTIwfQ."

@Vows.batch
class AlgNoneVerification(Vows.Context):
    """ Check we get an error when verifying token that has alg none with
        a public key """
    def topic(self):
        """ Return the token """
        return jwt_alg_none

    class VerifyJWT(Vows.Context):
        """ Verify token without specifying public key """
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None)

        def token_should_verify(self, r):
            """ Should verify and match expected claims """
            expect(r).to_be_instance_of(tuple)

    class VerifyJWTWithPublicKey(Vows.Context):
        """ Verify token with public key """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token with some public key """
            return jwt.verify_jwt(topic, 'anysecrethere')

        def token_should_fail_to_verify_when_pub_key_specified(self, r):
            """ Check it doesn't verify because alg is none """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('key specified but alg is none')

    class VerifyJWTWithPublicKeyAndAllowedAlgNone(Vows.Context):
        """ Verify token with public key and specify none alg is allowed """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token with some public key and none alg allowed """
            return jwt.verify_jwt(topic, 'anysecrethere', allowed_algs=['none'])

        def token_should_verify(self, r):
            """ Should verify and match expected claims """
            expect(r).to_be_instance_of(tuple)
