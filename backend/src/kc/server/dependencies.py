from __future__ import annotations

from litestar import Request
from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler

from kc.contrib.litestar import *
from kc.server.services import *
from kc.server.auth import decode_token, Claims, get_claims_from_cookies
from kc.server.exceptions import *
from kc.server import get_session, get_settings


def get_dependencies() -> dict[str, Provide]:
    return {
        "account_service": Provide(provide_account_service),
        "participant_service": Provide(provide_participant_service),
        "organizer_service": Provide(provide_organizer_service),
        "speaker_service": Provide(provide_speaker_service),
        "event_service": Provide(provide_event_service),
        "event_registration_service": Provide(provide_event_registration_service),
        "segment_service": Provide(provide_segment_service),
        "segment_registration_service": Provide(provide_segment_registration_service),
        "claims": Provide(provide_claims),
        "account": Provide(provide_account),
        "organizer": Provide(provide_organizer),
        "speaker": Provide(provide_speaker),
        "participant": Provide(provide_participant),
        "admin_organizer": Provide(provide_admin_organizer),
        "hr_organizer": Provide(provide_hr_organizer),
        "legal_organizer": Provide(provide_legal_organizer),
    }


provide_account_service = create_service_provider(AccountService)
provide_participant_service = create_service_provider(ParticipantService)
provide_organizer_service = create_service_provider(OrganizerService)
provide_speaker_service = create_service_provider(SpeakerService)
provide_event_service = create_service_provider(EventService)
provide_event_registration_service = create_service_provider(EventRegistrationService)
provide_segment_service = create_service_provider(SegmentService)
provide_segment_registration_service = create_service_provider(SegmentRegistrationService)


async def provide_claims(
    request: Request,
) -> Claims | None:
    return get_claims_from_cookies(request.cookies)


async def provide_account(
    account_service: AccountService,
    claims: Claims,
) -> Account:
    db_obj = await account_service.get_one_or_none(id=claims.sub)

    if not db_obj:
        raise AccountNotFoundError()
    
    return db_obj


async def provide_organizer(
    organizer_service: OrganizerService,
    account: Account,
) -> Organizer:
    db_obj = await organizer_service.get_one_or_none(account_id=account.id)

    if not db_obj:
        raise AccountNotFoundError()
    
    return db_obj


async def provide_speaker(
    speaker_service: SpeakerService,
    account: Account,
) -> Speaker:
    db_obj = await speaker_service.get_one_or_none(account_id=account.id)

    if not db_obj:
        raise AccountNotFoundError()
    
    return db_obj


async def provide_participant(
    participant_service: ParticipantService,
    account: Account,
) -> Participant:
    db_obj = await participant_service.get_one_or_none(account_id=account.id)

    if not db_obj:
        raise AccountNotFoundError()
    
    return db_obj


async def provide_admin_organizer(organizer: Organizer) -> Organizer:
    if not organizer.is_admin:
        raise ForbiddenError()
    
    return organizer


async def provide_hr_organizer(organizer: Organizer) -> Organizer:
    if not organizer.is_hr:
        raise ForbiddenError()
    
    return organizer


async def provide_legal_organizer(organizer: Organizer) -> Organizer:
    if not organizer.is_legal:
        raise ForbiddenError()
    
    return organizer
