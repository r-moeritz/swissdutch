import operator
import math
import random
import abc
import copy
from swissdutch.constants import Colour

class SwissPairingEngine(metaclass=abc.ABCMeta):
    @staticmethod
    def _select_random_colour():
        return random.choice((Colour.white, Colour.black))

    @abc.abstractclassmethod
    def __init__(self, top_seed_colour_selection_fn, bye_value):
        self._bye_value = bye_value
        self._select_top_seed_colour = staticmethod(top_seed_colour_selection_fn
                                                    if top_seed_colour_selection_fn 
                                                    else self._select_random_colour)

    @abc.abstractmethod
    def _pair_round(self):
        pass

    def _rank_players(self):
        self._players.sort(key=operator.attrgetter('name'))
        self._players.sort(key=operator.attrgetter('rating', 'title'),
                           reverse=True)

    def _assign_pairing_numbers(self):
        for i in range(len(self._players)):
            p = self._players[i]
            p.pairing_no = i + 1

    def _pair_first_round(self):
        self._rank_players()
        self._assign_pairing_numbers()

        k          = math.floor(len(self._players)/2)
        s1         = self._players[:k]
        s2         = self._players[k:]
        odd_colour = self._select_top_seed_colour()

        while s1:
            p1       = s1.pop(0)
            p2       = s2.pop(0)
            odd,even = (p1,p2) if p1.pairing_no % 2 else (p2,p1)
            odd.pair_both(even, odd_colour)

        if s2:
            s2[0].bye(self._bye_value)

        return self._players

    def pair_round(self, round_no, players, last_round=False):
        self._round_no   = round_no
        self._players    = [copy.deepcopy(p) for p in players]
        self._last_round = last_round

        return (self._pair_first_round()
                if self._round_no == 1 else self._pair_round())
