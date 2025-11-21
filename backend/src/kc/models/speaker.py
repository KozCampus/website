from __future__ import annotations

import typing as t

from kc.contrib.sqlalchemy import *

if t.TYPE_CHECKING:
    from kc.models.account import Account


class Speaker(UUIDAuditBase):
    __tablename__ = "speaker"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("account.id", ondelete="cascade"),
        unique=True,
        nullable=False,
    )
    introduction: Mapped[str] = mapped_column(default="")

    account: Mapped[Account] = relationship(
        foreign_keys="Speaker.account_id",
        lazy="joined",
        cascade="all, delete",
    )
