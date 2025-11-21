from __future__ import annotations

import typing as t

from kc.contrib.sqlalchemy import *

if t.TYPE_CHECKING:
    from kc.models.participant import Participant
    from kc.models.event import Event


class EventRegistration(UUIDAuditBase):
    __tablename__ = "event_registration"

    participant_id: Mapped[UUID] = mapped_column(
        ForeignKey("participant.id", ondelete="cascade")
    )
    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("event.id", ondelete="cascade")
    )

    participant: Mapped[Participant] = relationship(
        back_populates="event_registrations",
        foreign_keys="EventRegistration.participant_id",
        lazy="joined",
    )
    event: Mapped[Event] = relationship(
        back_populates="registrations",
        foreign_keys="EventRegistration.event_id",
        lazy="joined",
    )
