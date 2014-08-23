from enum import Enum, IntEnum

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
    black = -1
    none  =  0,
    white =  1

class FloatStatus(IntEnum):
    down     = -2,
    downPrev = -1,
    none     =  0,
    upPrev   =  1,
    up       =  2

class ColourPref(IntEnum):
    whiteAbs =  2,
    whiteStr =  1,
    mild     =  0,
    blackStr = -1,
    blackAbs = -2
