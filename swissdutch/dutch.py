import math
from swissdutch.swiss import SwissPairingEngine
import itertools
import operator

class DutchPairingEngine(SwissPairingEngine):
    def __init__(self, top_seed_colour_selection_fn=None, bye_value=1):
        super().__init__(top_seed_colour_selection_fn, bye_value)

    def _pair_round(self):
        self._create_score_brackets()

    def _create_score_brackets(self):
        self.pairing_cards.sort(key=operator.attrgetter('pairing_no'))
        self.pairing_cards.sort(key=operator.attrgetter('score'), reverse=True)

        self._score_brackets = []
        for __, g in itertools.groupby(self.pairing_cards, key=operator.attrgetter('score')):
            self._score_brackets.append(list(g))