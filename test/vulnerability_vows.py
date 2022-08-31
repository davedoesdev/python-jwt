""" Test claim forgery vulnerability fix """
from datetime import timedelta
from json import loads, dumps
from test.common import generated_keys
from test import python_jwt as jwt
from pyvows import Vows, expect
from jwcrypto.common import base64url_decode, base64url_encode

@Vows.batch
class ForgedClaims(Vows.Context):
    """ Check we get an error when payload is forged using mix of compact and JSON formats """
    def topic(self):
        """ Generate token """
        payload = {'sub': 'alice'}
        return jwt.generate_jwt(payload, generated_keys['PS256'], 'PS256', timedelta(minutes=60))

    class PolyglotToken(Vows.Context):
        """ Make a forged token """
        def topic(self, topic):
            """ Use mix of JSON and compact format to insert forged claims including long expiration """
            [header, payload, signature] = topic.split('.')
            parsed_payload = loads(base64url_decode(payload))
            parsed_payload['sub'] = 'bob'
            parsed_payload['exp'] = 2000000000
            fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))
            return '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'

        class Verify(Vows.Context):
            """ Check the forged token fails to verify """
            @Vows.capture_error
            def topic(self, topic):
                """ Verify the forged token """
                return jwt.verify_jwt(topic, generated_keys['PS256'], ['PS256'])

            def token_should_not_verify(self, r):
                """ Check the token doesn't verify due to mixed format being detected """
                expect(r).to_be_an_error()
                expect(str(r)).to_equal('invalid JWT format')
