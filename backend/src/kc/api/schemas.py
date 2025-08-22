from __future__ import annotations

from kc.contrib.msgspec import *


class ClientLogin(Struct):
    email: str
    password: str


class AccountRegister(Struct):
    name: str
    email: str
    password: str


class AccountSchema(Struct):
    id: UUID
    name: str
    email: str
    is_email_verified: bool
    is_banned: bool
    is_admin: bool


class AccountCreate(Struct):
    name: str
    email: str
    password_hash: str


class AccountUpdate(Struct):
    name: str | None
    is_banned: bool | None
    is_admin: bool | None


class TOTPSchema(Struct):
    secret: str
    uri: str
    qr_code: str
