""" Test Google OAuth token """

# pylint: disable=wrong-import-order
from test.common import clock_tick, orig_datetime, clock_reset
from test import jwt
from pyvows import Vows, expect

# JWT from https://developers.google.com/accounts/docs/OAuth2ServiceAccount
google_jwt_example = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3NjEzMjY3OTgwNjktcjVtbGpsbG4xcmQ0bHJiaGc3NWVmZ2lncDM2bTc4ajVAZGV2ZWxvcGVyLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJzY29wZSI6Imh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvcHJlZGljdGlvbiIsImF1ZCI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi90b2tlbiIsImV4cCI6MTMyODU1NDM4NSwiaWF0IjoxMzI4NTUwNzg1fQ.ixOUGehweEVX_UKXv5BbbwVEdcz6AYS-6uQV6fGorGKrHf3LIJnyREw9evE-gs2bmMaQI5_UbabvI4k-mQE4kBqtmSpTzxYBL1TCd7Kv5nTZoUC1CmwmWCFqT9RE6D7XSgPUh_jF1qskLa2w0rxMSjwruNKbysgRNctZPln7cqQ"

@Vows.batch
class GoogleJWTOAuth(Vows.Context):
    """ Verify token from Google OAuth example """
    def topic(self):
        """ Return the token """
        return google_jwt_example

    class VerifyJWT(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['RS256', 'none'])

        def token_should_fail_to_verify(self, r):
            """ Check it doesn't verify because of missing claims """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('nbf claim not present')

    class VerifyJWTChecksOptional(Vows.Context):
        """ Verify token, relax claim existence checking """
        def topic(self, topic):
            """ Verify the token without requiring all claims """
            adjust = orig_datetime.utcnow() - orig_datetime.utcfromtimestamp(0)
            clock_tick(-adjust)
            r = jwt.verify_jwt(topic,
                               None,
                               ['RS256', 'none'],
                               iat_skew=adjust,
                               checks_optional=True)
            clock_reset()
            return r

        def token_should_verify(self, r):
            """ Should verify and match expected claims """
            expect(r).to_be_instance_of(tuple)
            header, claims = r
            expect(header).to_equal({
                u'alg': u'RS256',
                u'typ': u'JWT'
            })
            expect(claims).to_equal({
                u'iss': u'761326798069-r5mljlln1rd4lrbhg75efgigp36m78j5@developer.gserviceaccount.com',
                u'scope': u'https://www.googleapis.com/auth/prediction',
                u'aud': u'https://accounts.google.com/o/oauth2/token',
                u'exp': 1328554385,
                u'iat': 1328550785
            })
