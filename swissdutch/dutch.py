import operator
import itertools
from swissdutch.swiss import SwissPairingEngine
from swissdutch.pairing import ScoreBracket, PairingContext

class DutchPairingEngine(SwissPairingEngine):
    def __init__(self, top_seed_colour_selection_fn=None, bye_value=1):
        super().__init__(top_seed_colour_selection_fn, bye_value)

    def _pair_round(self):
        score_brackets = self._create_score_brackets()
        ctx            = PairingContext(self._round_no, self._last_round,
                                        self._bye_value, score_brackets)
        for sb in ctx:
            sb.generate_pairings(ctx)

        ctx.finalize_pairings()

        return self._players

    def _create_score_brackets(self):
        self._players.sort(key=operator.attrgetter('pairing_no'))
        self._players.sort(key=operator.attrgetter('score'), reverse=True)

        return [ScoreBracket(score, players)
                for score, players 
                in itertools.groupby(self._players,
                                     key=operator.attrgetter('score'))]
