from dataclasses import dataclass
from enum import Enum

class Color(Enum):
    Red = 1
    Black = 2

class Suit(Enum):
    Spades = 1
    Clubs = 2
    Hearts = 3
    Diamonds = 4
    Red = 5
    Black = 6

SUITS_TO_COLORS = {
    Suit.Spades: Color.Black,
    Suit.Clubs: Color.Black,
    Suit.Diamonds: Color.Red,
    Suit.Hearts: Color.Red,
    Suit.Red: Color.Red,
    Suit.Black: Color.Black
}

FACE_CARDS = ['J', 'Q', 'K', 'A']


@dataclass
class Card:
    value: str
    suit: Suit

    @property
    def numeric_value(self):
        if self.is_numeric:
            return int(self.value)
        
        if self.is_joker:
            return 15
        
        return 11 + FACE_CARDS.index(self.value)

    @property
    def is_face_card(self):
        return self.value in FACE_CARDS
    
    @property
    def is_numeric(self):
        return self.value.isnumeric()

    @property
    def is_joker(self):
        return self.value == 'Joker'

    @property
    def color(self):
        return SUITS_TO_COLORS[self.suit]
    
        
