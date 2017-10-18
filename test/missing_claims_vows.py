""" Test missing claims """

from datetime import timedelta
from test.common import payload, algs, generated_keys
from test import python_jwt as jwt
from pyvows import Vows, expect
from jwcrypto.common import json_decode, json_encode, base64url_decode, base64url_encode

def missing_expiry(alg, key):
    """ setup tests"""
    @Vows.batch
    #pylint: disable=unused-variable
    class GenerateJWTWithoutExpiry(Vows.Context):
        """ Check we get an error when no exp claim is set """
        def topic(self):
            """ Generate token """
            return jwt.generate_jwt(payload, key, alg)

        class Verify(Vows.Context):
            """ Verify token """
            @Vows.capture_error
            def topic(self, topic):
                """ Verify the token """
                return jwt.verify_jwt(topic, key, [alg])

            def token_should_not_verify(self, r):
                """ Should not verify """
                expect(r).to_be_an_error()
                expect(str(r)).to_equal('exp claim not present')

        class VerifyChecksOptional(Vows.Context):
            """ Verify token """
            @Vows.capture_error
            def topic(self, topic):
                """ Verify the token """
                return jwt.verify_jwt(topic, key, [alg], checks_optional=True)

            def token_should_verify(self, r):
                """ Should verify """
                expect(r).to_be_instance_of(tuple)

missing_expiry('none', None)
for _alg in algs:
    missing_expiry(_alg, generated_keys[_alg])

@Vows.batch
class GenerateJWTWithoutIssuedAt(Vows.Context):
    """ Check we get an error when no iat claim is set """
    def topic(self):
        """ Generate token """
        token = jwt.generate_jwt(payload, None, 'none', timedelta(seconds=60))
        header, claims, _ = token.split('.')
        parsed_claims = json_decode(base64url_decode(claims))
        del parsed_claims['iat']
        return u"%s.%s." % (header, base64url_encode(json_encode(parsed_claims)))

    class Verify(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'])

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('iat claim not present')

    class VerifyChecksOptional(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'], checks_optional=True)

        def token_should_verify(self, r):
            """ Should verify """
            expect(r).to_be_instance_of(tuple)

@Vows.batch
class GenerateJWTWithoutAlgorithm(Vows.Context):
    """ Check we get an error when no alg header is set """
    def topic(self):
        """ Generate token """
        token = jwt.generate_jwt(payload, None, 'none', timedelta(seconds=60))
        header, claims, _ = token.split('.')
        parsed_header = json_decode(base64url_decode(header))
        del parsed_header['alg']
        return u"%s.%s." % (base64url_encode(json_encode(parsed_header)), claims)

    class Verify(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'])

@Vows.batch
class GenerateJWTWithoutType(Vows.Context):
    """ Check we get an error when no typ header is set """
    def topic(self):
        """ Generate token """
        token = jwt.generate_jwt(payload, None, 'none', timedelta(seconds=60))
        header, claims, _ = token.split('.')
        parsed_header = json_decode(base64url_decode(header))
        del parsed_header['typ']
        return u"%s.%s." % (base64url_encode(json_encode(parsed_header)), claims)

    class Verify(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'])

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('typ header not present')

    class VerifyChecksOptional(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'], checks_optional=True)

        def token_should_verify(self, r):
            """ Should verify """
            expect(r).to_be_instance_of(tuple)

@Vows.batch
class GenerateJWTWithWrongType(Vows.Context):
    """ Check we get an error when no typ header isn't 'jwt' """
    def topic(self):
        """ Generate token """
        token = jwt.generate_jwt(payload, None, 'none', timedelta(seconds=60))
        header, claims, _ = token.split('.')
        parsed_header = json_decode(base64url_decode(header))
        parsed_header['typ'] = 'foo'
        return u"%s.%s." % (base64url_encode(json_encode(parsed_header)), claims)

    class Verify(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'])

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('typ header is not JWT')

@Vows.batch
class GenerateJWTWithUnknownHeader(Vows.Context):
    """ Check we get an error when unknown header present """
    def topic(self):
        """ Generate token """
        token = jwt.generate_jwt(payload, None, 'none', timedelta(seconds=60))
        header, claims, _ = token.split('.')
        parsed_header = json_decode(base64url_decode(header))
        parsed_header['foo'] = 'bar'
        return u"%s.%s." % (base64url_encode(json_encode(parsed_header)), claims)

    class Verify(Vows.Context):
        """ Verify token """
        @Vows.capture_error
        def topic(self, topic):
            """ Verify the token """
            return jwt.verify_jwt(topic, None, ['none'])

        def token_should_not_verify(self, r):
            """ Should not verify """
            expect(r).to_be_an_error()
            expect(str(r)).to_equal('unknown header: foo')
