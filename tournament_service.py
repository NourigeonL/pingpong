from models import Federation, Tournament
from models.entities import Participant
from typing import TypedDict
from pydantic import BaseModel

class ParticipantForm(BaseModel):
    id : str
    rank : int
    
class ClubForm(BaseModel):
    id : str
    player_list : list[ParticipantForm]

class TournamentService:
    
    def __init__(self, federation : Federation) -> None:
        self.federation = federation
        
    def register_players_to_tournament(self, tournament : Tournament, participants : list[ClubForm]) -> None:
        self.federation.register_many_clubs(set([p.id for p in participants]))
        for club in participants:
            self.federation.register_many_players([p.id for p in club.player_list])
            tournament.register_many_participants([Participant(player.id, club.id, player.rank) for player in club.player_list])