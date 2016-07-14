""" test generation and verification of tokens """
# pylint: disable=wrong-import-order
from test.common import payload, pub_keys, priv_keys, algs, generated_keys, \
                        clock_tick, clock_load
from test import jwt
from datetime import timedelta, datetime
from base64 import urlsafe_b64decode
from pyvows import Vows, expect

keys = list(payload.keys())
keys += ['exp', 'nbf', 'iat', 'jti']

def is_string(obj):
    """ Duck type detect string """
    try:
        #pylint: disable=unused-variable
        obj2 = obj + ''
        return True
    except TypeError:
        return False

#pylint: disable=R0912
def _setup(alg, priv_type, pub_type, exp, iat_skew, nbf, jti_size, keyless, expected):
    """ setup tests """
    privk = None if keyless else priv_keys[alg][priv_type]
    pubk = None if keyless else pub_keys[alg][pub_type]
    jtis = {}
    @Vows.batch
    #pylint: disable=W0612
    class GenerateJWT(Vows.Context):
    #pylint: enable=W0612
        """ generate token """
        def topic(self):
            """ generate tokens, one with lifetime, one with expires """
            lt = timedelta(seconds=exp)
            now = datetime.utcnow()
            not_before = (now + timedelta(minutes=nbf)) if nbf else None
            if callable(privk):
                token = privk(payload, alg, lt, not_before=not_before)
            else:
                token = jwt.generate_jwt(payload, privk, alg, lt,
                                         not_before=not_before,
                                         jti_size=jti_size)
            yield clock_tick(timedelta(milliseconds=1500)), token
            now = datetime.utcnow()
            not_before = (now + timedelta(minutes=nbf)) if nbf else None
            if callable(privk):
                token = privk(payload, alg,
                              expires=(now + lt),
                              not_before=not_before)
            else:
                token = jwt.generate_jwt(payload, privk, alg,
                                         expires=(now + lt),
                                         not_before=not_before,
                                         jti_size=jti_size)
            yield clock_tick(timedelta(milliseconds=1500)), token

        class ProcessJWT(Vows.Context):
            """ Parse the token, check contents """
            def topic(self, topic):
                """ Get just the token, don't need clock """
                _, sjwt = topic
                return jwt.process_jwt(sjwt)

            class CheckClaims(Vows.Context):
                """ Check claims in token """
                def topic(self, token):
                    """ Get just the claims """
                    _, claims = token
                    return claims

                def payload_keys_should_be_as_expected(self, claims):
                    """ Check keys """
                    expect(list(claims.keys())).to_be_like(keys if jti_size or callable(privk) else [key for key in keys if key != 'jti'])

                def payload_values_should_match(self, claims):
                    """ Check values """
                    for x in payload:
                        expect(claims[x]).to_equal(payload[x])

                def jtis_should_be_unique(self, claims):
                    """ Check jtis """
                    if jti_size or callable(privk):
                        expect(is_string(claims['jti'])).to_be_true()
                        expect(jtis).Not.to_include(claims['jti'])
                        jtis[claims['jti']] = True

                def jti_size_should_be_as_expected(self, claims):
                    """ Check jti size """
                    if jti_size and not callable(privk): # don't assume format of externally-generated JTIs
                        expect(len(urlsafe_b64decode(claims['jti'].encode('utf-8')))).to_equal(jti_size)

            def header_should_be_as_expected(self, token):
                """ Check header """
                header, _ = token
                expect(header).to_equal({
                    'alg': 'none' if keyless else alg,
                    'typ': 'JWT'
                })

        class VerifyJWTWithGeneratedKey(Vows.Context):
            """ Verify token doesn't verify with minted key """
            @Vows.capture_error
            def topic(self, topic):
                """ Set clock and verify token with minted key """
                clock, sjwt = topic
                clock_load(clock)
                pubk = None if keyless else generated_keys[alg]
                return jwt.verify_jwt(sjwt, pubk, ['none'] if keyless else [alg],
                                      timedelta(seconds=iat_skew))

            def should_fail_to_verify(self, r):
                """ Should fail to verify with minted key """
                if keyless and expected:
                    expect(r).to_be_instance_of(tuple)
                else:
                    expect(r).to_be_an_error()

        class VerifyJWT(Vows.Context):
            """ Verify token with public key passed in """
            @Vows.capture_error
            def topic(self, topic):
                """ Set clock and verify token """
                clock, sjwt = topic
                clock_load(clock)
                if callable(pubk):
                    return pubk(sjwt, timedelta(seconds=iat_skew))
                else:
                    return jwt.verify_jwt(sjwt, pubk, ['none'] if keyless else [alg],
                                          timedelta(seconds=iat_skew))

            def should_verify_as_expected(self, r):
                """ Check verified or not, as per expected arg """
                if expected:
                    try:
                        expect(r).to_be_instance_of(tuple)
                    except:
                        print(alg, priv_type, pub_type, exp, iat_skew, nbf, keyless, expected)
                        raise
                else:
                    expect(r).to_be_an_error()

#pylint: disable=W0621,dangerous-default-value
def setup(algs=algs):
    """ Setup all the tests for each alg """
    for alg in algs:
        for priv_type in priv_keys[alg]:
            for pub_type in pub_keys[alg]:
                for keyless in [False, True]:
                    for jti_size in [16, 128, 0]:
                        _setup(alg, priv_type, pub_type, 10, 0, None, jti_size, keyless, True)
                        _setup(alg, priv_type, pub_type, 1, 0, None, jti_size, keyless, False)

                        _setup(alg, priv_type, pub_type, 10, -10, None, jti_size, keyless, False)
                        _setup(alg, priv_type, pub_type, 1, -10, None, jti_size, keyless, False)

                        _setup(alg, priv_type, pub_type, 10, 10, None, jti_size, keyless, True)
                        _setup(alg, priv_type, pub_type, 1, 10, None, jti_size, keyless, False)


                        _setup(alg, priv_type, pub_type, 10, 0, 1, jti_size, keyless, False)
                        _setup(alg, priv_type, pub_type, 1, 0, 1, jti_size, keyless, False)

                        _setup(alg, priv_type, pub_type, 10, -10, 1, jti_size, keyless, False)
                        _setup(alg, priv_type, pub_type, 1, -10, 1, jti_size, keyless, False)

                        _setup(alg, priv_type, pub_type, 10, 10, 1, jti_size, keyless, False)
                        _setup(alg, priv_type, pub_type, 1, 10, 1, jti_size, keyless, False)


                        _setup(alg, priv_type, pub_type, 10, 0, -1, jti_size, keyless, True)
                        _setup(alg, priv_type, pub_type, 1, 0, -1, jti_size, keyless, False)

                        _setup(alg, priv_type, pub_type, 10, -10, -1, jti_size, keyless, False)
                        _setup(alg, priv_type, pub_type, 1, -10, -1, jti_size, keyless, False)

                        _setup(alg, priv_type, pub_type, 10, 10, -1, jti_size, keyless, True)
                        _setup(alg, priv_type, pub_type, 1, 10, -1, jti_size, keyless, False)
