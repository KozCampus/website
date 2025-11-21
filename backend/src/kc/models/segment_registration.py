from kc.contrib.sqlalchemy import *

if t.TYPE_CHECKING:
    from kc.models.account import Account
    from kc.models.segment import Segment


class SegmentRegistration(UUIDAuditBase):
    __tablename__ = "segment_registration"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="cascade"),
    )
    segment_id: Mapped[UUID] = mapped_column(
        ForeignKey("segments.id", ondelete="cascade"),
    )

    account: Mapped[Account] = relationship(
        back_populates="registrations",
        foreign_keys="SegmentRegistration.account_id",
        lazy="joined",
    )
    segment: Mapped[Segment] = relationship(
        back_populates="registrations",
        foreign_keys="SegmentRegistration.segment_id",
        lazy="joined",
    )
