import math
import itertools
import operator
from swissdutch.swiss import SwissPairingEngine
from swissdutch.pairing import ScoreBracket

class DutchPairingEngine(SwissPairingEngine):
    def __init__(self, top_seed_colour_selection_fn=None, bye_value=1):
        super().__init__(top_seed_colour_selection_fn, bye_value)

    def _pair_round(self):
        self._create_score_brackets()
        for i in range(len(self._score_brackets)):
            _c1(i)
            _c2(i)

    def _create_score_brackets(self):
        self._pairing_cards.sort(key=operator.attrgetter('pairing_no'))
        self._pairing_cards.sort(key=operator.attrgetter('score'), reverse=True)

        self._score_brackets = []
        for k, g in itertools.groupby(self._pairing_cards, key=operator.attrgetter('score')):
            self._score_brackets.append(ScoreBracket(k, g))

    def _c1(self, sb_index):
        # TODO
        # 1. Does this bracket contain players who can't play against any of the others because either
        # a) they have already met
        # b) they have the same absolute colour preference
        pass

    def _c2(self, sb_index):
        # TODO
        pass 
