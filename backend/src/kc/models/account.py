from __future__ import annotations

from kc.contrib.sqlalchemy import *


class Account(UUIDAuditBase):
    __tablename__ = "account"

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(unique=True, default=None)
    phone: Mapped[str | None] = mapped_column(unique=True, default=None)
    birth_date: Mapped[date | None] = mapped_column(default=None)
    password_hash: Mapped[str | None] = mapped_column(default=None)
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    encrypted_totp_secret: Mapped[str | None] = mapped_column(default=None)
