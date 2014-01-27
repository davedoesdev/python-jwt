"""
Functions for generating and verifying JSON Web Tokens.
"""

from datetime import datetime, timedelta
from calendar import timegm
from base64 import urlsafe_b64encode
from os import urandom
import jws

class _JWTError(Exception):
    """ Exception raised if claim doesn't pass. Private to this module because
        jws throws many exceptions too. """
    pass

def generate_jwt(claims, priv_key=None,
                 algorithm='PS512', lifetime=None, expires=None,
                 not_before=None):
    """
    Generate a JSON Web Token.

    :param claims: The claims you want included in the signature.
    :type claims: dict

    :param priv_key: The private key to be used to sign the token. Note: if you pass :obj:`None` then the token will be returned with an empty cryptographic signature and :obj:`algorithm` will be forced to the value ``none``.
    :type priv_key: `_RSAobj <https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA._RSAobj-class.html>`_, `SigningKey <https://github.com/warner/python-ecdsa>`_ or str

    :param algorithm: The algorithm to use for generating the signature. ``RS256``, ``RS384``, ``RS512``, ``PS256``, ``PS384``, ``PS512``, ``ES256``, ``ES384``, ``ES512``, ``HS256``, ``HS384``, ``HS512`` and ``none`` are supported.
    :type algorithm: str

    :param lifetime: How long the token is valid for.
    :type lifetime: datetime.timedelta

    :param expires: When the token expires (if :obj:`lifetime` isn't specified)
    :type expires: datetime.datetime

    :param not_before: When the token is valid from. Defaults to current time (if :obj:`None` is passed).
    :type not_before: datetime.datetime

    :rtype: str
    :returns: The JSON Web Token. Note this includes a header, the claims and a cryptographic signature. The following extra claims are added, per the `JWT spec <http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html>`_:

    - **exp** (*IntDate*) -- The UTC expiry date and time of the token, in number of seconds from 1970-01-01T0:0:0Z UTC.
    - **iat** (*IntDate*) -- The UTC date and time at which the token was generated.
    - **nbf** (*IntDate*) -- The UTC valid-from date and time of the token.
    - **jti** (*str*) -- A unique identifier for the token.
    """
    header = {
        'typ': 'JWT',
        'alg': algorithm if priv_key else 'none'
    }

    claims = dict(claims)

    now = datetime.utcnow()

    claims['jti'] = urlsafe_b64encode(urandom(128))
    claims['nbf'] = timegm((not_before or now).utctimetuple())
    claims['iat'] = timegm(now.utctimetuple())

    if lifetime:
        claims['exp'] = timegm((now + lifetime).utctimetuple())
    elif expires:
        claims['exp'] = timegm(expires.utctimetuple())

    return "%s.%s.%s" % (
        jws.utils.encode(header),
        jws.utils.encode(claims),
        '' if header['alg'] == 'none' else jws.sign(header, claims, priv_key)
    )

def verify_jwt(jwt, pub_key=None, iat_skew=timedelta()):
    """
    Verify a JSON Web Token.

    :param jwt: The JSON Web Token to verify.
    :type jwt: str

    :param pub_key: The public key to be used to verify the token. Note: if you pass :obj:`None` then the token's signature will not be verified.
    :type pub_key: `_RSAobj <https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA._RSAobj-class.html>`_, `VerifyingKey <https://github.com/warner/python-ecdsa>`_, str or NoneType

    :param iat_skew: The amount of leeway to allow between the issuer's clock and the verifier's clock when verifiying that the token was generated in the past. Defaults to no leeway.
    :type iat_skew: datetime.timedelta

    :rtype: tuple
    :returns: ``(header, claims)`` if the token was verified successfully. The token must pass the following tests:

    - Its signature must verify using the public key or its algorithm must be ``none``.
    - Its header must contain a property **typ** with the value ``JWT``.
    - Its claims must contain a property **iat** which represents a date in the past (taking into account :obj:`iat_skew`).
    - Its claims must contian a property **nbf** which represents a date in the past.
    - Its claims must contain a property **exp** which represents a date in the future.

    :raises: If the token failed to verify.
    """
    header, claims, sig = jwt.split('.')

    header = jws.utils.from_base64(header)
    parsed_header = jws.utils.from_json(header)
    claims = jws.utils.from_base64(claims)

    if pub_key and parsed_header['alg'] != 'none':
        jws.verify(header, claims, sig, pub_key, True)

    header = parsed_header
    claims = jws.utils.from_json(claims)

    utcnow = datetime.utcnow()
    now = timegm(utcnow.utctimetuple())

    if header.get('typ') and header['typ'] != 'JWT':
        raise _JWTError('type is not JWT')

    if claims.get('iat') and claims['iat'] > timegm((utcnow + iat_skew).utctimetuple()):
        raise _JWTError('issued in the future')

    if claims.get('nbf') and claims['nbf'] > now:
        raise _JWTError('not yet valid')

    if claims.get('exp') and claims['exp'] <= now:
        raise _JWTError('expired')

    return header, claims

def process_jwt(jwt):
    """
    Process a JSON Web Token without verifying it.

    Call this before :func:`verify_jwt` if you need access to the header or claims in the token before verifying it. For example, the claims might identify the issuer such that you can retrieve the appropriate public key.

    :param jwt: The JSON Web Token to verify.
    :type jwt: str

    :rtype: tuple
    :returns: ``(header, claims)``
    """
    header, claims, _ = jwt.split('.')
    header = jws.utils.decode(header)
    claims = jws.utils.decode(claims)
    return header, claims

