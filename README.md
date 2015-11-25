# python-jwt&nbsp;&nbsp;&nbsp;[![Build Status](https://travis-ci.org/davedoesdev/python-jwt.png)](https://travis-ci.org/davedoesdev/python-jwt) [![Coverage Status](https://coveralls.io/repos/davedoesdev/python-jwt/badge.png?branch=master)](https://coveralls.io/r/davedoesdev/python-jwt?branch=master) [![PyPI version](https://badge.fury.io/py/python_jwt.png)](http://badge.fury.io/py/python_jwt)

Module for generating and verifying [JSON Web Tokens](http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html).

- **Note:** Versions 1.0.0 and later fix [a vulnerability](https://www.timmclean.net/2015/02/25/jwt-alg-none.html) in JSON Web Token verification so please upgrade if you're using this functionality. The API has changed so you will need to update your application. [verify_jwt](http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/docs/_build/html/index.html#jwt.verify_jwt) now requires you to specify which signature algorithms are allowed.
- Uses [python-jws](https://github.com/brianloveswords/python-jws) to do the heavy lifting.
- Supports [__RS256__, __RS384__, __RS512__](http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.3), [__PS256__, __PS384__, __PS512__](http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.5), [__HS256__, __HS384__, __HS512__](http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.2) and [__none__](http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.6) signature algorithms.
- Unit tests, including tests for interoperability with [node-jsjws](https://github.com/davedoesdev/node-jsjws).
- Supports Python 3.4. **Note:** [generate_jwt](http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/docs/_build/html/index.html#jwt.generate_jwt) returns the token as a Unicode string, even on Python 2.7.

Example:

```python
import jwt, Crypto.PublicKey.RSA as RSA, datetime
key = RSA.generate(2048)
payload = { 'foo': 'bar', 'wup': 90 };
token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))
header, claims = jwt.verify_jwt(token, key, ['PS256'])
for k in payload: assert claims[k] == payload[k]
```

The API is described [here](http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/docs/_build/html/index.html).


## Installation

```shell
pip install python_jwt
```

## Another Example

You can read and write keys from and to [PEM-format](http://www.openssl.org/docs/crypto/pem.html) strings:

```python
import jwt, Crypto.PublicKey.RSA as RSA, datetime
key = RSA.generate(2048)
priv_pem = key.exportKey()
pub_pem = key.publickey().exportKey()
payload = { 'foo': 'bar', 'wup': 90 };
priv_key = RSA.importKey(priv_pem)
pub_key = RSA.importKey(pub_pem)
token = jwt.generate_jwt(payload, priv_key, 'RS256', datetime.timedelta(minutes=5))
header, claims = jwt.verify_jwt(token, pub_key, ['RS256'])
for k in payload: assert claims[k] == payload[k]
```

## Licence

[MIT](https://raw.github.com/davedoesdev/python-jwt/master/LICENCE)

## Tests

```shell
make test
```

## Lint

```shell
make lint
```

## Code Coverage

```shell
make coverage
```

[coverage.py](http://nedbatchelder.com/code/coverage/) results are available [here](http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/coverage/html/index.html).

Coveralls page is [here](https://coveralls.io/r/davedoesdev/python-jwt).

## Benchmarks

```shell
make bench
```

Here are some results on a laptop with an Intel Core i5-3210M 2.5Ghz CPU and 6Gb RAM running Ubuntu 13.04.

Generate Key|user (ns)|sys (ns)|real (ns)
:--|--:|--:|--:
RSA|152,700,000|300,000|152,906,095

Generate Token|user (ns)|sys (ns)|real (ns)
:--|--:|--:|--:
HS256|140,000|10,000|157,202
HS384|160,000|10,000|156,403
HS512|139,999|20,000|153,212
PS256|3,159,999|49,999|3,218,649
PS384|3,170,000|10,000|3,176,899
PS512|3,120,000|9,999|3,141,219
RS256|3,070,000|20,000|3,094,644
RS384|3,090,000|0|3,092,471
RS512|3,079,999|20,000|3,095,314

Load Key|user (ns)|sys (ns)|real (ns)
:--|--:|--:|--:
RSA|811,000|0|810,139

Verify Token|user (ns)|sys (ns)|real (ns)
:--|--:|--:|--:
HS256|140,000|0|129,947
HS384|130,000|0|130,161
HS512|119,999|0|128,850
PS256|780,000|10,000|775,609
PS384|759,999|0|752,933
PS512|739,999|0|738,118
RS256|700,000|0|719,365
RS384|719,999|0|721,524
RS512|730,000|0|719,706

