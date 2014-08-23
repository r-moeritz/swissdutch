import math
import itertools
import operator
from swissdutch.swiss import SwissPairingEngine
from swissdutch.pairing import ScoreBracket, PairingContext

class DutchPairingEngine(SwissPairingEngine):
    def __init__(self, top_seed_colour_selection_fn=None, bye_value=1):
        super().__init__(top_seed_colour_selection_fn, bye_value)

    def _pair_round(self):
        score_brackets = self._create_score_brackets()
        
        ctx = PairingContext(self._round_no, self._last_round, score_brackets)
        for sb in ctx:
            sb.generate_pairings(ctx)

        return list(itertools.chain.from_iterable(sb.finalize_pairings()
                                                  for sb in score_brackets))

    def _create_score_brackets(self):
        self._pairing_cards.sort(key=operator.attrgetter('pairing_no'))
        self._pairing_cards.sort(key=operator.attrgetter('score'), reverse=True)

        return [ScoreBracket(score, pairing_cards)
                for score, pairing_cards in itertools.groupby(self._pairing_cards, 
                                                              key=operator.attrgetter('score'))]