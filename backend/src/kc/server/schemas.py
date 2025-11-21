from __future__ import annotations

from kc.contrib.msgspec import *


class ClientLogin(Struct):
    email: str
    password: str


class TOTPSchema(Struct):
    secret: str
    uri: str
    qr_code: str


class AccountSchema(Struct):
    id: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    email: str | None
    phone: str | None
    birth_date: date | None
    is_email_verified: bool


class AccountCreate(Struct):
    name: str
    email: str | None
    phone: str | None
    birth_date: date | None
    password: str | None


class ParticipantSchema(Struct):
    id: UUID
    created_at: datetime
    updated_at: datetime
    account: AccountSchema
    country: str
    postal_code: str
    city: str
    address_line1: str
    address_line2: str | None
    is_student: bool
    school_name: str | None


class ClientParticipantCreate(Struct):
    country: str
    postal_code: str
    city: str
    address_line1: str
    address_line2: str | None
    is_student: bool
    school_name: str | None


class OrganizerSchema(Struct):
    id: UUID
    created_at: datetime
    updated_at: datetime
    account: AccountSchema
    is_admin: bool
    is_hr: bool
    is_legal: bool
    finance_and_law_interest: bool
    venue_coordination_interest: bool
    it_interest: bool
    program_organization_interest: bool
    partner_relations_interest: bool
    media_and_marketing_interest: bool
    hr_interest: bool


class ClientOrganizerCreate(Struct):
    finance_and_law_interest: bool
    venue_coordination_interest: bool
    it_interest: bool
    program_organization_interest: bool
    partner_relations_interest: bool
    media_and_marketing_interest: bool
    hr_interest: bool


class OrganizerCreate(ClientOrganizerCreate):
    account_id: UUID
    is_admin: bool
    is_hr: bool
    is_legal: bool


class SpeakerSchema(Struct):
    id: UUID
    created_at: datetime
    updated_at: datetime
    account: AccountSchema
    introduction: str


class SpeakerCreate(Struct):
    account_id: UUID
    introduction: str
