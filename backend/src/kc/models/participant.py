from __future__ import annotations

import typing as t

from kc.contrib.sqlalchemy import *
from kc.models.segment_registration import SegmentRegistration

if t.TYPE_CHECKING:
    from kc.models.account import Account
    from kc.models.event_registration import EventRegistration


class Participant(UUIDAuditBase):
    __tablename__ = "participant"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("account.id", ondelete="cascade"),
        unique=True,
    )
    country: Mapped[str] = mapped_column()
    postal_code: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    address_line1: Mapped[str] = mapped_column()
    address_line2: Mapped[str | None] = mapped_column(default=None)
    is_student: Mapped[bool] = mapped_column()
    school_name: Mapped[str | None] = mapped_column(default=None)

    account: Mapped[Account] = relationship(
        foreign_keys="Participant.account_id",
        lazy="joined",
        cascade="all, delete",
    )
    event_registrations: Mapped[list[EventRegistration]] = relationship(
        back_populates="participant",
        cascade="all, delete-orphan",
        lazy="noload",
    )
    segment_registrations: Mapped[list[SegmentRegistration]] = relationship(
        back_populates="participant",
        cascade="all, delete-orphan",
        lazy="noload",
    )
