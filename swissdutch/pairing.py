import copy

class PairingCard:
    def __init__(self, surname, rating, title=None, pairing_no=None, 
                 score=0, float=0, opponents=[], colour_hist=[]):
        self.surname     = surname
        self.rating      = rating
        self.title       = title
        self.pairing_no  = pairing_no
        self.score       = score
        self.float       = float
        self.opponents   = copy.copy(opponents)
        self.colour_hist = copy.copy(colour_hist)

    def __eq__(self, other):
        return self.surname == other.surname \
            and self.rating == other.rating \
            and self.title == other.title \
            and self.pairing_no == other.pairing_no \
            and self.score == other.score \
            and self.float == other.float \
            and self.opponents == other.opponents \
            and self.colour_hist == other.colour_hist

    def __repr__(self):
        return '{0} {1} {2} {3} {4} {5} {6} {7}' \
            .format(self.surname, self.rating, self.title,
                    self.pairing_no, self.score, self.float,
                    self.opponents, self.colour_hist)

    def pair(self, opponent, colour, float=None):
        self.opponents.append(opponent)
        self.colour_hist.append(colour)
        # TODO: float

    def bye(self):
        self.opponents.append(0)
        self.colour_hist.append(0)