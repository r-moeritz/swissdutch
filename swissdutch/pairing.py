from swissdutch.constants import FloatStatus, Colour
from copy import copy

class PairingCard:
    def __init__(self, surname, rating, title=None, pairing_no=None, 
                 score=0, float_status=FloatStatus.none, opponents=None, colour_hist=None):
        self.surname      = surname
        self.rating       = rating
        self.title        = title
        self.pairing_no   = pairing_no
        self.score        = score
        self.float_status = float_status
        self.opponents    = copy(opponents) if opponents else []
        self.colour_hist  = copy(colour_hist) if opponents else []

    def __eq__(self, other):
        return (self.surname == other.surname \
            and self.rating == other.rating \
            and self.title == other.title \
            and self.pairing_no == other.pairing_no \
            and self.score == other.score \
            and self.float_status == other.float_status \
            and self.opponents == other.opponents) \
            and self.colour_hist == other.colour_hist \
            if isinstance(other, PairingCard) else NotImplemented

    def __repr__(self):
        return 'sn:{0}, r:{1}, t:{2}, pn:{3}, s:{4}, f:{5}, op:{6}, ch:{7}' \
            .format(self.surname, self.rating, self.title, self.pairing_no,
                    self.score, self.float_status, self.opponents, self.colour_hist)

    def pair(self, opponent, colour, float_status=FloatStatus.none):
        self.opponents.append(opponent)
        self.colour_hist.append(colour)
        self._set_float_status(float_status)

    def bye(self, bye_value):
        self.opponents.append(0)
        self.colour_hist.append(Colour.none)
        self.float_status = FloatStatus.down
        self.score += bye_value

    def _set_float_status(self, float_status):
        if float_status != FloatStatus.none:
            self.float_status = float_status
            return

        if self.float_status < 0:
            self.float_status += 1
        elif self.float_status > 0:
            self.float_status -= 1
