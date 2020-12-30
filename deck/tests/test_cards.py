from unittest import TestCase
from deck.cards import Card, Suit, Face

class TestCard(TestCase):

    def test_card_strength(self):
        card = Card(suit=Suit.Diamonds, face=Face.Five)
        self.assertEqual(5, card.strength())

    def test_card_enum_strength(self):
        card = Card(suit=Suit.Diamonds, face=Face.Queen)
        self.assertEqual(12, card.face.strength())