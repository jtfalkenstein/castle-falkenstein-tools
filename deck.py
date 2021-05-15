import itertools
from typing import List, Callable
import random
from card import Card, FACE_CARDS, Suit


class Deck:
    def __init__(self, cards: List[Card]) -> None:
        self.cards = cards
    
    @classmethod
    def new(cls):
        numbered_cards = map(str, range(2, 11))
        all_card_values = itertools.chain(numbered_cards, FACE_CARDS)
        suits = [Suit.Spades, Suit.Clubs, Suit.Diamonds, Suit.Hearts]
        normal_cards = itertools.product(all_card_values, suits)
        jokers = [('Joker', Suit.Red), ('Joker', Suit.Black)]
        all_cards = map(lambda t: Card(*t), itertools.chain(normal_cards, jokers))
        all_cards_list = list(all_cards)
        return cls(all_cards_list)
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self, index=0):
        return self.cards.pop(index)

    def deal_face_card(self):
        return self.deal_first_card(lambda card: card.is_face_card)

    def deal_numeric_card(self):
        return self.deal_first_card(lambda card: card.is_numeric)

    def deal_first_card(self, evaluator: Callable[[Card], bool]):
        for index, card in enumerate(self.cards):
            if evaluator(card):
                return self.deal_card(index)