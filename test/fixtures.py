""" Common globals """

from os import urandom
from binascii import hexlify

import Crypto.PublicKey.RSA as RSA

payload = {
    "foo": "joe",
    u"hell\u25C9": u"th\u0113re",
    "bar": 2398742.23092384,
    "http://example.com/is_root": True
}

priv_pem = "-----BEGIN RSA PRIVATE KEY-----                 \n\
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

pub_pem = "-----BEGIN PUBLIC KEY-----                       \n\
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4qiw8PWs7PpnnC2BUEoD\n\
RcwXF8pq8XT1/3Hc3cuUJwX/otNefr/Bomr3dtM0ERLN3DrepCXvuzEU5FcJVDUB\n\
3sI+pFtjjLBXD/zJmuL3Afg91J9p79+Dm+43cR6wuKywVJx5DJIdswF6oQDDzhwu\n\
89d2V5x02aXB9LqdXkPwiO0eR5s/xHXgASl+hqDdVL9hLod3iGa9nV7cElCbcl8U\n\
VXNPJnQAfaiKazF+hCdl/syrIh0KCZ5opggsTJibo8qFXBmG4PkT5YbhHE11wYKI\n\
LwZFSvZ9iddRPQK3CtgFiBnXbVwU5t67tn9pMizHgypgsfBoeoyBrpTuc4egSCpj\n\
sQIDAQAB                                                        \n\
-----END PUBLIC KEY-----"

priv_key = RSA.importKey(priv_pem)
pub_key = RSA.importKey(pub_pem)

priv_keys = {
    'HS256': {'default': 'some random key'},
    'HS384': {'default': 'another one'},
    'HS512': {'default': 'keys keys keys!'},
    'RS256': {'python-jwt': priv_key},
    'RS384': {'python-jwt': priv_key},
    'RS512': {'python-jwt': priv_key},
    'PS256': {'python-jwt': priv_key},
    'PS384': {'python-jwt': priv_key},
    'PS512': {'python-jwt': priv_key}
}

pub_keys = {
    'HS256': {'default': priv_keys['HS256']['default']},
    'HS384': {'default': priv_keys['HS384']['default']},
    'HS512': {'default': priv_keys['HS512']['default']},
    'RS256': {'python-jwt': pub_key},
    'RS384': {'python-jwt': pub_key},
    'RS512': {'python-jwt': pub_key},
    'PS256': {'python-jwt': pub_key},
    'PS384': {'python-jwt': pub_key},
    'PS512': {'python-jwt': pub_key}
}

generated_key = RSA.generate(2048)

generated_keys = {
    'HS256': hexlify(urandom(16)),
    'HS384': hexlify(urandom(16)),
    'HS512': hexlify(urandom(16)),
    'RS256': generated_key,
    'RS384': generated_key,
    'RS512': generated_key,
    'PS256': generated_key,
    'PS384': generated_key,
    'PS512': generated_key
}

algs = list(priv_keys.keys())
