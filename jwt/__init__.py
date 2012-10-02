
from datetime import datetime
from calendar import timegm
from base64 import urlsafe_b64encode
from os import urandom
import jws

def to_jwt(claim, rsa_priv_key, lifetime=None, expires=None):
    header = {
        'typ': 'JWT',
        'alg': 'RS512'
    }

    now = datetime.utcnow()

    claim['jti'] = urlsafe_b64encode(urandom(128))
    claim['nbf'] = timegm(now.utctimetuple())
    claim['iat'] = timegm(now.utctimetuple())

    if lifetime:
        claim['exp'] = timegm((now + lifetime).utctimetuple())
    elif expires:
        claim['exp'] = timegm(expires.utctimetuple())

    return "%s.%s.%s" % (
        jws.utils.encode(header),
        jws.utils.encode(claim),
        jws.sign(header, claim, rsa_priv_key)
    )

