from __future__ import annotations

import typing as t

from litestar import Response
from litestar.middleware.rate_limit import RateLimitConfig

from kc.contrib.litestar import *
from kc.server import get_settings
from kc.server.exceptions import *
from kc.server.schemas import *
from kc.server.services import *
from kc.server.auth import (
    Claims,
    verify_password,
    hash_password,
    create_claims,
    issue_token,
    issue_totp_secret,
    encrypt_totp_secret,
)


def get_routes() -> list[ControllerRouterHandler]:
    return [
        AuthController,
        AccountController,
        ParticipantController,
        OrganizerController,
        SpeakerController,
        EventController,
        SegmentController,
    ]


auth_minute_rate_limit = RateLimitConfig(("minute", 60))
auth_daily_rate_limit = RateLimitConfig(("day", 600))


def set_auth_cookie(
    response: Response,
    token: str,
) -> None:
    settings = get_settings()
    _400_DAYS = 400 * 24 * 60 * 60

    if settings.api.debug:
        response.set_cookie(
            key="Auth",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=_400_DAYS,
        )
    else:
        response.set_cookie(
            key="__Secure-Auth",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=_400_DAYS,
        )


class AuthController(Controller):
    path = "/auth"
    tags = ["Auth"]
    middleware = [
        auth_minute_rate_limit.middleware,
        auth_daily_rate_limit.middleware,
    ]


    @post(
        operation_id="LoginClient",
        path="/login",
    )
    async def login_client(
        self,
        data: ClientLogin,
        account_service: AccountService,
    ) -> Response:
        account = await account_service.get_one_or_none(email=data.email)
        if account is None:
            raise AccountNotFoundError()
        
        if account.password_hash is None:
            raise NoPasswordSetError()

        if not verify_password(
            plain=data.password, 
            hashed=account.password_hash,
        ):
            raise InvalidPasswordError()
        
        claims = create_claims(account_id=account.id)

        token = issue_token(claims)
        
        response = Response(content=None, status_code=204)
        set_auth_cookie(response, token)

        return response


    @get(
        operation_id="GetClientClaims",
        path="/claims",
    )
    async def get_client_claims(
        self,
        claims: Claims | None,
    ) -> Claims | None:
        return claims
    

    @post(
        operation_id="SetupClientTOTP",
        path="/setup-totp",
    )
    async def setup_client_totp(
        self,
        account: Account,
        account_service: AccountService,
    ) -> TOTPSchema:
        schema = issue_totp_secret(account.name)
        try:
            encrypted_secret = encrypt_totp_secret(schema.secret)
            await account_service.update(
                item_id=account.id,
                data={"encrypted_totp_secret": encrypted_secret},
            )
        except:
            import traceback
            traceback.print_exc()
        return schema


class AccountController(Controller):
    path = "/accounts"
    tags = ["Accounts"]


    # TODO: remove
    @get(
        operation_id="ListAccounts",
        path="",
        cache=60,
    )
    async def list_accounts(
        self,
        account_service: AccountService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
        admin_organizer: Organizer,
    ) -> OffsetPagination[AccountSchema]:
        results, total = await account_service.list_and_count(*filters)
        return account_service.to_schema(
            data=results,
            total=total,
            schema_type=AccountSchema,
            filters=filters,
        )
    

    @get(
        operation_id="GetAccount",
        path="/{account_id:uuid}",
    )
    async def get_account(
        self,
        account_id: UUID,
        account_service: AccountService,
        admin_organizer: Organizer,
    ) -> AccountSchema:
        db_obj = await account_service.get(account_id)
        return account_service.to_schema(
            data=db_obj,
            schema_type=AccountSchema,
        )
    

    @get(
        operation_id="GetClientAccount",
        path="/me",
    )
    async def get_client_account(
        self,
        account: Account,
        account_service: AccountService,
    ) -> AccountSchema:
        return account_service.to_schema(
            data=account,
            schema_type=AccountSchema,
        )


    @post(
        operation_id="CreateAccount",
        path="",
        rate_limit=RateLimitConfig(("hour", 10)),
    )
    async def create_account(
        self,
        data: AccountCreate,
        account_service: AccountService,
    ) -> AccountSchema:
        if await account_service.get_one_or_none(email=data.email):
            raise ConflictError()
        
        if data.password is not None:
            password_hash = hash_password(data.password)
        else:
            password_hash = None

        account = await account_service.create(data={
            "name": data.name,
            "email": data.email,
            "phone": data.phone,
            "birth_date": data.birth_date,
            "password_hash": password_hash,
        })

        return account_service.to_schema(
            data=account,
            schema_type=AccountSchema,
        )
    

    @delete(
        operation_id="DeleteAccount",
        path="/{account_id:uuid}",
    )
    async def delete_account(
        self,
        account_id: UUID,
        account_service: AccountService,
        admin_organizer: Organizer,
    ) -> None:
        await account_service.delete(account_id)


class ParticipantController(Controller):
    path = "/participants"
    tags = ["Participants"]


    @get(
        operation_id="ListParticipants",
        path="",
    )
    async def list_participants(
        self,
        participant_service: ParticipantService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
        admin_organizer: Organizer,
    ) -> OffsetPagination[ParticipantSchema]:
        results, total = await participant_service.list_and_count(*filters)
        return participant_service.to_schema(
            data=results,
            total=total,
            schema_type=ParticipantSchema,
            filters=filters,
        )
    

    @get(
        operation_id="GetParticipant",
        path="/{participant_id:uuid}",
    )
    async def get_participant(
        self,
        participant_id: UUID,
        participant_service: ParticipantService,
        admin_organizer: Organizer,
    ) -> ParticipantSchema:
        db_obj = await participant_service.get(participant_id)
        return participant_service.to_schema(
            data=db_obj,
            schema_type=ParticipantSchema,
        )


    @get(
        operation_id="GetClientParticipant",
        path="/me",
    )
    async def get_client_participant(
        self,
        participant: Participant,
        participant_service: ParticipantService,
    ) -> ParticipantSchema:
        return participant_service.to_schema(
            data=participant,
            schema_type=ParticipantSchema,
        )
    

    @post(
        operation_id="CreateClientParticipant",
        path="/me",
    )
    async def create_client_participant(
        self,
        data: ClientParticipantCreate,
        participant_service: ParticipantService,
        account: Account,
    ) -> ParticipantSchema:
        if await participant_service.get_one_or_none(account_id=account.id):
            raise ConflictError()
        
        participant = await participant_service.create(data={
            "account_id": account.id,
            "country": data.country,
            "postal_code": data.postal_code,
            "city": data.city,
            "address_line1": data.address_line1,
            "address_line2": data.address_line2,
            "is_student": data.is_student,
            "school_name": data.school_name,
        })

        return participant_service.to_schema(
            data=participant,
            schema_type=ParticipantSchema,
        )
    

    @delete(
        operation_id="DeleteParticipant",
        path="/{participant_id:uuid}",
    )
    async def delete_participant(
        self,
        participant_id: UUID,
        participant_service: ParticipantService,
        admin_organizer: Organizer,
    ) -> None:
        await participant_service.delete(participant_id)


    @get(
        operation_id="GetClientParticipantRegistrations",
        path="/me/registrations",
    )
    async def get_client_participant_registrations(
        self,
        participant: Participant,
        event_registration_service: EventRegistrationService,
        segment_registration_service: SegmentRegistrationService,
    ) -> RegistrationsSchema:
        event_registrations = await event_registration_service.list(
            participant_id=participant.id,
        )
        events = [ _.event for _ in event_registrations ]

        segment_registrations = await segment_registration_service.list(
            participant_id=participant.id,
        )
        segments = [ _.segment for _ in segment_registrations ]

        return event_registration_service.to_schema(
            data={
                "events": events,
                "segments": segments,
            },
            schema_type=RegistrationsSchema,
        )


class OrganizerController(Controller):
    path = "/organizers"
    tags = ["Organizers"]


    @get(
        operation_id="ListOrganizers",
        path="",
    )
    async def list_organizers(
        self,
        organizer_service: OrganizerService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
        admin_organizer: Organizer,
    ) -> OffsetPagination[OrganizerSchema]:
        results, total = await organizer_service.list_and_count(*filters)
        return organizer_service.to_schema(
            data=results,
            total=total,
            schema_type=OrganizerSchema,
            filters=filters,
        )
    

    @get(
        operation_id="GetOrganizer",
        path="/{organizer_id:uuid}",
    )
    async def get_organizer(
        self,
        organizer_id: UUID,
        organizer_service: OrganizerService,
        admin_organizer: Organizer,
    ) -> OrganizerSchema:
        db_obj = await organizer_service.get(organizer_id)
        return organizer_service.to_schema(
            data=db_obj,
            schema_type=OrganizerSchema,
        )
    

    @post(
        operation_id="CreateOrganizer",
        path="",
    )
    async def create_organizer(
        self,
        data: OrganizerCreate,
        organizer_service: OrganizerService,
        admin_organizer: Organizer,
    ) -> OrganizerSchema:
        if await organizer_service.get_one_or_none(account_id=data.account_id):
            raise ConflictError()

        organizer = await organizer_service.create(data=data)

        return organizer_service.to_schema(
            data=organizer,
            schema_type=OrganizerSchema,
        )
    

    @get(
        operation_id="GetClientOrganizer",
        path="/me",
    )
    async def get_client_organizer(
        self,
        organizer: Organizer,
        organizer_service: OrganizerService,
    ) -> OrganizerSchema:
        return organizer_service.to_schema(
            data=organizer,
            schema_type=OrganizerSchema,
        )
    

    @post(
        operation_id="CreateClientOrganizer",
        path="/me",
    )
    async def create_client_organizer(
        self,
        data: ClientOrganizerCreate,
        organizer_service: OrganizerService,
        account: Account,
    ) -> OrganizerSchema:
        if await organizer_service.get_one_or_none(account_id=account.id):
            raise ConflictError()
        
        organizer = await organizer_service.create(data={
            "account_id": account.id,
            "finance_and_law_interest": data.finance_and_law_interest,
            "venue_coordination_interest": data.venue_coordination_interest,
            "it_interest": data.it_interest,
            "program_organization_interest": data.program_organization_interest,
            "partner_relations_interest": data.partner_relations_interest,
            "media_and_marketing_interest": data.media_and_marketing_interest,
            "hr_interest": data.hr_interest,
        })

        return organizer_service.to_schema(
            data=organizer,
            schema_type=OrganizerSchema,
        )


    @delete(
        operation_id="DeleteOrganizer",
        path="/{organizer_id:uuid}",
    )
    async def delete_organizer(
        self,
        organizer_id: UUID,
        organizer_service: OrganizerService,
        admin_organizer: Organizer,
    ) -> None:
        await organizer_service.delete(organizer_id)


class SpeakerController(Controller):
    path = "/speakers"
    tags = ["Speakers"]


    @get(
        operation_id="ListSpeakers",
        path="",
    )
    async def list_speakers(
        self,
        speaker_service: SpeakerService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
        admin_organizer: Organizer,
    ) -> OffsetPagination[SpeakerSchema]:
        results, total = await speaker_service.list_and_count(*filters)
        return speaker_service.to_schema(
            data=results,
            total=total,
            schema_type=SpeakerSchema,
            filters=filters,
        )
    

    @get(
        operation_id="GetSpeaker",
        path="/{speaker_id:uuid}",
    )
    async def get_speaker(
        self,
        speaker_id: UUID,
        speaker_service: SpeakerService,
        admin_organizer: Organizer,
    ) -> SpeakerSchema:
        db_obj = await speaker_service.get(speaker_id)
        return speaker_service.to_schema(
            data=db_obj,
            schema_type=SpeakerSchema,
        )
    

    @get(
        operation_id="GetClientSpeaker",
        path="/me",
    )
    async def get_client_speaker(
        self,
        speaker: Speaker,
        speaker_service: SpeakerService,
    ) -> SpeakerSchema:
        return speaker_service.to_schema(
            data=speaker,
            schema_type=SpeakerSchema,
        )
    

    @post(
        operation_id="CreateSpeaker",
        path="",
    )
    async def create_speaker(
        self,
        data: SpeakerCreate,
        speaker_service: SpeakerService,
        admin_organizer: Organizer,
    ) -> SpeakerSchema:
        if await speaker_service.get_one_or_none(account_id=data.account_id):
            raise ConflictError()

        speaker = await speaker_service.create(data=data)

        return speaker_service.to_schema(
            data=speaker,
            schema_type=SpeakerSchema,
        )
    

    @delete(
        operation_id="DeleteSpeaker",
        path="/{speaker_id:uuid}",
    )
    async def delete_speaker(
        self,
        speaker_id: UUID,
        speaker_service: SpeakerService,
        admin_organizer: Organizer,
    ) -> None:
        await speaker_service.delete(speaker_id)


class EventController(Controller):
    path = "/events"
    tags = ["Events"]


    @get(
        operation_id="ListEvents",
        path="",
    )
    async def list_events(
        self,
        event_service: EventService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
    ) -> OffsetPagination[EventSchema]:
        results, total = await event_service.list_and_count(*filters)
        return event_service.to_schema(
            data=results,
            total=total,
            schema_type=EventSchema,
            filters=filters,
        )


    @get(
        operation_id="GetEvent",
        path="/{event_id:uuid}",
    )
    async def get_event(
        self,
        event_id: UUID,
        event_service: EventService,
    ) -> EventSchema:
        db_obj = await event_service.get(event_id)
        return event_service.to_schema(
            data=db_obj,
            schema_type=EventSchema,
        )
    

    @post(
        operation_id="CreateEvent",
        path="",
    )
    async def create_event(
        self,
        data: EventCreate,
        event_service: EventService,
        admin_organizer: Organizer,
    ) -> EventSchema:
        event = await event_service.create(data=data)
        return event_service.to_schema(
            data=event,
            schema_type=EventSchema,
        )
    

    @delete(
        operation_id="DeleteEvent",
        path="/{event_id:uuid}",
    )
    async def delete_event(
        self,
        event_id: UUID,
        event_service: EventService,
        admin_organizer: Organizer,
    ) -> None:
        await event_service.delete(event_id)


    @get(
        operation_id="ListEventSegments",
        path="/{event_id:uuid}/segments",
    )
    async def list_event_segments(
        self,
        event_id: UUID,
        segment_service: SegmentService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ],
    ) -> OffsetPagination[SegmentSchema]:
        results, total = await segment_service.list_and_count(
            event_id=event_id,
            *filters,
        )
        return segment_service.to_schema(
            data=results,
            total=total,
            schema_type=SegmentSchema,
            filters=filters,
        )
    

    @post(
        operation_id="CreateClientEventRegistration",
        path="/{event_id:uuid}/register",
    )
    async def create_client_event_registration(
        self,
        event_id: UUID,
        event_registration_service: EventRegistrationService,
        participant: Participant,
    ) -> EventSchema:
        event_registration = await event_registration_service.create(
            data={
                "event_id": event_id,
                "participant_id": participant.id,
            },
        )
        return event_registration_service.to_schema(
            data=event_registration.event,
            schema_type=EventSchema,
        )


class SegmentController(Controller):
    path = "/segments"
    tags = ["Segments"]


    @get(
        operation_id="GetSegment",
        path="/{segment_id:uuid}",
    )
    async def get_segment(
        self,
        segment_id: UUID,
        segment_service: SegmentService,
    ) -> SegmentSchema:
        db_obj = await segment_service.get(segment_id)
        return segment_service.to_schema(
            data=db_obj,
            schema_type=SegmentSchema,
        )
    

    @post(
        operation_id="CreateClientSegmentRegistration",
        path="/{segment_id:uuid}/register",
    )
    async def create_client_segment_registration(
        self,
        segment_id: UUID,
        segment_registration_service: SegmentRegistrationService,
        participant: Participant,
    ) -> SegmentSchema:
        segment_registration = await segment_registration_service.create(
            data={
                "segment_id": segment_id,
                "participant_id": participant.id,
            },
        )
        return segment_registration_service.to_schema(
            data=segment_registration.segment,
            schema_type=SegmentSchema,
        )


    @post(
        operation_id="CreateEventSegment",
        path="",
    )
    async def create_segment(
        self,
        data: SegmentCreate,
        segment_service: SegmentService,
        admin_organizer: Organizer,
    ) -> SegmentSchema:
        segment = await segment_service.create(data=data)
        return segment_service.to_schema(
            data=segment,
            schema_type=SegmentSchema,
        )
