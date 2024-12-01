from uuid import uuid4
from enum import Enum
from datetime import date
from eventsourcing.aggregates import AggregateRoot
from eventsourcing.event import IEvent
from dataclasses import dataclass
from multipledispatch import dispatch


@dataclass
class ClubRegistered(IEvent):
    id: str
    name : str
    
    @property
    def type(self) -> str:
        return "ClubRegistered"

@dataclass
class FederationCreated(IEvent):
    id: str
    
    @property
    def type(self) -> str:
        return "FederationCreated"

@dataclass
class PlayerRegistered(IEvent):
    id: str
    name : str
    
    @property
    def type(self) -> str:
        return "PlayerRegistered"


class Federation(AggregateRoot):
    __id : str
    def __init__(self, id: str | None = None) -> None:
        super().__init__()
        if id:
            self._apply_change(FederationCreated(id))
        self.clubs : list[str] = []
        self.players : list[str] = []
    
    
    def register_club(self, club_name : str) -> None:
        if club_name not in self.clubs:
            self._apply_change(ClubRegistered(club_name, club_name))
            
    def register_many_clubs(self, clubs_list : list[str]) -> None:
        for club in clubs_list:
            self.register_club(club)
            
    def register_player(self, player_name : str) -> None:
        if player_name not in self.players:
            self._apply_change(PlayerRegistered(player_name, player_name))
            
    def register_many_players(self, players_list : list[str]) -> None:
        for player in players_list:
            self.register_player(player)
    
    @property
    def id(self) -> str:
        return self.__id
    
    @dispatch(FederationCreated)
    def _apply(self, e: FederationCreated) -> None:
        self.__id = e.id
        
    @dispatch(ClubRegistered)
    def _apply(self, e: ClubRegistered) -> None:
        self.clubs.append(e.name)
        
    @dispatch(PlayerRegistered)
    def _apply(self, e: PlayerRegistered) -> None:
        self.players.append(e.name)
        
    @staticmethod
    def to_stream_id(id : str) -> str:
        return f"federation-{id}"