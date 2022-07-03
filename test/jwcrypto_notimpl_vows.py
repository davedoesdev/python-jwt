""" Test JWS not-implemented errors """

# pylint: disable=wrong-import-order
from test.common import clock_load, orig_datetime, clock_reset
from test import python_jwt as jwt
from pyvows import Vows, expect
from jwcrypto.jwk import JWK
from jwcrypto.common import base64url_encode

# Header:
# {
#   "typ": "JWT",
#   "alg": "HS256",
#   "jku": "https://server.example.com/keys.jwk"
# }
# Payload:
# {
#   "aud": "http://example.com/",
#   "iat": 0,
#   "nbf": 0,
#   "exp": 1455050174
# }
jwt_example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImprdSI6Imh0dHBzOi8vc2VydmVyLmV4YW1wbGUuY29tL2tleXMuandrIn0.eyJhdWQiOiJodHRwOi8vZXhhbXBsZS5jb20vIiwiaWF0IjowLCJuYmYiOjAsImV4cCI6MTQ1NTA1MDE3NH0.3jyP-oEGkI-YDA-FpoRbzJxLbZ5OIOu4gbTOmPhGw3w"

@Vows.batch
class JWSNotImplemented(Vows.Context):
    """ Generate token with a header not implemented by jwcrypto and check we
        get the error with ignore_not_implemented=False (default) but not with
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
            r = jwt.verify_jwt(topic,
                               JWK(kty='oct', k=base64url_encode('secret')),
                               ['HS256'])
            clock_reset()
            return r

        def token_should_fail_to_verify(self, r):
            """ Check it doesn't verify because JWS doesn't implement 'jku' """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('header not implemented: jku')

    class VerifyJWTChecksOptional(Vows.Context):
        """ Verify token """
        def topic(self, topic):
            """ Verify the token """
            clock_load(orig_datetime.utcfromtimestamp(0))
            r = jwt.verify_jwt(topic,
                               JWK(kty='oct', k=base64url_encode('secret')),
                               ['HS256'],
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
                "jku": "https://server.example.com/keys.jwk"
            })
            expect(claims).to_equal({
                "aud": "http://example.com/",
                "iat": 0,
                "nbf": 0,
                "exp": 1455050174
            })
