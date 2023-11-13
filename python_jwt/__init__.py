"""
Functions for generating and verifying JSON Web Tokens.
"""

import warnings
import re
from datetime import datetime, timedelta
from calendar import timegm
from os import urandom
from jwcrypto.jws import JWS, JWSHeaderRegistry
from jwcrypto.common import base64url_encode, base64url_decode, \
                            json_encode, json_decode

warnings.warn('The python_jwt module is deprecated', DeprecationWarning, stacklevel=2)

class _JWTError(Exception):
    """ Exception raised if claim doesn't pass. Private to this module because
        jwcrypto throws many exceptions too. """
    pass

def generate_jwt(claims, priv_key=None,
                 algorithm='PS512', lifetime=None, expires=None,
                 not_before=None,
                 jti_size=16, other_headers=None):
    """
    Generate a JSON Web Token.

    :param claims: The claims you want included in the signature.
    :type claims: dict

    :param priv_key: The private key to be used to sign the token. Note: if you pass ``None`` then the token will be returned with an empty cryptographic signature and :obj:`algorithm` will be forced to the value ``none``.
    :type priv_key: `jwcrypto.jwk.JWK <https://jwcrypto.readthedocs.io/en/latest/jwk.html>`_

    :param algorithm: The algorithm to use for generating the signature. ``RS256``, ``RS384``, ``RS512``, ``PS256``, ``PS384``, ``PS512``, ``ES256``, ``ES384``, ``ES512``, ``HS256``, ``HS384``, ``HS512`` and ``none`` are supported.
    :type algorithm: str

    :param lifetime: How long the token is valid for.
    :type lifetime: datetime.timedelta

    :param expires: When the token expires (if :obj:`lifetime` isn't specified)
    :type expires: datetime.datetime

    :param not_before: When the token is valid from. Defaults to current time (if ``None`` is passed).
    :type not_before: datetime.datetime

    :param jti_size: Size in bytes of the unique token ID to put into the token (can be used to detect replay attacks). Defaults to 16 (128 bits). Specify 0 or ``None`` to omit the JTI from the token.
    :type jti_size: int

    :param other_headers: Any headers other than "typ" and "alg" may be specified, they will be included in the header.
    :type other_headers: dict

    :rtype: unicode
    :returns: The JSON Web Token. Note this includes a header, the claims and a cryptographic signature. The following extra claims are added, per the `JWT spec <http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html>`_:

    - **exp** (*IntDate*) -- The UTC expiry date and time of the token, in number of seconds from 1970-01-01T0:0:0Z UTC.
    - **iat** (*IntDate*) -- The UTC date and time at which the token was generated.
    - **nbf** (*IntDate*) -- The UTC valid-from date and time of the token.
    - **jti** (*str*) -- A unique identifier for the token.

    :raises:
        ValueError: If other_headers contains either the "typ" or "alg" header
    """
    header = {
        'typ': 'JWT',
        'alg': algorithm if priv_key else 'none'
    }

    if other_headers is not None:
        redefined_keys = set(header.keys()) & set(other_headers.keys())
        if redefined_keys:
            raise ValueError('other_headers re-specified the headers: {}'.format(', '.join(redefined_keys)))
        header.update(other_headers)

    claims = dict(claims)

    now = datetime.utcnow()

    if jti_size:
        claims['jti'] = base64url_encode(urandom(jti_size))

    claims['nbf'] = timegm((not_before or now).utctimetuple())
    claims['iat'] = timegm(now.utctimetuple())

    if lifetime:
        claims['exp'] = timegm((now + lifetime).utctimetuple())
    elif expires:
        claims['exp'] = timegm(expires.utctimetuple())

    if header['alg'] == 'none':
        signature = ''
    else:
        token = JWS(json_encode(claims))
        token.allowed_algs = [header['alg']]
        token.add_signature(priv_key, protected=header)
        signature = json_decode(token.serialize())['signature']

    return u'%s.%s.%s' % (
        base64url_encode(json_encode(header)),
        base64url_encode(json_encode(claims)),
        signature
    )

#pylint: disable=R0912,too-many-locals

_jwt_re = re.compile(r'^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]*$')
def _check_jwt_format(jwt):
    if not _jwt_re.match(jwt):
        raise _JWTError('invalid JWT format')

def verify_jwt(jwt,
               pub_key=None,
               allowed_algs=None,
               iat_skew=timedelta(),
               checks_optional=False,
               ignore_not_implemented=False):
    """
    Verify a JSON Web Token.

    :param jwt: The JSON Web Token to verify.
    :type jwt: str or unicode

    :param pub_key: The public key to be used to verify the token. Note: if you pass ``None`` and **allowed_algs** contains ``none`` then the token's signature will not be verified.
    :type pub_key: `jwcrypto.jwk.JWK <https://jwcrypto.readthedocs.io/en/latest/jwk.html>`_

    :param allowed_algs: Algorithms expected to be used to sign the token. The ``in`` operator is used to test membership.
    :type allowed_algs: list or NoneType (meaning an empty list)

    :param iat_skew: The amount of leeway to allow between the issuer's clock and the verifier's clock when verifying that the token was generated in the past. Defaults to no leeway.
    :type iat_skew: datetime.timedelta

    :param checks_optional: If ``False``, then the token must contain the **typ** header property and the **iat**, **nbf** and **exp** claim properties.
    :type checks_optional: bool

    :param ignore_not_implemented: If ``False``, then the token must *not* contain the **jku**, **jwk**, **x5u**, **x5c** or **x5t** header properties.
    :type ignore_not_implemented: bool

    :rtype: tuple
    :returns: ``(header, claims)`` if the token was verified successfully. The token must pass the following tests:

    - Its header must contain a property **alg** with a value in **allowed_algs**.
    - Its signature must verify using **pub_key** (unless its algorithm is ``none`` and ``none`` is in **allowed_algs**).
    - If the corresponding property is present or **checks_optional** is ``False``:

      - Its header must contain a property **typ** with the value ``JWT``.
      - Its claims must contain a property **iat** which represents a date in the past (taking into account :obj:`iat_skew`).
      - Its claims must contain a property **nbf** which represents a date in the past.
      - Its claims must contain a property **exp** which represents a date in the future.

    :raises: If the token failed to verify.
    """
    #pylint: disable=too-many-statements

    _check_jwt_format(jwt)

    if allowed_algs is None:
        allowed_algs = []

    if not isinstance(allowed_algs, list):
        # jwcrypto only supports list of allowed algorithms
        raise _JWTError('allowed_algs must be a list')

    header, claims, _ = jwt.split('.')

    parsed_header = json_decode(base64url_decode(header))

    alg = parsed_header.get('alg')
    if alg is None:
        raise _JWTError('alg header not present')
    if alg not in allowed_algs:
        raise _JWTError('algorithm not allowed: ' + alg)

    if not ignore_not_implemented:
        for k in parsed_header:
            if k not in JWSHeaderRegistry:
                raise _JWTError('unknown header: ' + k)
            if not JWSHeaderRegistry[k].supported:
                raise _JWTError('header not implemented: ' + k)

    if pub_key:
        token = JWS()
        token.allowed_algs = allowed_algs
        token.deserialize(jwt, pub_key)
        parsed_claims = json_decode(token.payload)
    elif 'none' not in allowed_algs:
        raise _JWTError('no key but none alg not allowed')
    else:
        parsed_claims = json_decode(base64url_decode(claims))

    utcnow = datetime.utcnow()
    now = timegm(utcnow.utctimetuple())

    typ = parsed_header.get('typ')
    if typ is None:
        if not checks_optional:
            raise _JWTError('typ header not present')
    elif typ != 'JWT':
        raise _JWTError('typ header is not JWT')

    iat = parsed_claims.get('iat')
    if iat is None:
        if not checks_optional:
            raise _JWTError('iat claim not present')
    elif iat > timegm((utcnow + iat_skew).utctimetuple()):
        raise _JWTError('issued in the future')

    nbf = parsed_claims.get('nbf')
    if nbf is None:
        if not checks_optional:
            raise _JWTError('nbf claim not present')
    elif nbf > now:
        raise _JWTError('not yet valid')

    exp = parsed_claims.get('exp')
    if exp is None:
        if not checks_optional:
            raise _JWTError('exp claim not present')
    elif exp <= now:
        raise _JWTError('expired')

    return parsed_header, parsed_claims

#pylint: enable=R0912

def process_jwt(jwt):
    """
    Process a JSON Web Token without verifying it.

    Call this before :func:`verify_jwt` if you need access to the header or claims in the token before verifying it. For example, the claims might identify the issuer such that you can retrieve the appropriate public key.

    :param jwt: The JSON Web Token to verify.
    :type jwt: str or unicode

    :rtype: tuple
    :returns: ``(header, claims)``
    """
    _check_jwt_format(jwt)
    header, claims, _ = jwt.split('.')
    parsed_header = json_decode(base64url_decode(header))
    parsed_claims = json_decode(base64url_decode(claims))
    return parsed_header, parsed_claims
