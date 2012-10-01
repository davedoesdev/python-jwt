
from datetime import datetime
from calendar import timegm
from base64 import urlsafe_b64encode
from os import urandom

from Crypto.Hash import SHA512 as Hasher
from hashlib import sha512 as hasher
from python_pkcs1_v1_5.wrapper import Wrapper
# From https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/Hash/SHA512.py
# Change oid if change hash method.
def _new_Hasher_new(data=""):
    obj = Wrapper(hasher, data)
    obj.oid = '\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x03'
    obj.new = _new_Hasher_new
    return obj
Hasher.new = _new_Hasher_new

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

