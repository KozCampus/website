from __future__ import annotations

import typing as t

from kc.contrib.sqlalchemy import *
from kc.enums import RegistrationPolicy

if t.TYPE_CHECKING:
    from kc.models.event import Event
    from kc.models.segment_registration import SegmentRegistration


class Segment(UUIDAuditBase):
    __tablename__ = "segment"

    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("event.id", ondelete="cascade"),
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(default=None)
    registration_policy: Mapped[RegistrationPolicy] = mapped_column(
        default=RegistrationPolicy.CLOSED,
    )

    event: Mapped[Event] = relationship(
        foreign_keys="Segment.event_id",
        back_populates="segments",
        lazy="joined",
    )
    registrations: Mapped[list[SegmentRegistration]] = relationship(
        back_populates="segment",
        cascade="all, delete-orphan",
        lazy="noload",
    )
