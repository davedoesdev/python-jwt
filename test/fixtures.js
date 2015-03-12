/*jslint node: true */
"use strict";

var sinon = require('sinon'),
    jsjws = require('jsjws');

function generate(time, header, claims, expires, not_before, key)
{
    if (key.indexOf('-----BEGIN') === 0)
    {
        key = jsjws.createPrivateKey(key, 'utf8');
    }

    var clock = sinon.useFakeTimers(time * 1000);

    try
    {
        expires = new Date(expires * 1000);
        not_before = new Date(not_before * 1000);

        process.stdout.write(new jsjws.JWT().generateJWTByKey(header, claims, expires, not_before, key));
    }
    finally
    {
        clock.restore();
    }
}

function verify(time, sjwt, iat_skew, key, alg)
{
    if (key.indexOf('-----BEGIN') === 0)
    {
        key = jsjws.createPublicKey(key, 'utf8');
    }

    var clock = sinon.useFakeTimers(time * 1000), jwt;

    try
    {
        jwt = new jsjws.JWT();

        jwt.verifyJWTByKey(sjwt, {iat_skew: iat_skew}, key, [alg]);

        process.stdout.write(JSON.stringify([jwt.getParsedHeader(), jwt.getParsedPayload()]));
    }
    finally
    {
        clock.restore();
    }
}

exports.generate = generate;
exports.verify = verify;
