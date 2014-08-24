import math
import itertools
import operator
from copy import copy
from swissdutch.constants import FloatStatus, Colour, ColourPref

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

    def __hash__(self):
        return hash(repr(self))

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

    @property
    def colour_preference(self):
        diff = sum(self._colour_hist)
        return ColourPref(diff)

    @property
    def expected_colour(self):
        col  = Colour.none
        pref = self.colour_preference

        if pref > 0:
            col = Colour.white
        elif pref < 0:
            col = Colour.black
        else:
            last_col = next((c for c in self._colour_hist 
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

class ScoreBracket:
    def __init__(self, score, pairing_cards):
        self._score         = score
        self._pairing_cards = list(pairing_cards)
        self._criteria      = PairingCriteria(self)
        self._pairings      = []
        self._unpaired      = None
        self._bye           = None

    @property
    def x(self):
        return self._x

    @property
    def p(self):
        return self._p

    @property
    def z(self):
        return self._z

    @property
    def pairing_cards(self):
        return self._pairing_cards

    def generate_pairings(self, ctx):
        self._context = ctx
        step = self._c1()
        while step:
            step = step()

    def finalize_pairings(self):
        pairing_cards = []

        if self._pairings or self._bye:
            for pair in self._pairings:
                self._assign_colours(pair)
            pairing_cards += pair

            if self._bye:
                p = self._bye
                p.bye(self._context.bye_value)
                pairing_cards.append(p)
        
        return pairing_cards   

    @property
    def _heterogenous(self):
        num_players = len(self._pairing_cards)
        return num_players-self._m0 < num_players/2

    @property
    def _majority_expected_colour(self):
        pairing_cards = self._unpaired if self._unpaired else self._pairing_cards
        white         = sum(p.expected_colour == Colour.white for p in pairing_cards)
        black         = sum(p.expected_colour == Colour.black for p in pairing_cards)
        
        col = Colour.none
        
        if white > black:
            col = white
        elif black > white:
            col = black

        return col

    @property
    def _p0(self):
        return math.floor(len(self._pairing_cards)/2)

    @property
    def _x1(self):
        pairing_cards = self._unpaired if self._unpaired else self._pairing_cards
        white         = sum(p.expected_colour == Colour.white for p in pairing_cards)
        black         = sum(p.expected_colour == Colour.black for p in pairing_cards)
        neither       = len(pairing_cards) - white - black

        if white < black:
            white += neither
        else:
            black += neither

        return math.floor(abs((white - black) / 2))

    @property
    def _m0(self):
        return sum(p.score > self._score for p in self._pairing_cards)

    @property
    def _z1(self):
        if self._context.round_no % 2:
            return x1 # only calculate z1 in even rounds

        maj_col = self._majority_expected_colour
        num_var = sum(p.colour_preference == ColourPref.mild 
                      and p.expected_colour == maj_col 
                      for p in self._pairing_cards)
        return self._x1 - num_var

    def _assign_colours(self, pair):
        p1, p2 = pair
        if (abs(p1.colour_preference) > abs(p2.colour_preference)):
            p1.pair_both(p2, p1.expected_colour)
        elif (abs(p1.colour_preference) < abs(p2.colour_preference)):
            p2.pair_both(p1, p2.expected_colour)
        elif (p1.score > p2.score):
            p1.pair_both(p2, p1.expected_colour)
        elif (p1.score < p2.score):
            p2.pair_both(p1, p2.expected_colour)
        elif (p1.pairing_no < p2.pairing_no):
            p1.pair_both(p2, p1.expected_colour)
        else:
            p2.pair_both(p1, p2.expected_colour)

    def _c1(self):
        pairing_cards = copy(self._pairing_cards)
        p1 = pairing_cards.pop()

        while p1:
            compatible = False

            for p2 in pairing_cards:
                if self._criteria.b1a(p1, p2) and self._criteria.b2(p1, p2):
                    compatible = True
                    break

            if not compatible:
                # TODO: if player moved down from higher score bracket: apply C12
                # TODO: elif this score bracket is LSB: apply C13
                # else:
                self._context.downfloat(p1)

            p1 = pairing_cards.pop() if len(pairing_cards) else None

        return self._c2 if len(self._pairing_cards) else None

    def _c2(self):
        self._p1 = self._p0
        self._m1 = self._m0
        return self._c3

    def _c3(self):
        self._p = self._m1 if self._heterogenous else self._p1
        self._x = self._x1
        self._z = self._z1
        return self._c4

    def _c4(self):
        if self._unpaired:
            self._s1       = self._unpaired[:self._p]
            self._s2       = self._unpaired[self._p:]
            self._unpaired = None # ensure we don't get here again
        else:
            # Sort again in case we received downfloaters
            self._pairing_cards.sort(key=operator.attrgetter('pairing_no'))
            self._pairing_cards.sort(key=operator.attrgetter('score'), reverse=True)

            self._s1 = self._pairing_cards[:self._p]
            self._s2 = self._pairing_cards[self._p:]

        return self._c5

    def _c5(self):
        self._s1.sort(key=operator.attrgetter('pairing_no'))
        self._s1.sort(key=operator.attrgetter('score'), reverse=True)

        self._s2.sort(key=operator.attrgetter('pairing_no'))
        self._s2.sort(key=operator.attrgetter('score'), reverse=True)

        return self._c6

    def _c6(self):
        pairings    = [(self._s1[i], self._s2[i]) for i in range(len(self._s1))]
        unpaired    = list(set(self._s1 + self._s2) - set(sum(pairings, ())))
        bye         = unpaired[0] if len(unpaired) == 1 and self._context.lowest_score_bracket else None
        downfloater = unpaired[0] if not(bye) and len(unpaired) == 1 else None

        step = None
        if self._criteria.satisfied(pairings, downfloater, bye):
            if downfloater:
                self._context.downfloat(downfloater)

            self._pairings += pairings
            self._bye       = bye

            if len(unpaired) > 1:
                # Pair homogenous remainder (players left unpaired after pairing downfloaters)
                self._unpaired = unpaired
                self._p        = self._p1 - self._m1
                self._x        = self._x1 # recalculate x based on homogenous remainder
                return self._c4
        else:
            step = self._c7
        return step

    def _c7(self):
        if not hasattr(self, '_s2_permutations'):
            self._s2_permutations = itertools.permutations(self._s2)
            next(self._s2_permutations) # skip 1st permutation since it's equal to self._s2

        try:
            self._s2 = list(next(self._s2_permutations))
        except StopIteration:
            pass # TODO: No more permutations, where to now?
        else:
            return self._c6 # try again

class PairingCriteria:
    def __init__(self, score_bracket):
        self._score_bracket = score_bracket

    def b1a(self, p1, p2):
        """p1 and p2 may not be paired if they have met before."""
        return p2.pairing_no not in p1.opponents

    def b1b(self, p):
        """p may not receive a bye if they received a bye in the previous round."""
        return p1.opponents[-1]

    def b2(self, p1, p2):
        """p1 and p2 are incompatible if they have the same absolute colour preference."""
        return (abs(p1.colour_preference) != 2 
                or abs(p2.colour_preference) != 2
                or p1.colour_preference != p2.colour_preference)

    def b4(self, pairings):
        """The current pairings are acceptable if they satisfy the minimum number
        of colour preferences."""
        white,black = zip(*pairings)
        satisfied  = sum(p.expected_colour == Colour.white for p in white)
        satisfied += sum(p.expected_colour == Colour.black for p in black)
        return satisfied >= self._score_bracket.x

    def b5(self, p1, p2=None):
        """No player shall receive an identical float in two consecutive rounds."""
        return ((not(p2) and p1.float_status != FloatStatus.down)
                or p2 and (p1.score == p2.score 
                           or (p1.score > p2.score 
                               and (p1.float_status != FloatStatus.down 
                                    and p2.float_status != FloatStatus.up))
                           or (p1.score < p2.score 
                               and (p1.float_status != FloatStatus.up 
                                    and p2.float_status != FloatStatus.down))))

    def b6(self, p1, p2=None):
        """No player shall receive an identical float as two rounds before."""
        return ((not(p2) and p1.float_status != FloatStatus.downPrev)
                or p2 and (p1.score == p2.score
                           or (p1.score > p2.score 
                               and (p1.float_status != FloatStatus.downPrev 
                                    and p2.float_status != FloatStatus.upPrev)) 
                           or (p1.score < p2.score 
                               and (p1.float_status != FloatStatus.upPrev 
                                    and p2.float_status != FloatStatus.downPrev))))

    def satisfied(self, pairings, downfloater, bye):
        t1 = all(self.b1a(p1, p2) and self.b2(p1, p2) and self.b5(p1, p2) 
                 and self.b6(p1, p2) for (p1, p2) in pairings)
        t2 = self.b4(pairings)
        t3 = self.b5(downfloater) and self.b6(downfloater) if downfloater else True
        t4 = self.b1b(bye) if bye else True
        return t1 and t2 and t3 and t4

class PairingContext:
    def __init__(self, round_no, last_round, bye_value, score_brackets):
        self._round_no       = round_no
        self._last_round     = last_round
        self._bye_value      = bye_value
        self._score_brackets = score_brackets
        self._ix             = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            result = self._score_brackets[self._ix]
            self._ix += 1
            return result
        except IndexError:
            raise StopIteration

    @property
    def round_no(self):
        return self._round_no

    @property
    def last_round(self):
        return self._last_round

    @property
    def bye_value(self):
        return self._bye_value

    @property
    def lowest_score_bracket(self):
        return self._index == len(self._score_brackets) - 1

    def downfloat(self, pairing_card):
        curr_bracket = self._score_brackets[self._index]
        next_bracket = self._score_brackets[self._index + 1]

        curr_bracket.pairing_cards.remove(pairing_card)
        next_bracket.pairing_cards.append(pairing_card)

    @property
    def _index(self):
        return self._ix - 1 if self._ix else self._ix