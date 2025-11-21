from __future__ import annotations

from kc.contrib.litestar import SQLAlchemyAsyncRepositoryService
from kc.models import *
from kc.server.repositories import *


class AccountService(SQLAlchemyAsyncRepositoryService[Account]):
    repository_type = AccountRepository


class ParticipantService(SQLAlchemyAsyncRepositoryService[Participant]):
    repository_type = ParticipantRepository


class OrganizerService(SQLAlchemyAsyncRepositoryService[Organizer]):
    repository_type = OrganizerRepository


class SpeakerService(SQLAlchemyAsyncRepositoryService[Speaker]):
    repository_type = SpeakerRepository


class EventService(SQLAlchemyAsyncRepositoryService[Event]):
    repository_type = EventRepository


class EventRegistrationService(SQLAlchemyAsyncRepositoryService[EventRegistration]):
    repository_type = EventRegistrationRepository


class SegmentService(SQLAlchemyAsyncRepositoryService[Segment]):
    repository_type = SegmentRepository


class SegmentRegistrationService(SQLAlchemyAsyncRepositoryService[SegmentRegistration]):
    repository_type = SegmentRegistrationRepository
