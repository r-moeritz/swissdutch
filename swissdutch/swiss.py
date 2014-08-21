import operator
import math
import random
import abc
from copy import copy
from swissdutch.constants import Colour

class SwissPairingEngine(metaclass=abc.ABCMeta):
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

        k      = math.floor(len(self.pairing_cards)/2)
        s1     = self.pairing_cards[:k]
        s2     = self.pairing_cards[k:]
        w_even = random.randint(0, 1)

        while s1:
            p1       = s1.pop(0)
            p2       = s2.pop(0)
            odd,even = (p1,p2) if p1.pairing_no % 2 else (p2,p1)
            even.pair(odd.pairing_no, Colour.white if w_even else Colour.black)
            odd.pair(even.pairing_no, Colour.black if w_even else Colour.white)

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



