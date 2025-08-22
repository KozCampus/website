from __future__ import annotations

import uuid
import secrets
from uuid import UUID

import msgspec
from kc.contrib.litestar import AppSettings
from kc.contrib.openai import OpenAISettings
from kc.contrib.msgspec import Struct


class VPNAPISettings(Struct):
    api_key: str = ""


class TOTPSettings(Struct):
    fernet_key: str = ""


class Settings(AppSettings):
    instance_id: UUID = msgspec.field(default_factory=uuid.uuid4)
    name: str = "Local Instance"
    description: str = "Local Instance"
    secret: str = msgspec.field(
        default_factory=lambda: secrets.token_urlsafe(32),
    )
    account_id: UUID = msgspec.field(default_factory=uuid.uuid4)


    vpnapi: VPNAPISettings = msgspec.field(
        default_factory=VPNAPISettings,
    )

    openai: OpenAISettings = msgspec.field(
        default_factory=OpenAISettings,
    )

    totp: TOTPSettings = msgspec.field(
        default_factory=TOTPSettings,
    )
