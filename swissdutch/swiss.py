import operator
import math
import random
import abc
from copy import copy
from swissdutch.constants import Colour

class SwissPairingEngine(metaclass=abc.ABCMeta):
    @staticmethod
    def _select_random_colour(self):
        return random.choice([Colour.white, Colour.black])

    @abc.abstractclassmethod
    def __init__(self, top_seed_colour_selection_fn=None):
        self._select_top_seed_colour = staticmethod(top_seed_colour_selection_fn \
            if top_seed_colour_selection_fn else self._select_random_colour)

    def _rank_players(self):
        self.pairing_cards.sort(key=operator.attrgetter('surname'))
        self.pairing_cards.sort(key=operator.attrgetter('rating', 'title'),
                                reverse=True)

    def _assign_pairing_numbers(self):
        for i in range(len(self.pairing_cards)):
            p = self.pairing_cards[i]
            p.pairing_no = i + 1

    def _pair_first_round(self):
        self._rank_players()
        self._assign_pairing_numbers()

        k                       = math.floor(len(self.pairing_cards)/2)
        s1                      = self.pairing_cards[:k]
        s2                      = self.pairing_cards[k:]
        odd_colour              = self._select_top_seed_colour()
        even_colour             = Colour.white if odd_colour == Colour.black else Colour.black

        while s1:
            p1       = s1.pop(0)
            p2       = s2.pop(0)
            odd,even = (p1,p2) if p1.pairing_no % 2 else (p2,p1)
            odd.pair(even.pairing_no, odd_colour)
            even.pair(odd.pairing_no, even_colour)

        if s2:
            s2[0].bye()

        return self.pairing_cards

    @abc.abstractmethod
    def _pair_round(self):
        pass

    def pair_round(self, round_no, pairing_cards):
        self.round_no      = round_no
        self.pairing_cards = copy(pairing_cards)

        return self._pair_first_round() \
            if self.round_no == 1 \
            else self._pair_round()



