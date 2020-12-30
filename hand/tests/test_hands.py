from unittest import TestCase
from hand.hands import Hand, HoleCards, Community
from deck.cards import Card, Suit, Face

class TestHand(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.community = Community(cards=['JS','4C','AS','10D','6D'])
        cls.hole_cards = HoleCards(cards=['AD', '3S'])

    def test_init_hand(self):
        self.assertEqual(len(self.community.cards), 5)

    def test_has_card(self):
        self.assertTrue(self.community.has_card(Card(suit=Suit.Spades, face=Face.Jack)))
        self.assertFalse(self.community.has_card(Card(suit=Suit.Diamonds, face=Face.King)))

    def test_equal_to(self):
        self.assertTrue(self.community.equal_to(Hand(cards=['JS','4C','AS','10D','6D'])))
        self.assertFalse(self.community.equal_to(Hand(cards=['JS','4C','AS','10D','3D'])))

    def test_high_card(self):
        self.assertEqual(14, self.hole_cards.high_card(self.community))
        hc = HoleCards(cards=['4C','8H'])
        comm = Community(cards = ['2D', '10H', '7C'])
        self.assertEqual(10, hc.high_card(comm))
        
    def test_strongest_five_by_face(self):
        self.assertTrue(Hand(cards=['AD', 'AS', 'JS', '10D', '6D']).equal_to(self.hole_cards.strongest_five_by_face(self.community)))
        self.assertFalse(Hand(cards=['AD', 'AS', 'JS', '10D', '3S']).equal_to(self.hole_cards.strongest_five_by_face(self.community)))