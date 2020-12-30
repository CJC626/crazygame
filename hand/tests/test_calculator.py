from unittest import TestCase
from hand.calculator import has_straight, has_flush, has_x_of_a_kind, has_full_house, has_two_pair, has_straight_flush
from hand.hands import Community, HoleCards, Hand
from deck.cards import Face

class TestCalculator(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pair_hc = HoleCards(cards=['6C', '9S'])
        cls.pair_comm = Community(cards=['6S', '10D', '4H', 'QS', '5D'])

    def test_straight(self):
        low_ace_straight = Hand(cards=['3C','5H','AS','10H','4C','7C','2H'])
        high_ace_straight =  Hand(cards=['QC','5H','AD','10H','KD','7C','JH'])
        mid_straight =  Hand(cards=['3C','5H','9S','QH','6C','7C','8H'])
        no_straight_four =  Hand(cards=['5C','9H','JS','10H','4C','7C','6H'])
        no_straight_four_ace =  Hand(cards=['3C','9H','AS','10H','4C','7C','2H'])
        no_straight_three =  Hand(cards=['3C','KH','QS','9H','8C','7C','2H'])
        straight_six =  Hand(cards=['3C','5H','8S','10H','4C','7C','6H'])
        no_straight_dups = Hand(cards=['3C','5H','KS','10H','3S','7C','6H'])
        straight_dups = Hand(cards=['3C','5H','6S','7H','4C','7C','6H'])

        self.assertEqual(5, len(has_straight(low_ace_straight.cards)))
        self.assertEqual(5, len(has_straight(high_ace_straight.cards)))
        self.assertEqual(5, len(has_straight(mid_straight.cards)))
        self.assertEqual(6, len(has_straight(straight_six.cards)))
        self.assertEqual(5, len(has_straight(straight_dups.cards)))
        self.assertIsNone(has_straight(no_straight_four.cards))
        self.assertIsNone(has_straight(no_straight_four_ace.cards))
        self.assertIsNone(has_straight(no_straight_three.cards))
        self.assertIsNone(has_straight(no_straight_dups.cards))

    def test_has_flush(self):
        flush = Hand(cards=['3C','5C','10C','7C','9C','7S','6H'])
        no_flush = Hand(cards=['3S','5H','6S','10D','2C','AS','6S'])
        flush_six = Hand(cards=['3C','5C','9C','7H','JC','KC','10C'])

        self.assertEqual(5, len(has_flush(flush.cards)))
        self.assertIsNone(has_flush(no_flush.cards))
        self.assertEqual(6, len(has_flush(flush_six.cards)))

    def test_four_of_a_kind(self):
        four_of_a_kind_holecards = HoleCards(cards=['AH', '10D'])
        four_of_a_kind_community = Community(cards=['AD', 'AS', 'AC', '7S', '3D'])
        four_of_a_kind = has_x_of_a_kind(four_of_a_kind_community.cards + four_of_a_kind_holecards.cards)
        self.assertEqual(4, four_of_a_kind[0])
        self.assertEqual(14, four_of_a_kind[1])
        self.assertEqual(5, len(four_of_a_kind[2]))
        self.assertEqual(Face.Ten, four_of_a_kind[2][-1].face)
        self.assertEqual(Face.Ace, four_of_a_kind[2][-2].face)
        self.assertEqual(Face.Ace, four_of_a_kind[2][0].face)

        four_of_a_kind_holecards = HoleCards(cards=['7H', '7D'])
        four_of_a_kind_community = Community(cards=['QD', '7S', 'JC', '7C', '3D'])
        four_of_a_kind = has_x_of_a_kind(four_of_a_kind_community.cards + four_of_a_kind_holecards.cards)
        self.assertEqual(4, four_of_a_kind[0])
        self.assertEqual(7, four_of_a_kind[1])
        self.assertEqual(5, len(four_of_a_kind[2]))
        self.assertEqual(Face.Queen, four_of_a_kind[2][0].face)
        self.assertEqual(Face.Seven, four_of_a_kind[2][1].face)
        self.assertEqual(Face.Seven, four_of_a_kind[2][-1].face)

    def test_three_of_a_kind(self):
        three_of_a_kind_holecards = HoleCards(cards=['AH', '10D'])
        three_of_a_kind_community = Community(cards=['AD', '9S', 'AC', '7S', '3D'])
        three_of_a_kind = has_x_of_a_kind(three_of_a_kind_community.cards + three_of_a_kind_holecards.cards)
        self.assertEqual(3, three_of_a_kind[0])
        self.assertEqual(14, three_of_a_kind[1])
        self.assertEqual(5, len(three_of_a_kind[2]))
        self.assertEqual(Face.Nine, three_of_a_kind[2][-1].face)
        self.assertEqual(Face.Ten, three_of_a_kind[2][-2].face)
        self.assertEqual(Face.Ace, three_of_a_kind[2][0].face)

        three_of_a_kind_holecards = HoleCards(cards=['7H', '7D'])
        three_of_a_kind_community = Community(cards=['QD', '4S', 'JC', '7C', '3D'])
        three_of_a_kind = has_x_of_a_kind(three_of_a_kind_community.cards + three_of_a_kind_holecards.cards)
        self.assertEqual(3, three_of_a_kind[0])
        self.assertEqual(7, three_of_a_kind[1])
        self.assertEqual(5, len(three_of_a_kind[2]))
        self.assertEqual(Face.Queen, three_of_a_kind[2][0].face)
        self.assertEqual(Face.Jack, three_of_a_kind[2][1].face)
        self.assertEqual(Face.Seven, three_of_a_kind[2][-1].face)

    def test_pair(self):
        pair_holecards = HoleCards(cards=['AH', '10D'])
        pair_community = Community(cards=['AD', '9S', '6C', '7S', '3D'])
        pair = has_x_of_a_kind(pair_community.cards + pair_holecards.cards)
        self.assertEqual(2, pair[0])
        self.assertEqual(14, pair[1])
        self.assertEqual(5, len(pair[2]))
        self.assertEqual(Face.Seven,pair[2][-1].face)
        self.assertEqual(Face.Nine, pair[2][-2].face)
        self.assertEqual(Face.Ten, pair[2][-3].face)
        self.assertEqual(Face.Ace, pair[2][0].face)

        pair_holecards = HoleCards(cards=['7H', '7D'])
        pair_community = Community(cards=['QD', '4S', 'JC', '10C', '3D'])
        pair = has_x_of_a_kind(pair_community.cards + pair_holecards.cards)
        self.assertEqual(2, pair[0])
        self.assertEqual(7, pair[1])
        self.assertEqual(5, len(pair[2]))
        self.assertEqual(Face.Queen, pair[2][0].face)
        self.assertEqual(Face.Jack, pair[2][1].face)
        self.assertEqual(Face.Ten, pair[2][2].face)
        self.assertEqual(Face.Seven, pair[2][-1].face)

    def test_full_house(self):
        fullhouse_holecards = HoleCards(cards=['7H', '10D'])
        fullhouse_community = Community(cards=['QD', '7S', '7C', '10C', '3D'])
        fullhouse = has_full_house(fullhouse_community.cards + fullhouse_holecards.cards)
        self.assertEqual(7, fullhouse[0])
        self.assertEqual(5, len(fullhouse[1]))
        self.assertEqual(Face.Seven, fullhouse[1][0].face)
        self.assertEqual(Face.Seven, fullhouse[1][2].face)
        self.assertEqual(Face.Ten, fullhouse[1][-1].face)

        fullhouse_holecards = HoleCards(cards=['KH', 'KD'])
        fullhouse_community = Community(cards=['QD', 'KS', '7C', 'QC', '3D'])
        fullhouse = has_full_house(fullhouse_community.cards + fullhouse_holecards.cards)
        self.assertEqual(13, fullhouse[0])
        self.assertEqual(5, len(fullhouse[1]))
        self.assertEqual(Face.King, fullhouse[1][0].face)
        self.assertEqual(Face.King, fullhouse[1][2].face)
        self.assertEqual(Face.Queen, fullhouse[1][-1].face)

    def test_two_pair(self):
        twopair_holecards = HoleCards(cards=['7H', '10D'])
        twopair_community = Community(cards=['QD', '4S', '7C', '10C', '3D'])
        twopair = has_two_pair(twopair_community.cards + twopair_holecards.cards)
        self.assertEqual(10, twopair[0])
        self.assertEqual(5, len(twopair[1]))
        self.assertEqual(Face.Ten, twopair[1][0].face)
        self.assertEqual(Face.Seven, twopair[1][2].face)
        self.assertEqual(Face.Queen, twopair[1][-1].face)

        twopair_holecards = HoleCards(cards=['KH', 'KD'])
        twopair_community = Community(cards=['QD', '9S', '7C', 'QC', '3D'])
        twopair = has_two_pair(twopair_community.cards + twopair_holecards.cards)
        self.assertEqual(13, twopair[0])
        self.assertEqual(5, len(twopair[1]))
        self.assertEqual(Face.King, twopair[1][0].face)
        self.assertEqual(Face.Queen, twopair[1][2].face)
        self.assertEqual(Face.Nine, twopair[1][-1].face)

    def test_straight_flush(self):
        straightflush_holecards = HoleCards(cards=['7H', '10H'])
        straightflush_community = Community(cards=['8H', '4S', '6H', '9H', '2C'])
        straightflush = has_straight_flush(straightflush_community.cards + straightflush_holecards.cards)
        self.assertEqual(5, len(straightflush))
        self.assertEqual(Face.Ten, straightflush[0].face)

        straightflush_holecards = HoleCards(cards=['QD', '10D'])
        straightflush_community = Community(cards=['2H', '9D', '8D', 'JD', '7D'])
        straightflush = has_straight_flush(straightflush_community.cards + straightflush_holecards.cards)
        self.assertEqual(6, len(straightflush))
        self.assertEqual(Face.Queen, straightflush[0].face)
