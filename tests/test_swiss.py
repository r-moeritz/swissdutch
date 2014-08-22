import unittest
from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from swissdutch.pairing import PairingCard

class Test_SwissPairingEngine(unittest.TestCase):
    @staticmethod
    def select_top_seed_colour():
        return Colour.white

    def setUp(self):
        self.maxDiff = None
        self.engine = DutchPairingEngine(self.select_top_seed_colour)

    def test_pair_first_round(self):
        input_pairing_cards = (
            PairingCard(surname='Silman',
                        rating=2400,
                        title=FideTitle.IM),
            PairingCard(surname='Carlsen',
                        rating=2900,
                        title=FideTitle.GM),
            PairingCard(surname='Aronian',
                        rating=2800,
                        title=FideTitle.GM),
            PairingCard(surname='Smith',
                        rating=2200,
                        title=FideTitle.CM),
            PairingCard(surname='Jones',
                        rating=2200,
                        title=FideTitle.WIM),
            PairingCard(surname='Bernstein',
                        rating=1200),
            PairingCard(surname='Adams',
                        rating=1200)
        )
        expected_pairing_cards = [
            PairingCard(surname='Carlsen',
                        rating=2900,
                        title=FideTitle.GM,
                        pairing_no=1,
                        opponents=(4,),
                        colour_hist=(Colour.white,)),
            PairingCard(surname='Aronian',
                        rating=2800,
                        title=FideTitle.GM,
                        pairing_no=2,
                        opponents=(5,),
                        colour_hist=(Colour.black,)),
            PairingCard(surname='Silman',
                        rating=2400,
                        title=FideTitle.IM,
                        pairing_no=3,
                        opponents=(6,),
                        colour_hist=(Colour.white,)),
            PairingCard(surname='Jones',
                        rating=2200,
                        title=FideTitle.WIM,
                        pairing_no=4,
                        opponents=(1,),
                        colour_hist=(Colour.black,)),
            PairingCard(surname='Smith',
                        rating=2200,
                        title=FideTitle.CM,
                        pairing_no=5,
                        opponents=(2,),
                        colour_hist=(Colour.white,)),
            PairingCard(surname='Adams',
                        rating=1200,
                        title=None,
                        pairing_no=6,
                        opponents=(3,),
                        colour_hist=(Colour.black,)),
            PairingCard(surname='Bernstein',
                        rating=1200,
                        title=None,
                        pairing_no=7,
                        score=1,
                        float_status=FloatStatus.down,
                        opponents=(0,),
                        colour_hist=(Colour.none,))
        ]
        
        result_pairing_cards = self.engine.pair_round(1, input_pairing_cards)
        self.assertEqual(result_pairing_cards, expected_pairing_cards)