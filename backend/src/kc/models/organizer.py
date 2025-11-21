from __future__ import annotations

import typing as t

from kc.contrib.sqlalchemy import *

if t.TYPE_CHECKING:
    from kc.models.account import Account


class Organizer(UUIDAuditBase):
    __tablename__ = "organizer"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("account.id", ondelete="cascade"),
        unique=True,
    )
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_hr: Mapped[bool] = mapped_column(default=False)
    is_legal: Mapped[bool] = mapped_column(default=False)

    finance_and_law_interest: Mapped[bool] = mapped_column()
    venue_coordination_interest: Mapped[bool] = mapped_column()
    it_interest: Mapped[bool] = mapped_column()
    program_organization_interest: Mapped[bool] = mapped_column()
    partner_relations_interest: Mapped[bool] = mapped_column()
    media_and_marketing_interest: Mapped[bool] = mapped_column()
    hr_interest: Mapped[bool] = mapped_column()

    account: Mapped[Account] = relationship(
        foreign_keys="Organizer.account_id",
        lazy="joined",
        cascade="all, delete",
    )
