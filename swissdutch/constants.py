from enum import Enum, IntEnum

class FideTitle(IntEnum):
    WCM = 0x7FFFFFFFFFFFFFF8
    WFM = 0x7FFFFFFFFFFFFFF9
    CM  = 0x7FFFFFFFFFFFFFFA
    WIM = 0x7FFFFFFFFFFFFFFB
    FM  = 0x7FFFFFFFFFFFFFFC
    WGM = 0x7FFFFFFFFFFFFFFD
    IM  = 0x7FFFFFFFFFFFFFFE
    GM  = 0x7FFFFFFFFFFFFFFF

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
    whiteAbs = -2,
    whiteStr = -1,
    mild     =  0,
    blackStr =  1,
    blackAbs =  2