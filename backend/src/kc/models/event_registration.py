from kc.contrib.sqlalchemy import *

if t.TYPE_CHECKING:
    from kc.models.account import Account
    from kc.models.event import Event


class EventRegistration(UUIDAuditBase):
    __tablename__ = "event_registration"

    participant_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="cascade")
    )
    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("events.id", ondelete="cascade")
    )

    participant: Mapped[Account] = relationship(
        back_populates="event_registrations",
        foreign_keys="EventRegistration.participant_id",
        lazy="joined",
    )
    event: Mapped[Event] = relationship(
        back_populates="event_registrations",
        foreign_keys="EventRegistration.event_id",
        lazy="joined",
    )
