from __future__ import annotations

import typing as t

from kc.contrib.sqlalchemy import *
from kc.enums import RegistrationPolicy

if t.TYPE_CHECKING:
    from kc.models.segment import Segment
    from kc.models.event_registration import EventRegistration


class Event(UUIDAuditBase):
    __tablename__ = "event"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(default=None)
    registration_policy: Mapped[RegistrationPolicy] = mapped_column(
        default=RegistrationPolicy.CLOSED,
    )

    segments: Mapped[list[Segment]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="noload",
    )
    registrations: Mapped[list[EventRegistration]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="noload",
    )
