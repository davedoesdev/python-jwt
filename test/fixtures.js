/*jslint node: true */
"use strict";

const crypto = require('crypto');
const { importJWK, importPKCS8, importSPKI, SignJWT, jwtVerify } = require('jose');

async function import_key(key, alg) {
    if (key.startsWith('-----BEGIN PRIVATE KEY-----')) {
        return await importPKCS8(key);
    }
    if (key.startsWith('-----BEGIN PUBLIC KEY-----')) {
        return await importSPKI(key);
    }
    return await importJWK({
        kty: 'oct',
        k: Buffer.from(key, 'utf8').toString('base64url')
    }, alg);
}

async function generate(time, header, claims, expires, not_before, key) {
    claims.exp = expires;
    claims.nbf = not_before;
    process.stdout.write(await new SignJWT(Object.assign({}, claims, {
            jti: crypto.randomBytes(16).toString('hex')
        }))
        .setProtectedHeader({
            alg: header.alg,
            typ: 'JWT'
        })
        .setIssuedAt(time)
        .sign(await import_key(key, header.alg)));
}

async function verify(time, sjwt, iat_skew, key, alg) {
    const { header, payload } = jwtVerify(sjwt, await import_key(key, alg), {
        algorithms: [ alg ],
        clockTolerance: iat_skew,
        currentDate: new Date(time * 1000)
    });
    process.stdout.write(JSON.stringify([header, payload]));
}

exports.generate = generate;
exports.verify = verify;
