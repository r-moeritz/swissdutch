import unittest
from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle
from swissdutch.pairing import PairingCard

class Test_DutchPairingEngine(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.pairing_cards = [
            PairingCard(surname='Carlsen',
                        rating=2900,
                        title=FideTitle.GM),
            PairingCard(surname='Aronian',
                        rating=2800,
                        title=FideTitle.GM),
            PairingCard(surname='Silman',
                        rating=2400,
                        title=FideTitle.IM),
            PairingCard(surname='Jones',
                        rating=2200,
                        title=FideTitle.WIM),
            PairingCard(surname='Smith',
                        rating=2200,
                        title=FideTitle.CM),
            PairingCard(surname='Adams',
                        rating=1200),
            PairingCard(surname='Bernstein',
                        rating=1200)
        ]
        self.engine = DutchPairingEngine()
        self.addTypeEqualityFunc(PairingCard,
                                 lambda one, two, msg=None: \
                                     self.surname == other.surname \
                                     and self.rating == other.rating \
                                     and self.title == other.title \
                                     and self.pairing_no == other.pairing_no \
                                     and self.score == other.score \
                                     and self.float == other.float \
                                     and self.opponents == other.opponents)

    def test_pair_first_round(self):
        expected_pairing_cards = [
            PairingCard(surname='Carlsen',
                        rating=2900,
                        title=FideTitle.GM,
                        pairing_no=1,
                        opponents=[4]),
            PairingCard(surname='Jones',
                        rating=2200,
                        title=FideTitle.WIM,
                        pairing_no=4,
                        opponents=[1]),
            PairingCard(surname='Smith',
                        rating=2200,
                        title=FideTitle.CM,
                        pairing_no=5,
                        opponents=[2]),
            PairingCard(surname='Aronian',
                        rating=2800,
                        title=FideTitle.GM,
                        pairing_no=2,
                        opponents=[5]),
            PairingCard(surname='Silman',
                        rating=2400,
                        title=FideTitle.IM,
                        pairing_no=3,
                        opponents=[6]),
            PairingCard(surname='Adams',
                        rating=1200,
                        title=None,
                        pairing_no=6,
                        opponents=[3]),
            PairingCard(surname='Bernstein',
                        rating=1200,
                        title=None,
                        pairing_no=7,
                        opponents=[0])
        ]
        
        result_pairing_cards = self.engine.pair_round(1, self.pairing_cards)
        self.assertCountEqual(result_pairing_cards, expected_pairing_cards)