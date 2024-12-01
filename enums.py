from enum import Enum

class Result(int, Enum):
    A_WON = 1
    A_LOSE = -1
    CANCELED = 0

class Stage(int, Enum):
    GROUPE = 0
    ROUND_OF_64 = 64
    ROUND_OF_32 = 32
    ROUND_OF_16 = 16
    QUARTER_FINAL = 8
    SEMI_FINAL = 4
    FINAL = 2
    
class Bracket(str, Enum):
    WINNER = "winner"
    LOSER = "loser"



        
        
        

        
        