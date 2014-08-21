from swissdutch.swiss import SwissPairingEngine

class DutchPairingEngine(SwissPairingEngine):
    def __init__(self, top_seed_colour_selection_fn=None):
        super().__init__(top_seed_colour_selection_fn)

    def _pair_round(self):
        pass