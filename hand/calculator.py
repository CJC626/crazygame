from hand.hands import Hand
from deck.cards import Suit, Face
from enum import Enum

class HandPower(Enum):
    HighCard = 0
    Pair = 1
    TwoPair = 2
    ThreeOfAKind = 3
    Straight = 4
    Flush = 5
    FullHouse = 6
    FourOfAKind = 7
    StraightFlush = 8

class HandOutcome:

    def __init__(self, power, strength, *involvedCards):
        self.power = power
        self.strength = strength
        self.involvedCards = involvedCards

def has_flush(cards):
    temp_card_stack = {
        Suit.Spades: [],
        Suit.Diamonds: [],
        Suit.Hearts: [],
        Suit.Clubs: []
    }

    for c in cards:
        temp_card_stack[c.suit].append(c)
    for k in temp_card_stack.keys():
        if len(temp_card_stack[k]) > 4:
            temp_card_stack[k].sort(key=lambda c: c.strength(), reverse=True)
            return temp_card_stack[k]
    return None

def has_straight(cards):

    if len(cards) < 5:
        return None

    cards_in_straight = []

    cards.sort(key=lambda c: c.strength())
    cards_sorted = 1
    possible_low_ace_straight = False
    bottom_strength = None
    for ix, c in enumerate(cards):
        if(ix==0):
            if(c.face == Face.Two):
                possible_low_ace_straight = True
            cards_in_straight.append(c)
            bottom_strength = c.strength()
        else:
            if c.face == Face.Ace:
                if possible_low_ace_straight and cards_sorted == 4:
                    cards_in_straight.append(c)
                    cards_sorted = cards_sorted + 1
            if c.strength() - cards_in_straight[-1].strength() == 1:
                cards_sorted = cards_sorted + 1
                cards_in_straight.append(c)
            elif c.strength() - cards_in_straight[-1].strength() == 0:
                pass
            elif possible_low_ace_straight:
                pass
            elif(cards_sorted < 5):
                cards_sorted = 1
                cards_in_straight = [c]
                bottom_strength = c.strength()
    if len(cards_in_straight) < 5:
        return None
    else:
        cards_in_straight.sort(key=lambda c: c.strength(), reverse=True)
        return cards_in_straight

def has_x_of_a_kind(cards):
    facesets = {}
    for c in cards:
        if(c.face not in facesets):
            facesets[c.face] = [c]
        else:
            facesets[c.face].append(c)
    x_of_a_kind_ct = 0
    x_of_a_kind_strength = 0
    cards_in_x_of_a_kind = []
    for k in facesets.keys():
        if len(facesets[k]) > x_of_a_kind_ct or (len(facesets[k]) == x_of_a_kind_ct and k.strength() > x_of_a_kind_strength) :
            x_of_a_kind_ct = len(facesets[k])
            x_of_a_kind_strength = k.strength()
            cards_in_x_of_a_kind = facesets[k]
    if(x_of_a_kind_ct == 1):
        return None
    #add next highest cards
    othercards = []
    other_card_ct = 5 - x_of_a_kind_ct
    for c in cards:
        if c not in cards_in_x_of_a_kind and (len(othercards) < other_card_ct or c.strength() > othercards[-1].strength()):
            if len(othercards) == other_card_ct:
                othercards.pop()
            othercards.append(c)
            othercards.sort(key=lambda c1: c1.strength(), reverse=True)
    bestcards = cards_in_x_of_a_kind + othercards
    bestcards.sort(key=lambda c: c.strength(), reverse=True)
    return [x_of_a_kind_ct, x_of_a_kind_strength, bestcards]

def has_full_house(cards):
    highest_x_of_a_kind = has_x_of_a_kind(cards)
    if highest_x_of_a_kind is None or highest_x_of_a_kind[0] != 3:
        return None
    non_threex_cards = []
    threex_cards = []
    for c in cards:
        if c.strength() == highest_x_of_a_kind[1]:
            threex_cards.append(c)
        else:
            non_threex_cards.append(c)
    next_highest_x_of_a_kind = has_x_of_a_kind(non_threex_cards)
    if next_highest_x_of_a_kind is None or next_highest_x_of_a_kind[0] != 2:
        return None
    pair_cards = []
    for c in cards:
        if c.strength() == next_highest_x_of_a_kind[1]:
            pair_cards.append(c)
    fullhouse = threex_cards + pair_cards
    return [fullhouse[0].strength(), fullhouse]

def has_two_pair(cards):
    highest_pair = has_x_of_a_kind(cards)
    if highest_pair is None or highest_pair[0] != 2:
        return None
    first_pair_cards = []
    second_pair_cards = []
    non_pair_cards = []
    for c in cards:
        if c.strength() == highest_pair[1]:
            first_pair_cards.append(c)
        else:
            non_pair_cards.append(c)
    next_highest_pair = has_x_of_a_kind(non_pair_cards)
    if next_highest_pair is None or next_highest_pair[0] != 2:
        return None
    for c in non_pair_cards:
        if c.strength() == next_highest_pair[1]:
           second_pair_cards.append(c)
    for c in second_pair_cards:
        non_pair_cards.remove(c)
    non_pair_cards.sort(key=lambda c: c.strength(), reverse=True)
    return [highest_pair[1], first_pair_cards + second_pair_cards + [non_pair_cards[0]]]

def has_straight_flush(cards):
    flush = has_flush(cards)
    if(flush is None):
        return None
    straight_flush = has_straight(flush)
    if(straight_flush is not None):
        straight_flush.sort(key=lambda c: c.strength(), reverse=True)
        return straight_flush
    return None