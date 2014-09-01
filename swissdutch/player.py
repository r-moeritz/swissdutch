from swissdutch.constants import FloatStatus, Colour, ColourPref

class Player:
    def __init__(self, name, rating, title=None, pairing_no=None,
                 score=0, float_status=FloatStatus.none, opponents=(),
                 colour_hist=()):
        self._name         = name
        self._rating       = rating
        self._title        = title
        self._pairing_no   = pairing_no
        self._score        = score
        self._float_status = float_status
        self._opponents    = opponents
        self._colour_hist  = colour_hist

    def __eq__(self, other):
        return (self._name == other.name
                and self._rating == other.rating
                and self._title == other.title
                and self._pairing_no == other.pairing_no
                and self._score == other.score
                and self._float_status == other.float_status
                and self._opponents == other.opponents
                and self._colour_hist == other.colour_hist
                if isinstance(other, Player) else NotImplemented)

    def __repr__(self):
        return ('sn:{0}, r:{1}, t:{2}, pn:{3}, s:{4}, f:{5}, op:{6}, ch:{7}'
            .format(self._name, self._rating, self._title, self._pairing_no,
                    self._score, self._float_status, self._opponents, self._colour_hist))

    def __hash__(self):
        return hash(repr(self))

    @property
    def name(self):
        return self._name

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

    @property
    def colour_preference(self):
        cd  = sum(self._colour_hist)
        cd2 = sum([c for c in self._colour_hist if c != Colour.none][-2:])
        cp  = max(cd, cd2)
        return ColourPref(cp)

    @property
    def expected_colour(self):
        col  = Colour.none
        pref = self.colour_preference

        if pref > 0:
            col = Colour.black
        elif pref < 0:
            col = Colour.white
        else:
            last_col = next((c for c in reversed(self._colour_hist)
                             if c != Colour.none), Colour.none)
            if last_col == Colour.white:
                col = Colour.black
            elif last_col == Colour.black:
                col = Colour.white

        return col

    def pair_both(self, opponent, colour):
        opp_col = Colour.black if colour == Colour.white else Colour.white
        self.pair(opponent, colour)
        opponent.pair(self, opp_col)

    def pair(self, opponent, colour):
        self._opponents += (opponent.pairing_no,)
        self._colour_hist += (colour,)

        float_stat = FloatStatus.none

        if opponent.score > self._score:
            float_stat = FloatStatus.up
        elif opponent.score < self._score:
            float_stat = FloatStatus.down

        self._set_float_status(float_stat)

    def bye(self, bye_value):
        self._opponents += (0,)
        self._colour_hist += (Colour.none,)
        self._float_status = FloatStatus.down
        self._score += bye_value

    def _set_float_status(self, float_status):
        if float_status != FloatStatus.none:
            self._float_status = float_status
            return

        if self._float_status < 0:
            self._float_status += 1
        elif self._float_status > 0:
            self._float_status -= 1