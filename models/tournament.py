from uuid import uuid4
from enum import Enum
from datetime import date
from eventsourcing.aggregates import AggregateRoot
from eventsourcing.event import IEvent
from dataclasses import dataclass
from multipledispatch import dispatch
from models.entities import Participant, MatchResult


@dataclass
class TournamentCreated(IEvent):
    id : str
    name : str
    date : str
    
    @property
    def type(self) -> str:
        return "TournamentCreated"

@dataclass
class ParticipantRegistered(IEvent):
    participant_id : str
    club : str
    rank : int
    
    @property
    def type(self) -> str:
        return "ParticipantRegistered"
    
@dataclass
class MatchFinished(IEvent):
    match_result : MatchResult
    
    @property
    def type(self) -> str:
        return "MatchFinished"


class Tournament(AggregateRoot):
    __id : str
    name : str
    tournament_date : date
    
    def __init__(self, id: str | None = None, name : str | None = None, competition_date : date | None = None) -> None:
        super().__init__()
        if id and name and competition_date:
            self._apply_change(TournamentCreated(id, name, competition_date.isoformat()))
        self.participants : list[Participant] = []
        self.match_history : list[MatchResult] = []
        
    def register_participant(self, participant : Participant) -> None:
        if participant.id not in [p.id for p in self.participants]:
            self._apply_change(ParticipantRegistered(participant.id, participant.club_id, participant.rank))
            
    def register_many_participants(self, participants_list : list[Participant]) -> None:
        for participant in participants_list:
            self.register_participant(participant)
            
    def register_match_result(self, match_result : MatchResult) -> None:
        self._apply_change(MatchFinished(match_result))
        
    @dispatch(TournamentCreated)
    def _apply(self, e: TournamentCreated) -> None:
        self.__id = e.id
        self.tournament_date = date.fromisoformat(e.date)
        self.name = e.name
        
    @dispatch(ParticipantRegistered)
    def _apply(self, e: ParticipantRegistered) -> None:
        self.participants.append(Participant(e.participant_id, e.club, e.rank))
        
    @dispatch(MatchFinished)
    def _apply(self, e: MatchFinished) -> None:
        self.match_history.append(e.match_result)
        
    @property
    def id(self) -> str:
        return self.__id
    
    @staticmethod
    def to_stream_id(id : str) -> str:
        return f"competition-{id}"
    