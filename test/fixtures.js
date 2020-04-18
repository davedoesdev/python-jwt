/*jslint node: true */
"use strict";

const crypto = require('crypto');
const sinon = require('sinon');
const { JWK, JWT } = require('jose');

function generate(time, header, claims, expires, not_before, key) {
    const clock = sinon.useFakeTimers(time * 1000);
    claims.exp = expires;
    claims.nbf = not_before;
    try {
        process.stdout.write(JWT.sign(claims, JWK.asKey(key), {
            algorithm: header.alg,
            jti: crypto.randomBytes(16).toString('hex'),
            kid: false,
            header: { typ: 'JWT' }
        }));
    } finally {
        clock.restore();
    }
}

function verify(time, sjwt, iat_skew, key, alg) {
    const clock = sinon.useFakeTimers(time * 1000);
    try {
        const { header, payload } = JWT.verify(sjwt, JWK.asKey(key), {
            algorithms: [ alg ],
            ignoreIat: true,
            complete: true
        });
        if (payload.iat > (Math.floor(Date.now() / 1000) + iat_skew)) {
            throw new Error('issued in the future');
        }
        process.stdout.write(JSON.stringify([header, payload]));
    } finally {
        clock.restore();
    }
}

exports.generate = generate;
exports.verify = verify;
