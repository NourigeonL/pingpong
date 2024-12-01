from models import Federation, Tournament
from models.entities import Participant, MatchResult
from typing import TypedDict
from pydantic import BaseModel
from enums import Result, Bracket, Stage

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
            
    def register_groupe_stage_result(self, tournament : Tournament, participants : list[str], results : list[list[Result]]) -> None:
        for i in range(len(participants)-1):
            for j in range(len(results[i])):
                tournament.register_match_result(MatchResult(player_a=participants[i], player_b=participants[i+j], stage=Stage.GROUPE, bracket=None, result=results[i][j]))
                
    def register_stage_result(self, tournament : Tournament, stage : Stage, bracket : Bracket, participants : list[str|None], results : list[Result]) -> list[str]:
        qualified_players = []
        for i in range(len(results)):
            if participants[2*i] and participants[2*i+1]:
                tournament.register_match_result(MatchResult(participants[2*i], participants[2*i+1], stage, bracket, results[i]))
            if  results[i] == Result.A_WON:
                qualified_players.append(participants[2*i])
            else:
                qualified_players.append(participants[2*i+1])
        return qualified_players
                
            