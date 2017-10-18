\ |Build Status| |Coverage Status| |PyPI version|

Module for generating and verifying `JSON Web
Tokens <http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html>`__.

-  **Note:** From version 2.0.1 the namespace has changed from ``jwt``
   to ``python_jwt``, in order to avoid conflict with
   `PyJWT <https://github.com/jpadilla/pyjwt>`__.
-  **Note:** Versions 1.0.0 and later fix `a
   vulnerability <https://www.timmclean.net/2015/02/25/jwt-alg-none.html>`__
   in JSON Web Token verification so please upgrade if you're using this
   functionality. The API has changed so you will need to update your
   application.
   `verify\_jwt <http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/docs/_build/html/index.html#python_jwt.verify_jwt>`__
   now requires you to specify which signature algorithms are allowed.
-  Uses `jwcrypto <https://jwcrypto.readthedocs.io>`__ to do the heavy
   lifting.
-  Supports `**RS256**, **RS384**,
   **RS512** <http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.3>`__,
   `**PS256**, **PS384**,
   **PS512** <http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.5>`__,
   `**HS256**, **HS384**,
   **HS512** <http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.2>`__
   and
   `**none** <http://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-14#section-3.6>`__
   signature algorithms.
-  Unit tests, including tests for interoperability with
   `node-jsjws <https://github.com/davedoesdev/node-jsjws>`__.
-  Supports Python 3.6. **Note:**
   `generate\_jwt <http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/docs/_build/html/index.html#python_jwt.generate_jwt>`__
   returns the token as a Unicode string, even on Python 2.7.

Example:

.. code:: python

    import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
    key = jwk.JWK.generate(kty='RSA', size=2048)
    payload = { 'foo': 'bar', 'wup': 90 };
    token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))
    header, claims = jwt.verify_jwt(token, key, ['PS256'])
    for k in payload: assert claims[k] == payload[k]

The API is described
`here <http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/docs/_build/html/index.html>`__.

Installation
------------

.. code:: shell

    pip install python_jwt

Another Example
---------------

You can read and write keys from and to
`PEM-format <http://www.openssl.org/docs/crypto/pem.html>`__ strings:

.. code:: python

    import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
    key = jwk.JWK.generate(kty='RSA', size=2048)
    priv_pem = key.export_to_pem(private_key=True, password=None)
    pub_pem = key.export_to_pem()
    payload = { 'foo': 'bar', 'wup': 90 };
    priv_key = jwk.JWK.from_pem(priv_pem)
    pub_key = jwk.JWK.from_pem(pub_pem)
    token = jwt.generate_jwt(payload, priv_key, 'RS256', datetime.timedelta(minutes=5))
    header, claims = jwt.verify_jwt(token, pub_key, ['RS256'])
    for k in payload: assert claims[k] == payload[k]

Licence
-------

`MIT <https://raw.github.com/davedoesdev/python-jwt/master/LICENCE>`__

Tests
-----

.. code:: shell

    make test

Lint
----

.. code:: shell

    make lint

Code Coverage
-------------

.. code:: shell

    make coverage

`coverage.py <http://nedbatchelder.com/code/coverage/>`__ results are
available
`here <http://rawgit.davedoesdev.com/davedoesdev/python-jwt/master/coverage/html/index.html>`__.

Coveralls page is
`here <https://coveralls.io/r/davedoesdev/python-jwt>`__.

Benchmarks
----------

.. code:: shell

    make bench

Here are some results on a laptop with an Intel Core i5-4300M 2.6Ghz CPU
and 8Gb RAM running Ubuntu 17.04.

+----------------+---------------+------------+---------------+
| Generate Key   | user (ns)     | sys (ns)   | real (ns)     |
+================+===============+============+===============+
| RSA            | 103,100,000   | 200,000    | 103,341,537   |
+----------------+---------------+------------+---------------+

+------------------+-------------+------------+-------------+
| Generate Token   | user (ns)   | sys (ns)   | real (ns)   |
+==================+=============+============+=============+
| HS256            | 220,000     | 0          | 226,478     |
+------------------+-------------+------------+-------------+
| HS384            | 220,000     | 0          | 218,233     |
+------------------+-------------+------------+-------------+
| HS512            | 230,000     | 0          | 225,823     |
+------------------+-------------+------------+-------------+
| PS256            | 1,530,000   | 10,000     | 1,536,235   |
+------------------+-------------+------------+-------------+
| PS384            | 1,550,000   | 0          | 1,549,844   |
+------------------+-------------+------------+-------------+
| PS512            | 1,520,000   | 10,000     | 1,524,844   |
+------------------+-------------+------------+-------------+
| RS256            | 1,520,000   | 10,000     | 1,524,565   |
+------------------+-------------+------------+-------------+
| RS384            | 1,530,000   | 0          | 1,528,074   |
+------------------+-------------+------------+-------------+
| RS512            | 1,510,000   | 0          | 1,526,089   |
+------------------+-------------+------------+-------------+

+------------+-------------+------------+-------------+
| Load Key   | user (ns)   | sys (ns)   | real (ns)   |
+============+=============+============+=============+
| RSA        | 210,000     | 3,000      | 210,791     |
+------------+-------------+------------+-------------+

+----------------+-------------+------------+-------------+
| Verify Token   | user (ns)   | sys (ns)   | real (ns)   |
+================+=============+============+=============+
| HS256          | 100,000     | 0          | 101,478     |
+----------------+-------------+------------+-------------+
| HS384          | 100,000     | 10,000     | 103,014     |
+----------------+-------------+------------+-------------+
| HS512          | 110,000     | 0          | 104,323     |
+----------------+-------------+------------+-------------+
| PS256          | 230,000     | 0          | 231,058     |
+----------------+-------------+------------+-------------+
| PS384          | 240,000     | 0          | 237,551     |
+----------------+-------------+------------+-------------+
| PS512          | 240,000     | 0          | 232,450     |
+----------------+-------------+------------+-------------+
| RS256          | 230,000     | 0          | 227,737     |
+----------------+-------------+------------+-------------+
| RS384          | 230,000     | 0          | 230,698     |
+----------------+-------------+------------+-------------+
| RS512          | 230,000     | 0          | 228,624     |
+----------------+-------------+------------+-------------+

.. |Build Status| image:: https://travis-ci.org/davedoesdev/python-jwt.png
   :target: https://travis-ci.org/davedoesdev/python-jwt
.. |Coverage Status| image:: https://coveralls.io/repos/davedoesdev/python-jwt/badge.png?branch=master
   :target: https://coveralls.io/r/davedoesdev/python-jwt?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/python_jwt.png
   :target: http://badge.fury.io/py/python_jwt
