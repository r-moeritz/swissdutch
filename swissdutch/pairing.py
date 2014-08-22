from swissdutch.constants import FloatStatus, Colour, ColourPref, BracketType

class PairingCard:
    def __init__(self, surname, rating, title=None, pairing_no=None, 
                 score=0, float_status=FloatStatus.none, opponents=(), colour_hist=()):
        self._surname      = surname
        self._rating       = rating
        self._title        = title
        self._pairing_no   = pairing_no
        self._score        = score
        self._float_status = float_status
        self._opponents    = opponents
        self._colour_hist  = colour_hist

    def __eq__(self, other):
        return (self.surname == other.surname 
            and self.rating == other.rating
            and self.title == other.title
            and self.pairing_no == other.pairing_no
            and self.score == other.score
            and self.float_status == other.float_status
            and self.opponents == other.opponents
            and self.colour_hist == other.colour_hist
            if isinstance(other, PairingCard) else NotImplemented)

    def __repr__(self):
        return ('sn:{0}, r:{1}, t:{2}, pn:{3}, s:{4}, f:{5}, op:{6}, ch:{7}'
            .format(self._surname, self._rating, self._title, self._pairing_no,
                    self._score, self._float_status, self._opponents, self._colour_hist))

    @property
    def surname(self):
        return self._surname

    @property
    def rating(self):
        return self._rating

    @property
    def title(self):
        return self._title

    @property
    def pairing_no(self):
        return self._pairing_no

    @pairing_no.setter
    def pairing_no(self, n):
        self._pairing_no = n

    @property
    def score(self):
        return self._score

    @property
    def float_status(self):
        return self._float_status

    @property
    def colour_hist(self):
        return self._colour_hist

    @property
    def opponents(self):
        return self._opponents

    def pair(self, opponent, colour, float_status=FloatStatus.none):
        self._opponents += (opponent,)
        self._colour_hist += (colour,)
        self._set_float_status(float_status)

    def bye(self, bye_value):
        self._opponents += (0,)
        self._colour_hist += (Colour.none,)
        self._float_status = FloatStatus.down
        self._score += bye_value

    def colour_preference(self):
        diff = sum(self._colour_hist)
        return ColourPreference(diff)

    def _set_float_status(self, float_status):
        if float_status != FloatStatus.none:
            self._float_status = float_status
            return

        if self._float_status < 0:
            self._float_status += 1
        elif self._float_status > 0:
            self._float_status -= 1

class ScoreBracket:
    def __init__(self, pairing_cards):
        self._pairing_cards = list(pairing_cards)

    def type(self):
        scores = []
        for __, g in itertools.groupby(self._pairing_cards, key=operator.attrgetter('score')):
            scores.append(g)
        return (BracketType.Homogenous
                if len(scores) < 2 or len(scores) - len(scores[-1]) > len(scores[-1])
                else BracketType.Heteregenous)
