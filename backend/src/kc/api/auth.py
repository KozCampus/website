from __future__ import annotations

import time
import qrcode
import io
import base64
from uuid import UUID

import pyotp
from authlib.jose import jwt, JWTClaims
from cryptography import fernet
from passlib.context import CryptContext

from kc.contrib.msgspec import *
from kc.api import get_settings
from kc.api.schemas import TOTPSchema
from kc.api.exceptions import *


_pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def verify_password(
    plain: str,
    hashed: str,
) -> bool:
    return _pwd_context.verify(plain, hashed)


def hash_password(
    plain: str,
) -> str:
    return _pwd_context.hash(plain)


def get_token_from_cookies(cookies: dict[str, str]) -> str | None:
    settings = get_settings()

    if settings.api.debug:
        return cookies.get("Auth")
    else:
        return cookies.get("__Secure-Auth")


class Claims(Struct):
    sub: UUID
    exp: int
    iat: int
    scope: str


JWT_LIFETIME = 60 * 60 * 24 * 7  # 1 week


def create_claims(
    account_id: UUID,
    account_read: bool = True,
    account_write: bool = False,
) -> Claims:
    scope_list = []

    if account_read:
        scope_list.append("account:read")
    
    if account_write:
        scope_list.append("account:write")

    scope_string = " ".join(scope_list)

    now = int(time.time())

    claims = Claims(
        sub=account_id,
        exp=now + JWT_LIFETIME,
        iat=now,
        scope=scope_string,
    )

    return claims


def issue_token(claims: Claims) -> str:
    header = {"alg": "HS256"}
    settings = get_settings()
    secret = settings.api.jwt_secret_key
    payload = msgspec.to_builtins(claims, builtin_types=(str, int))
    token = jwt.encode(header, payload, secret).decode("utf-8")
    print(token, type(token))
    return token


def decode_token(token: str) -> Claims | None:
    settings = get_settings()
    secret = settings.api.jwt_secret_key
    
    try:
        payload: JWTClaims = jwt.decode(token, secret)
        payload.validate(leeway=5)
        return msgspec.convert(payload, Claims)
    except:
        return None


def get_claims_from_token(
    token: str | None,
) -> Claims | None:
    if token is None:
        raise TokenMissingError()
    
    claims = decode_token(token)
    
    if not claims:
        raise TokenInvalidError()
    
    return claims


def get_claims_from_cookies(
    cookies: dict[str, str],
) -> Claims | None:
    token = get_token_from_cookies(cookies)
    return get_claims_from_token(token)


def encrypt_totp_secret(plain_secret: str) -> str:
    settings = get_settings()
    fernet_key = settings.totp.fernet_key
    fernet_instance = fernet.Fernet(fernet_key)
    encrypted_secret = fernet_instance.encrypt(plain_secret.encode("utf-8"))
    return encrypted_secret.decode("utf-8")


def decrypt_totp_secret(encrypted_secret: str) -> str:
    settings = get_settings()
    fernet_key = settings.totp.fernet_key
    fernet_instance = fernet.Fernet(fernet_key)
    plain_secret = fernet_instance.decrypt(encrypted_secret.encode("utf-8"))
    return plain_secret.decode("utf-8")


def issue_totp_secret(name: str) -> TOTPSchema:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=name, issuer_name="KözCampus")

    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return TOTPSchema(
        secret=secret,
        uri=uri,
        qr_code=f"data:image/png;base64,{qr_code}",
    )


def verify_totp(account_id: UUID, encrypted_secret: str, code: str) -> str:
    try:
        secret = decrypt_totp_secret(encrypted_secret)
        totp = pyotp.TOTP(secret)
        is_verified = totp.verify(code)

        if not is_verified:
            raise TOTPError()
        
        claims = create_claims(account_id)
        return issue_token(claims)

    except Exception as e:
        raise TOTPError() from e
