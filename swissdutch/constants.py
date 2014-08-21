from enum import IntEnum

class FideTitle(IntEnum):
    WCM = 0
    WFM = 1
    CM  = 2
    WIM = 3
    FM  = 4
    WGM = 5
    IM  = 6
    GM  = 7

class Colour(IntEnum):
    none  = 0,
    white = 1,
    black = 2