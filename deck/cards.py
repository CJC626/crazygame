from enum import Enum
import json

class Card:

    def __init__(self, **kwargs):
        suit_enum = None
        face_enum = None
        if('cardstr' in kwargs):
            cardstr = kwargs['cardstr']
            facestr = None
            suitstr = None
            if(len(cardstr)==3):
                facestr = cardstr[0:2]
                suitstr = cardstr[2]
            else:
                facestr = cardstr[0]
                suitstr = cardstr[1]
            for f in Face:
                if (f.value[0] == facestr):
                    face_enum = f
                    break
            for s in Suit:
                if (s.value[0] == suitstr):
                    suit_enum = s
                    break
            self.suit=suit_enum
            self.face=face_enum
        elif('suit' in kwargs and 'face' in kwargs):
            suit_enum=kwargs['suit']
            face_enum=kwargs['face']
        else:
            raise ValueError("Illegal kwargs: " + json.dumps(kwargs))
        self.suit = suit_enum
        self.face = face_enum

    def is_card_equal(self, card):
        return card.suit == self.suit and card.face == self.face

    def strength(self):
        return self.face.strength()

class Suit(Enum):
    Hearts = ["H","Hearts"]
    Spades = ["S","Spades"]
    Clubs = ["C","Clubs"]
    Diamonds = ["D","Diamonds"]

class Face(Enum):
    Two = ['2',2]
    Three = ['3',3]
    Four = ['4',4]
    Five = ['5',5]
    Six = ['6',6]
    Seven = ['7',7]
    Eight = ['8',8]
    Nine = ['9',9]
    Ten = ['10',10]
    Jack = ['J',11]
    Queen = ['Q',12]
    King = ['K',13]
    Ace = ['A',14]

    def strength(self):
        return self.value[1]