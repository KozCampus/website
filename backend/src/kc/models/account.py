from __future__ import annotations

from kc.contrib.sqlalchemy import *


class Account(UUIDAuditBase):
    __tablename__ = "accounts"

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column()
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    encrypted_totp_secret: Mapped[str | None] = mapped_column(default=None)
