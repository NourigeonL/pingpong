from dataclasses import dataclass
from enums import Stage, Result, Bracket
@dataclass
class Participant:
    id : str
    club_id : str
    rank : int
    

@dataclass
class MatchResult:
    player_a : str
    player_b : str
    stage : Stage
    bracket : Bracket | None
    result : Result
    