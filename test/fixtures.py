""" Common globals """

import sys
from os import urandom
from binascii import hexlify
from jwcrypto.jwk import JWK
from jwcrypto.common import base64url_encode

if sys.version_info < (3, 0):
    _binary_type = str
else:
    _binary_type = bytes

def to_bytes_2and3(s):
    """ Ensure string is binary """
    return s if isinstance(s, _binary_type) else s.encode('utf-8')

payload = {
    "foo": "joe",
    u"hell\u25C9": u"th\u0113re",
    "bar": 2398742.23092384,
    "http://example.com/is_root": True
}

rsa_priv_pem = "-----BEGIN RSA PRIVATE KEY-----                 \n\
MIIEogIBAAKCAQEA4qiw8PWs7PpnnC2BUEoDRcwXF8pq8XT1/3Hc3cuUJwX/otNe\n\
fr/Bomr3dtM0ERLN3DrepCXvuzEU5FcJVDUB3sI+pFtjjLBXD/zJmuL3Afg91J9p\n\
79+Dm+43cR6wuKywVJx5DJIdswF6oQDDzhwu89d2V5x02aXB9LqdXkPwiO0eR5s/\n\
xHXgASl+hqDdVL9hLod3iGa9nV7cElCbcl8UVXNPJnQAfaiKazF+hCdl/syrIh0K\n\
CZ5opggsTJibo8qFXBmG4PkT5YbhHE11wYKILwZFSvZ9iddRPQK3CtgFiBnXbVwU\n\
5t67tn9pMizHgypgsfBoeoyBrpTuc4egSCpjsQIDAQABAoIBAF2sU/wxvHbwAhQE\n\
pnXVMMcO0thtOodxzBz3JM2xThhWnVDgxCPkAhWq2X0NSm5n9BY5ajwyxYH6heTc\n\
p6lagtxaMONiNaE2W7TqxzMw696vhnYyL+kH2e9+owEoKucXz4QYatqsJIQPb2vM\n\
0h+DfFAgUvNgYNZ2b9NBsLn9oBImDfYueHyqpRGTdX5urEVtmQz029zaC+jFc7BK\n\
Y6qBRSTwFwnVgE+Td8UgdrO3JQ/0Iwk/lkphnhls/BYvdNC5O8oEppozNVmMV8jm\n\
61K+agOh1KD8ky60iQFjo3VdFpUjI+W0+sYiYpDb4+Z9OLOTK/5J2EBAGim9siyd\n\
gHspx+UCgYEA9+t5Rs95hG9Q+6mXn95hYduPoxdFCIFhbGl6GBIGLyHUdD8vmgwP\n\
dHo7Y0hnK0NyXfue0iFBYD94/fuUe7GvcXib93heJlvPx9ykEZoq9DZnhPFBlgIE\n\
SGeD8hClazcr9O99Fmg3e7NyTuVou+CIublWWlFyN36iamP3a08pChsCgYEA6gvT\n\
pi/ZkYI1JZqxXsTwzAsR1VBwYslZoicwGNjRzhvuqmqwNvK17dnSQfIrsC2VnG2E\n\
UbE5EIAWbibdoL4hWUpPx5Tl096OjC3qBR6okAxbVtVEY7Rmv7J9RwriXhtD1DYp\n\
eBvo3eQonApFkfI8Lr2kuKGIgwzkZ72QLXsKJiMCgYBZXBCci0/bglwIObqjLv6e\n\
zQra2BpT1H6PGv2dC3IbLvBq7hN0TQCNFTmusXwuReNFKNq4FrB/xqEPusxsQUFh\n\
fv2Il2QoI1OjUE364jy1RZ7Odj8TmKp+hoEykPluybYYVPIbT3kgJy/+bAXyIh5m\n\
Av2zFEQ86HIWMu4NSb0bHQKBgETEZNOXi52tXGBIK4Vk6DuLpRnAIMVl0+hJC2DB\n\
lCOzIVUBM/VxKvNP5O9rcFq7ihIEO7SlFdc7S1viH4xzUOkjZH2Hyl+OLOQTOYd3\n\
kp+AgfXpg8an4ujAUP7mu8xaxns7zsNzr+BCgYwXmIlhWz2Aiz2UeL/IsfOpRwuV\n\
801xAoGADQB84MJe/X8xSUZQzpn2KP/yZ7C517qDJjComGe3mjVxTIT5XAaa1tLy\n\
T4mvpSeYDJkBD8Hxr3fB1YNDWNbgwrNPGZnUTBNhxIsNLPnV8WySiW57LqVXlggH\n\
vjFmyDdU5Hh6ma4q+BeAqbXZSJz0cfkBcBLCSe2gIJ/QJ3YJVQI=            \n\
-----END RSA PRIVATE KEY-----"

rsa_pub_pem = "-----BEGIN PUBLIC KEY-----                       \n\
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4qiw8PWs7PpnnC2BUEoD\n\
RcwXF8pq8XT1/3Hc3cuUJwX/otNefr/Bomr3dtM0ERLN3DrepCXvuzEU5FcJVDUB\n\
3sI+pFtjjLBXD/zJmuL3Afg91J9p79+Dm+43cR6wuKywVJx5DJIdswF6oQDDzhwu\n\
89d2V5x02aXB9LqdXkPwiO0eR5s/xHXgASl+hqDdVL9hLod3iGa9nV7cElCbcl8U\n\
VXNPJnQAfaiKazF+hCdl/syrIh0KCZ5opggsTJibo8qFXBmG4PkT5YbhHE11wYKI\n\
LwZFSvZ9iddRPQK3CtgFiBnXbVwU5t67tn9pMizHgypgsfBoeoyBrpTuc4egSCpj\n\
sQIDAQAB                                                        \n\
-----END PUBLIC KEY-----"

rsa_priv_key = JWK.from_pem(to_bytes_2and3(rsa_priv_pem))
rsa_pub_key = JWK.from_pem(to_bytes_2and3(rsa_pub_pem))

ec_p256_priv_pem = "-----BEGIN EC PRIVATE KEY-----              \n\
MHcCAQEEIHUzppsG3mykCT4wm/zle/61EiRxMrqhMuIhJ9ODYSSPoAoGCCqGSM49\n\
AwEHoUQDQgAEXkWPnLkwayWN5S1m5b6+3ZMlOi4IdMYQx6tGwPdCZLUko3sqIQHp\n\
CLCxpT9Cis1hHR/kWy4Tr18Ow3tBi9YKLA==                            \n\
-----END EC PRIVATE KEY-----"

ec_p256_pub_pem = "-----BEGIN PUBLIC KEY-----                   \n\
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEXkWPnLkwayWN5S1m5b6+3ZMlOi4I\n\
dMYQx6tGwPdCZLUko3sqIQHpCLCxpT9Cis1hHR/kWy4Tr18Ow3tBi9YKLA==    \n\
-----END PUBLIC KEY-----"

ec_p256_priv_key = JWK.from_pem(to_bytes_2and3(ec_p256_priv_pem))
ec_p256_pub_key = JWK.from_pem(to_bytes_2and3(ec_p256_pub_pem))

ec_p256k_priv_pem = "-----BEGIN EC PRIVATE KEY-----             \n\
MHQCAQEEIFhSYfpa4vthbQPj+zBWe2KAyzi2h0F3mAEEDGXGQWSqoAcGBSuBBAAK\n\
oUQDQgAEoCGAhYo5kCRHKIGU5ATdoOrT8cIHNJ0QdF/Z+mWwBWyZLMU134kFiq3L\n\
d5HvX7Glq2wNXsdVL+nkraF09DqmKg==                                \n\
-----END EC PRIVATE KEY-----"

ec_p256k_pub_pem = "-----BEGIN PUBLIC KEY-----                  \n\
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEoCGAhYo5kCRHKIGU5ATdoOrT8cIHNJ0Q\n\
dF/Z+mWwBWyZLMU134kFiq3Ld5HvX7Glq2wNXsdVL+nkraF09DqmKg==        \n\
-----END PUBLIC KEY-----"

ec_p256k_priv_key = JWK.from_pem(to_bytes_2and3(ec_p256k_priv_pem))
ec_p256k_pub_key = JWK.from_pem(to_bytes_2and3(ec_p256k_pub_pem))

ec_p384_priv_pem = "-----BEGIN EC PRIVATE KEY-----              \n\
MIGkAgEBBDD26eiD4oZG7vGOM3++/Aunr+O5sj0uk98LRO/zo/djbyKR+9NlUbQi\n\
WoZ/cLyrsYOgBwYFK4EEACKhZANiAAT/fYfrdozbYy9CNL4BCsYevZx1S23mZhJH\n\
5ujAqBCDyWuJ7QJp8nuaONnqxyoeuIBUUniED7k8ZdyULKNqVumtzqdwARReII+y\n\
cuOhey7xWcZd3yau4Tv70Cd3Z6A49KY=                                \n\
-----END EC PRIVATE KEY-----"

ec_p384_pub_pem = "-----BEGIN PUBLIC KEY-----                   \n\
MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAE/32H63aM22MvQjS+AQrGHr2cdUtt5mYS\n\
R+bowKgQg8lrie0CafJ7mjjZ6scqHriAVFJ4hA+5PGXclCyjalbprc6ncAEUXiCP\n\
snLjoXsu8VnGXd8mruE7+9And2egOPSm                                \n\
-----END PUBLIC KEY-----"

ec_p384_priv_key = JWK.from_pem(to_bytes_2and3(ec_p384_priv_pem))
ec_p384_pub_key = JWK.from_pem(to_bytes_2and3(ec_p384_pub_pem))

ec_p521_priv_pem = "-----BEGIN EC PRIVATE KEY-----              \n\
MIHcAgEBBEIAEc9JKWjwtGrA67E+b3QDS3OYOJEPgZuSYE1gA8tFnWTbDtBUDBPo\n\
ZhbwfKE+ozMlJ7g9R9TohnT3RupQnIttZgigBwYFK4EEACOhgYkDgYYABAHpBrSt\n\
Y7gHSMNLga3heEsy9XJqHrxzOfniINKj6IPkA/c2JnhHqTxxrM2czQov+iVf3Tm1\n\
Gp37G94OdFEl1e/UywAlriBuDvmIDVjPve8e8ZRYTYKVpsL713c1u1SFBzsmbo+p\n\
U8pRn7Rnueu7WF+y5mZqN8MDxIXHrvjigqr1G8yxKQ==                    \n\
-----END EC PRIVATE KEY-----"

ec_p521_pub_pem = "-----BEGIN PUBLIC KEY-----                   \n\
MIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQB6Qa0rWO4B0jDS4Gt4XhLMvVyah68\n\
czn54iDSo+iD5AP3NiZ4R6k8cazNnM0KL/olX905tRqd+xveDnRRJdXv1MsAJa4g\n\
bg75iA1Yz73vHvGUWE2ClabC+9d3NbtUhQc7Jm6PqVPKUZ+0Z7nru1hfsuZmajfD\n\
A8SFx6744oKq9RvMsSk=                                            \n\
-----END PUBLIC KEY-----"

ec_p521_priv_key = JWK.from_pem(to_bytes_2and3(ec_p521_priv_pem))
ec_p521_pub_key = JWK.from_pem(to_bytes_2and3(ec_p521_pub_pem))

okp_ed25519_priv_pem = "-----BEGIN PRIVATE KEY-----             \n\
MC4CAQAwBQYDK2VwBCIEIIIQgV+pN7DLacgbsuuP7gZ2RrjBCotI7QYTm8KwAnL7\n\
-----END PRIVATE KEY-----"

okp_ed25519_pub_pem = "-----BEGIN PUBLIC KEY-----           \n\
MCowBQYDK2VwAyEAvNB3YCZtON09oUTyTycaSRv5TblOvKHVM70AQ1q18zs=\n\
-----END PUBLIC KEY-----"

okp_ed25519_priv_key = JWK.from_pem(to_bytes_2and3(okp_ed25519_priv_pem))
okp_ed25519_pub_key = JWK.from_pem(to_bytes_2and3(okp_ed25519_pub_pem))

priv_keys = {
    'HS256': {'python-jwt': JWK(kty='oct', k=base64url_encode('some random key some random key some random key'))},
    'HS384': {'python-jwt': JWK(kty='oct', k=base64url_encode('another one another one another one another one another one'))},
    'HS512': {'python-jwt': JWK(kty='oct', k=base64url_encode('keys keys keys! keys keys keys! keys keys keys! keys keys keys! keys keys keys!'))},
    'RS256': {'python-jwt': rsa_priv_key},
    'RS384': {'python-jwt': rsa_priv_key},
    'RS512': {'python-jwt': rsa_priv_key},
    'PS256': {'python-jwt': rsa_priv_key},
    'PS384': {'python-jwt': rsa_priv_key},
    'PS512': {'python-jwt': rsa_priv_key},
    'ES256': {'python-jwt': ec_p256_priv_key},
    'ES256K': {'python-jwt': ec_p256k_priv_key},
    'ES384': {'python-jwt': ec_p384_priv_key},
    'ES512': {'python-jwt': ec_p521_priv_key},
    'EdDSA': {'python-jwt': okp_ed25519_priv_key}
}

pub_keys = {
    'HS256': {'python-jwt': priv_keys['HS256']['python-jwt']},
    'HS384': {'python-jwt': priv_keys['HS384']['python-jwt']},
    'HS512': {'python-jwt': priv_keys['HS512']['python-jwt']},
    'RS256': {'python-jwt': rsa_pub_key},
    'RS384': {'python-jwt': rsa_pub_key},
    'RS512': {'python-jwt': rsa_pub_key},
    'PS256': {'python-jwt': rsa_pub_key},
    'PS384': {'python-jwt': rsa_pub_key},
    'PS512': {'python-jwt': rsa_pub_key},
    'ES256': {'python-jwt': ec_p256_pub_key},
    'ES256K': {'python-jwt': ec_p256k_pub_key},
    'ES384': {'python-jwt': ec_p384_pub_key},
    'ES512': {'python-jwt': ec_p521_pub_key},
    'EdDSA': {'python-jwt': okp_ed25519_pub_key}
}

generated_rsa_key = JWK.generate(kty='RSA', size=2048)

generated_keys = {
    'HS256': JWK(kty='oct', k=base64url_encode(hexlify(urandom(16)))),
    'HS384': JWK(kty='oct', k=base64url_encode(hexlify(urandom(16)))),
    'HS512': JWK(kty='oct', k=base64url_encode(hexlify(urandom(16)))),
    'RS256': generated_rsa_key,
    'RS384': generated_rsa_key,
    'RS512': generated_rsa_key,
    'PS256': generated_rsa_key,
    'PS384': generated_rsa_key,
    'PS512': generated_rsa_key,
    'ES256': JWK.generate(kty='EC', crv='P-256'),
    'ES256K': JWK.generate(kty='EC', crv='secp256k1'),
    'ES384': JWK.generate(kty='EC', crv='P-384'),
    'ES512': JWK.generate(kty='EC', crv='P-521'),
    'EdDSA': JWK.generate(kty='OKP', crv='Ed25519')
}

algs = list(priv_keys.keys())
