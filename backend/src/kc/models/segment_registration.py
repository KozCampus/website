from __future__ import annotations

import typing as t

from kc.contrib.sqlalchemy import *

if t.TYPE_CHECKING:
    from kc.models.participant import Participant
    from kc.models.segment import Segment


class SegmentRegistration(UUIDAuditBase):
    __tablename__ = "segment_registration"

    participant_id: Mapped[UUID] = mapped_column(
        ForeignKey("participant.id", ondelete="cascade"),
    )
    segment_id: Mapped[UUID] = mapped_column(
        ForeignKey("segment.id", ondelete="cascade"),
    )

    participant: Mapped[Participant] = relationship(
        back_populates="segment_registrations",
        foreign_keys="SegmentRegistration.participant_id",
        lazy="joined",
    )
    segment: Mapped[Segment] = relationship(
        back_populates="registrations",
        foreign_keys="SegmentRegistration.segment_id",
        lazy="joined",
    )
