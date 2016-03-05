""" Test JWS not-implemented errors """

# pylint: disable=wrong-import-order
from test.common import clock_load, orig_datetime, clock_reset
from test import jwt
from pyvows import Vows, expect

# Header:
# {
#   "typ": "JWT",
#   "alg": "HS256",
#   "kid": "1234xbzsfgd54321"
# }
# Payload:
# {
#   "aud": "http://example.com/",
#   "iat": 0,
#   "nbf": 0,
#   "exp": 1455050174
# }
jwt_example = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjEyMzR4YnpzZmdkNTQzMjEifQ.eyJhdWQiOiJodHRwOi8vZXhhbXBsZS5jb20vIiwiaWF0IjowLCJuYmYiOjAsImV4cCI6MTQ1NTA1MDE3NH0.Mtz8WAc3ufd-o7PzAQ49JouEfBZGhU9q3uLfSnz0Nzw"

@Vows.batch
class JWSNotImplemented(Vows.Context):
    """ Generate token with a header not implemented by jws and check we get the
        error with ignore_not_implemented=False (default) but not with
        ignore_not_implemented=True
    """
    def topic(self):
        """ Return the token """
        return jwt_example

    class VerifyJWT(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            clock_load(orig_datetime.utcfromtimestamp(0))
            r = jwt.verify_jwt(topic, 'secret', ['HS256'])
            clock_reset()
            return r

        def token_should_fail_to_verify(self, r):
            """ Check it doesn't verify because JWS doesn't implement 'kid' """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('Header Parameter kid not implemented in the context of verifying')

    class VerifyJWTChecksOptional(Vows.Context):
        """ Verify token """
        def topic(self, topic):
            """ Verify the token """
            clock_load(orig_datetime.utcfromtimestamp(0))
            r = jwt.verify_jwt(topic, 'secret', ['HS256'],
                               ignore_not_implemented=True)
            clock_reset()
            return r

        def token_should_verify(self, r):
            """ Should verify and match expected claims """
            expect(r).to_be_instance_of(tuple)
            header, claims = r
            expect(header).to_equal({
                "typ": "JWT",
                "alg": "HS256",
                "kid": "1234xbzsfgd54321"
            })
            expect(claims).to_equal({
                "aud": "http://example.com/",
                "iat": 0,
                "nbf": 0,
                "exp": 1455050174
            })
