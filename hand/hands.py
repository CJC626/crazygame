from deck.cards import Card, Suit, Face
from enum import Enum

class Hand:

    def __init__(self, cards):
        self.cards = []
        for c in cards:
            if(isinstance(c, str)):
                self.cards.append(Card(cardstr=c))
            elif(isinstance(c, Card)):
                self.cards.append(c)
            else:
                raise TypeError

    def has_card(self, card):
        for c in self.cards:
            if(c.suit == card.suit and c.face == card.face):
                return True
        return False

    def equal_to(self, hand):
        cards = None
        if(isinstance(hand, Hand)):
            cards = hand.cards
        else:
            cards = hand
        for hc in cards:
            if(not self.has_card(hc)):
                return False
        return True

class HoleCards(Hand):

    def __init__(self, cards):
        super().__init__(cards)

    def strongest_five_by_face(self, community):
        all_cards = self.cards + community.cards
        if (len(all_cards) < 6):
            return all_cards
        all_cards.sort(key=lambda c: c.strength(), reverse=True)
        return all_cards[:5]

    def high_card(self, community):
        strongest_five = self.strongest_five_by_face(community)
        hc = None
        for c in strongest_five:
            if(hc is None):
                hc = c.strength()
            else:
                if(hc < c.strength()):
                    hc = c.strength()
        return hc

class Community(Hand):

    def __init__(self, cards):
        super().__init__(cards)

    def current_Phase(self):
        if(len(self.cards) in community_cards_in_phase.keys()):
            return community_cards_in_phase[len(self.cards)]
        else:
            raise KeyError

class Phase(Enum):
    PreFlop = 0
    Flop = 1
    Turn = 2
    River = 3

community_cards_in_phase = {
    0: Phase.PreFlop,
    3: Phase.Flop,
    4: Phase.Turn,
    5: Phase.River
}