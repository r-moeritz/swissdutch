import unittest
from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle
from swissdutch.pairing import PairingCard

class Test_DutchPairingEngine(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.addTypeEqualityFunc(PairingCard,
                                 'assertPairingCardsEqual')

    def assertPairingCardsEqual(self, p1, p2, msg=None):
        self.assertTrue(isinstance(p1, PairingCard), 'First argument is not a PairingCard')
        self.assertTrue(isinstance(p2, PairingCard), 'Second argument is not a PairingCard')

        msg = "{0}: first has '{1}', second has '{2}'"
        if p1.surname != p2.surname:
            self.fail(msg.format('surname', p1.surname, p2.surname))
        elif p1.rating != p2.rating:
            self.fail(msg.format('rating', p1.rating, p2.rating))
        elif p1.title != p2.title:
            self.fail(msg.format('title', p1.title, p2.title))
        elif p1.pairing_no != p2.pairing_no:
            self.fail(msg.format('pairing_no', p1.pairing_no, p2.pairing_no))
        elif p1.score != p2.score:
            self.fail(msg.format('score', p1.score, p2.score))
        elif p1.float != p2.float:
            self.fail(msg.format('float', p1.float, p2.float))
        elif p1.opponents != p2.opponents:
            self.fail(msg.format('opponents', p1.opponents, p2.opponents))

    def setUp(self):
        self.maxDiff = None
        self.pairing_cards = [
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
        ]
        self.engine = DutchPairingEngine()

    def test_pair_first_round(self):
        expected_pairing_cards = [
            PairingCard(surname='Carlsen',
                        rating=2900,
                        title=FideTitle.GM,
                        pairing_no=1,
                        opponents=[4]),
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
        for i in range(len(result_pairing_cards)):
            self.assertEqual(result_pairing_cards[i], expected_pairing_cards[i])