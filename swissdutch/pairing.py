import math
import itertools
import operator
from copy import copy
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

class ScoreBracket:
    def __init__(self, score, players):
        self._score                   = score
        self._all_players             = list(players)
        self._remaining_players       = None
        self._criteria                = PairingCriteria(self)
        self._pairings                = []
        self._bye                     = None
        self._transpositions          = None
        self._exchanges               = None
        self._exchange_length         = 1
        self._saved_transpositions    = None
        self._incompatible_player     = None
        self._paired_floaters         = False

    @property
    def all_players(self):
        return self._all_players

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
    def odd_round(self):
        return self._context.round_no % 2

    @property
    def last_round(self):
        return self._context.last_round

    @property
    def round_no(self):
        return self._context.round_no

    def generate_pairings(self, ctx):
        self._context = ctx
        step = self._c1()
        while step:
            step = step()

    def finalize_pairings(self):
        for pair in self._pairings:
            self._assign_colours(pair)

        if self._bye:
            p = self._bye
            p.bye(self._context.bye_value)

    def add_player(self, player):
        self._all_players.append(player)

    def remove_player(self, player):
        self._all_players.remove(player)

    def can_backtrack(self, player):
        return player != self._incompatible_player

    def backtrack(self, player):
        self._reset()
        self._all_players.append(player)

    @property
    def _lsb(self):
        return self._context.lowest_score_bracket

    @property
    def _players(self):
        return self._remaining_players if self._remaining_players else self._all_players

    @property
    def _heterogenous(self):
        return (any(p.score > self._score for p in self._players)
                and sum(p.score > self._score for p in self._players) / len(self._players) < 0.5)

    @property
    def _majority_expected_colour(self):
        white = sum(p.expected_colour == Colour.white for p in self._players)
        black = sum(p.expected_colour == Colour.black for p in self._players)
        
        col = Colour.none
        
        if white > black:
            col = Colour.white
        elif black > white:
            col = Colour.black

        return col

    @property
    def _p0(self):
        return math.floor(len(self._players)/2)

    @property
    def _m0(self):
        return sum(p.score > self._score for p in self._players)
    
    def _reset(self):
        self._remaining_players       = None
        self._pairings                = []
        self._bye                     = None
        self._exchanges               = None
        self._exchange_length         = 1
        self._incompatible_player     = None

    def _calculate_x1(self):
        white   = sum(p.expected_colour == Colour.white for p in self._players)
        black   = sum(p.expected_colour == Colour.black for p in self._players)
        neither = len(self._players) - white - black

        if white < black:
            white += neither
        else:
            black += neither

        return math.floor(abs((white - black) / 2))

    def _calculate_z1(self):
        if self.odd_round:
            return self._x1 # only calculate z1 in even rounds

        maj_col = self._majority_expected_colour
        num_var = sum(p.colour_preference == ColourPref.mild 
                      and p.expected_colour == maj_col 
                      for p in self._players)
        return self._x1 - num_var

    def _assign_colours(self, pair):
        p1, p2 = pair
        if abs(p1.colour_preference) > abs(p2.colour_preference):
            p1.pair_both(p2, p1.expected_colour)
        elif abs(p1.colour_preference) < abs(p2.colour_preference):
            p2.pair_both(p1, p2.expected_colour)
        elif p1.score > p2.score:
            p1.pair_both(p2, p1.expected_colour)
        elif p1.score < p2.score:
            p2.pair_both(p1, p2.expected_colour)
        elif p1.pairing_no < p2.pairing_no:
            p1.pair_both(p2, p1.expected_colour)
        else:
            p2.pair_both(p1, p2.expected_colour)

    def _c1(self):
        step = self._c2a

        for p1 in self._players:
            compatible = False

            other_players = copy(self._players)
            other_players.remove(p1)

            for p2 in other_players:
                if self._criteria.b1a(p1, p2) and self._criteria.b2(p1, p2):
                    compatible = True
                    break

            if not compatible:
                player = p1
                if len(other_players) == 1:
                    player = p1 if p1.score >= p2.score else p2
                self._incompatible_player = player

                if player.score > self._score:
                    step = self._c13 if self._lsb else self._c12
                    break
                elif self._lsb:
                    step = self._c13
                    break
                elif self._context.can_downfloat(player):
                    self._context.downfloat(player)
                    self._incompatible_player = None

        if not len(self._players):
            step = None

        return step

    def _c2a(self):
        self._p1 = self._p0
        self._m1 = self._m0
        return self._c2b

    def _c2b(self):
        self._x1 = self._calculate_x1()
        self._z1 = self._calculate_z1()
        return self._c3a

    def _c3a(self):
        self._p = self._m1 if self._heterogenous else self._p1
        return self._c3b

    def _c3b(self):
        self._criteria.b2_enabled_for_top_scorers = True
        return self._c3c

    def _c3c(self):
        self._criteria.a7d_enabled = True
        return self._c3d

    def _c3d(self):
        self._x = self._x1
        self._z = self._z1
        return self._c3e

    def _c3e(self):
        self._criteria.b5_enabled_for_downfloaters = True
        return self._c3f

    def _c3f(self):
        self._criteria.b6_enabled_for_downfloaters = True
        return self._c3g

    def _c3g(self):
        self._criteria.b5_enabled_for_upfloaters = True
        return self._c3h

    def _c3h(self):
        self._criteria.b6_enabled_for_upfloaters = True
        return self._c4

    def _c4(self):
        self._players.sort(key=operator.attrgetter('pairing_no'))
        self._players.sort(key=operator.attrgetter('score'), reverse=True)

        self._s1 = self._players[:self._p]
        self._s2 = self._players[self._p:]

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
        bye         = unpaired[0] if len(unpaired) == 1 and self._lsb else None
        downfloater = unpaired[0] if not(bye) and len(unpaired) == 1 else None

        step = None
        if self._criteria.satisfied(pairings, downfloater, bye):
            if downfloater:
                if self._context.can_downfloat(downfloater):
                    self._pairings += pairings
                    self._context.downfloat(downfloater)
                else:
                    possible_floaters = sum(self._criteria.b5(p) 
                                            and self._criteria.b6(p) 
                                            and self._context.can_downfloat(p)
                                            for p in self._players)
                    if possible_floaters:
                        step = self._c7 # try to find a different floater
                    else:
                        # Force this floater down anyway & let the next score
                        # bracket deal with it.
                        self._context.downfloat(downfloater)
            else:
                self._pairings += pairings
                self._bye       = bye

                if len(unpaired) > 1:
                    # Pair homogenous remainder
                    self._paired_floaters      = True
                    self._saved_transpositions = self._transpositions
                    self._transpositions       = None
                    self._exchanges            = None
                    self._remaining_players    = unpaired
                    self._p                    = self._p1 - self._m1
                    self._x                    = self._x1
                    step                       = self._c4
        else:
            step = self._c7

        return step

    def _c7(self):
        if not self._transpositions:
            self._transpositions = itertools.permutations(self._s2)
            next(self._transpositions) # skip 1st one since it's equal to self._s2

        step = self._c6

        try:
            self._s2 = list(next(self._transpositions))
        except StopIteration: # no more transpositions
            self._transpositions = None
            step = self._c10a if self._heterogenous else self._c8

        return step

    @staticmethod
    def _generate_exchanges(s1, s2, n):
        s1_subsets = sorted(itertools.combinations(s1, r=n),
                            key=lambda players: sum(p.pairing_no for p in players),
                            reverse=True)
        s1_subsets.sort(key=lambda players: sum(p.score for p in players), 
                        reverse=True)
        s2_subsets = sorted(itertools.combinations(s2, r=n),
                            key=lambda players: sum(p.pairing_no for p in players))
        s2_subsets.sort(key=lambda players: sum(p.score for p in players))
        end_s1_subsets = len(s1_subsets) - 1
        end_s2_subsets = len(s2_subsets) - 1

        diff = lambda s1sub, s2sub: abs(sum(p.score for p in s1sub) - sum(p.score for p in s2sub))
        min_diff = diff(s1_subsets[0], s2_subsets[0])
        max_diff = diff(s1_subsets[-1], s2_subsets[-1])

        delta = min_diff
        i = 0
        k = 0
        exchanges = []

        while delta <= max_diff:
            if delta == diff(s1_subsets[i], s2_subsets[k]):
                exchanges.append( (s1_subsets[i], s2_subsets[k]) )
            if k < end_s2_subsets:
                k += 1
                continue
            if i < end_s1_subsets:
                i += 1
                k = 0
                continue
            delta += 1
            i = 0
            k = 0

        return exchanges

    def _c8(self):
        step    = self._c5

        if self._exchanges == None:
            self._s1.sort(key=operator.attrgetter('pairing_no'), reverse=True)
            self._s1.sort(key=operator.attrgetter('score'))

            self._s2.sort(key=operator.attrgetter('pairing_no'))
            self._s2.sort(key=operator.attrgetter('score'), reverse=True)

            self._exchanges = self._generate_exchanges(self._s1, self._s2,
                                                       self._exchange_length)
        
        exchange = None

        try:
            exchange = self._exchanges.pop(0)
        except IndexError: # no more exchanges (for this subset size)
            self._exchanges = None
            self._exchange_length += 1

            if self._exchange_length > self._p:
                # We've exhausted all possible exchanges
                self._exchange_length = 1
                self._remaining_players = None
                step = self._c9 if self._heterogenous else self._c10a
            else:
                step = self._c8 # generate another set of exchanges
        else:
            s1_subset, s2_subset = exchange
            for player in s1_subset:
                self._s1.remove(player)
                self._s2.append(player)
            for player in s2_subset:
                self._s2.remove(player)
                self._s1.append(player)

        return step

    def _c9(self):
        self._pairings          = []
        self._transpositions    = self._saved_transpositions
        self._s1                = self._players[:self._p]
        self._s2                = self._players[self._p:]
        self._p                 = self._p1
        self._x                 = self._x1
        return self._c7

    def _c10a(self):
        step = self._c4
        if not self._criteria.b6_enabled_for_upfloaters:
            step = self._c10b
        self._criteria.b6_enabled_for_upfloaters = False
        return step

    def _c10b(self):
        step = self._c3h
        if not self._criteria.b5_enabled_for_upfloaters:
            step = self._c10c
        self._criteria.b5_enabled_for_upfloaters = False
        return step

    def _c10c(self):
        step = self._c3g
        if not self._criteria.b6_enabled_for_downfloaters:
            step = self._c10d
        self._criteria.b6_enabled_for_downfloaters = False
        return step

    def _c10d(self):
        step = self._c3f
        if not self._criteria.b5_enabled_for_downfloaters:
            step = self._c10e
        self._criteria.b5_enabled_for_downfloaters = False
        return step

    def _c10e(self):
        if self.odd_round:
            if self._x < self._p1:
                self._x += 1
        else:
            if self._z < self._x:
                self._z += 1
            elif self._z == self._x and self._x < self._p1:
                self._x += 1
                self._z = self._z1
        return self._c3e

    def _c10f(self):
        if self.odd_round:
            self._criteria.a7d_enabled = False
        return self._c3d

    def _c10g(self):
        if self.last_round:
            self._criteria.b2_enabled_for_top_scorers = False
        return self._c3c

    def _c12(self):
        step = None
        
        player = self._incompatible_player
        if self._context.can_backtrack(player):
            self._context.backtrack(player)
            self._incompatible_player = None
        elif self._heterogenous:
            step = self._c14b
        else:
            step = self._c14a

        return step

    def _c13(self):
        step = None

        if self._heterogenous:
            step = self._c14b
        else:
            player = self._incompatible_player
            if self._context.can_backtrack(player):
                self._context.backtrack(player)
                self._incompatible_player = None
            else:
                self._context.collapse_previous_score_bracket()
                self._incompatible_player = None
                step = self._c1

        return step

    def _c14a(self):
        step = self._c3a

        if self._p1 == 0:
            self._context.collapse_current_score_bracket()
            step = None
        else:
            self._p1 -= 1
            self._x1 -= 1 if self._x1 > 0 else 0
            self._z1 -= 1 if not self.odd_round and self._z1 > 0 else 0

        return step

    def _c14b(self):
        step = self._c3a

        if self._paired_floaters and not self._lsb:
            self._p1 -= 1
            self._x1 -= 1 if self._x1 > 0 else 0
            self._z1 -= 1 if not self.odd_round and self._z1 > 0 else 0
        else:
            if self._m1 > 1:
                self._m1 -= 1
                step = self._c3a
            elif self._m1 == 1:
                self._m1 = 0
                self._p1 = self._p0
                step = self._c2b

        return step

class PairingCriteria:
    def __init__(self, score_bracket):
        self._score_bracket              = score_bracket
        self.b5_enabled_for_downfloaters = True
        self.b5_enabled_for_upfloaters   = True
        self.b6_enabled_for_downfloaters = True
        self.b6_enabled_for_upfloaters   = True
        self.a7d_enabled                 = True
        self.b2_enabled_for_top_scorers  = True

    def b1a(self, p1, p2):
        """p1 and p2 may not be paired if they have met before."""
        return p2.pairing_no not in p1.opponents

    def b1b(self, player):
        """player may not receive a bye if they received a bye in the previous round."""
        return player.opponents[-1]

    def b2(self, p1, p2):
        """p1 and p2 are incompatible if they have the same absolute colour preference."""
        abs_value = 1 if self._score_bracket.odd_round and self.a7d_enabled else 2
        p1_abs    = abs(p1.colour_preference) >= abs_value
        p2_abs    = abs(p2.colour_preference) >= abs_value

        half_max_score = self._score_bracket.round_no/2
        return (not(p1_abs) or not(p2_abs) or p1.colour_preference != p2.colour_preference
                or (self._score_bracket.last_round and not(self.b2_enabled_for_top_scorers)
                    and (p1.score > half_max_score or p2.score > half_max_score)))

    def b4(self, pairings):
        """The current pairings are acceptable if they satisfy the minimum number
        of colour preferences."""
        violated  = sum(p1.expected_colour == p2.expected_colour for (p1,p2) in pairings)
        return violated <= self._score_bracket.x

    def b5(self, p1, p2=None):
        """No player shall receive an identical float in two consecutive rounds."""
        t1 = (p1.float_status != FloatStatus.down
              if not(p2) and self.b5_enabled_for_downfloaters else True)
        t2 = ((p1.score == p2.score
              or (p1.score < p2.score
                  and p1.float_status != FloatStatus.up)
              or (p1.score > p2.score
                  and p2.float_status != FloatStatus.up))
              if p2 and self.b5_enabled_for_upfloaters else True)
        return t1 and t2

    def b6(self, p1, p2=None):
        """No player shall receive an identical float as two rounds before."""
        t1 = (p1.float_status != FloatStatus.downPrev
              if not(p2) and self.b6_enabled_for_downfloaters else True)
        t2 = ((p1.score == p2.score
              or (p1.score < p2.score
                  and p1.float_status != FloatStatus.upPrev)
              or (p1.score > p2.score
                  and p2.float_status != FloatStatus.upPrev))
              if p2 and self.b6_enabled_for_upfloaters else True)
        return t1 and t2

    def satisfied(self, pairings, downfloater, bye):
        t1 = all(self.b1a(p1, p2) and self.b2(p1, p2) and self.b5(p1, p2) 
                 and self.b6(p1, p2) for (p1, p2) in pairings)
        t2 = self.b4(pairings) if pairings else True
        t3 = self.b5(downfloater) and self.b6(downfloater) if downfloater else True
        t4 = self.b1b(bye) if bye else True
        return t1 and t2 and t3 and t4

class PairingContext:
    def __init__(self, round_no, last_round, bye_value, score_brackets):
        self._ix             = 0
        self._round_no       = round_no
        self._last_round     = last_round
        self._bye_value      = bye_value
        self._score_brackets = score_brackets
        self._downfloaters   = []
        self._backtrackers   = []

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

    def collapse_current_score_bracket(self):
        for p in self._current_score_bracket.all_players:
            self._next_score_bracket.add_player(p)
        self._score_brackets.remove(self._current_score_bracket)
        self._ix -= 1

    def collapse_previous_score_bracket(self):
        for p in self._previous_score_bracket.all_players:
            self._current_score_bracket.add_player(p)
        self._score_brackets.remove(self._previous_score_bracket)
        self._ix -= 1

    def can_downfloat(self, player):
        return (player not in self._downfloaters
                and not self.lowest_score_bracket)

    def downfloat(self, player):
        self._downfloaters.append(player)
        self._current_score_bracket.remove_player(player)
        self._next_score_bracket.add_player(player)

    def can_backtrack(self, player):
        return (player not in self._backtrackers
                and self._index != 0
                and self._previous_score_bracket.can_backtrack(player))

    def backtrack(self, player):
        self._backtrackers.append(player)
        self._current_score_bracket.remove_player(player)
        self._previous_score_bracket.backtrack(player)
        self._ix -= 2

    def finalize_pairings(self):
        for sb in self._score_brackets:
            sb.finalize_pairings()

    @property
    def _current_score_bracket(self):
        return self._score_brackets[self._index]

    @property 
    def _previous_score_bracket(self):
        return self._score_brackets[self._index-1] 

    @property
    def _next_score_bracket(self):
        return self._score_brackets[self._index+1]

    @property
    def _index(self):
        return self._ix - 1 if self._ix else self._ix
