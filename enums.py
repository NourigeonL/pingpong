from enum import Enum

class Result(Enum):
    A_WON = 1
    A_LOSE = -1
    CANCELED = 0

class Stage(Enum):
    GROUPE = "groupe"
    ROUND_OF_64 = "64"
    ROUND_OF_32 = "32"
    ROUND_OF_16 = "16"
    QUARTER_FINAL = "quarter"
    SEMI_FINAL = "semi"
    FINAL = "final"
    
class Bracket(Enum):
    WINNER = "winner"
    LOSER = "loser"



        
        
        

        
        