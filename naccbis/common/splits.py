from enum import Enum


class Split(Enum):
    OVERALL = "overall"
    CONFERENCE = "conference"

    def __str__(self):
        return self.value


class GameLogSplit(Enum):
    HITTING = "hitting"
    PITCHING = "pitching"
    FIELDING = "fielding"

    def __str__(self):
        return self.value
