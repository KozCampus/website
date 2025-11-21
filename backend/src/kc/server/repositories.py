from __future__ import annotations

from kc.contrib.litestar import SQLAlchemyAsyncRepository
from kc.models import *


class AccountRepository(SQLAlchemyAsyncRepository[Account]):
    model_type = Account


class ParticipantRepository(SQLAlchemyAsyncRepository[Participant]):
    model_type = Participant


class OrganizerRepository(SQLAlchemyAsyncRepository[Organizer]):
    model_type = Organizer


class SpeakerRepository(SQLAlchemyAsyncRepository[Speaker]):
    model_type = Speaker


class EventRepository(SQLAlchemyAsyncRepository[Event]):
    model_type = Event


class EventRegistrationRepository(SQLAlchemyAsyncRepository[EventRegistration]):
    model_type = EventRegistration


class SegmentRepository(SQLAlchemyAsyncRepository[Segment]):
    model_type = Segment


class SegmentRegistrationRepository(SQLAlchemyAsyncRepository[SegmentRegistration]):
    model_type = SegmentRegistration
