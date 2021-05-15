from deck import Suit, Deck
from dataclasses import dataclass


RACE_MAP = {
    Suit.Spades: 'Dwarf',
    Suit.Clubs: 'Human',
    Suit.Diamonds: 'Dragon',
    Suit.Hearts: 'Faerie'
}

TEMPERAMENT_MAP = {
    ('K', Suit.Diamonds): 'Plodder, hard worker, dull, unimaginative',
    ('K', Suit.Clubs): 'Energetic, showoff, entertainer, wiseguy',
    ('K', Suit.Hearts): 'Romantic, lover, and a dreamer',
    ('K', Suit.Spades): 'Domineering, strong-willed, forceful, a bully',
    ('Q', Suit.Diamonds): 'An organizer, blunt, goal-oriented, active',
    ('Q', Suit.Clubs): 'Expensive tastes, vain, self-absorbed, a star',
    ('Q', Suit.Spades): 'Two-faced, conniving, treacherous, sneaking',
    ('J', Suit.Diamonds): 'Quick-witted; a good communicator',
    ('J', Suit.Clubs): 'Insecure, vacillating, painfully shy',
    ('J', Suit.Hearts): 'Immature and childlike, throws tantrums',
    ('J', Suit.Spades): 'A charmer and flirt, a bit superficial',
    ('A', Suit.Diamonds): 'Friendly, open, a team player',
    ('A', Suit.Clubs): 'Clever, witty, life of the party',
    ('A', Suit.Hearts): 'Cheerful, mature, really likeable',
    ('A', Suit.Spades): 'Honest, blunt, and trustworthy'
}

INNER_MOTIVES_MAP = {
    Suit.Clubs: 'Aggressive, warlike, violent, short-tempered',
    Suit.Hearts: 'Friendly, helpful, loving and open',
    Suit.Diamonds: 'Mercenary, logical, remote, calculting',
    Suit.Spades: 'Ruthless, ambitions, treacherous'
}

PRIMARY_WEAPON = {
    2: 'Fists (Defer to Physique)',
    3: 'Pocket-knife (1/1/2)',
    4: 'Dagger (1/2/2)',
    5: 'Combat Knife (1/2/3)',
    6: 'Saber (3/4/5)',
    7: 'Saber (4/5/6)',
    8: '6-shot revolver (4/5/6)',
    9: 'Derringer (3/4/5)',
    10: 'Rifle (4/5/6)'
}


@dataclass
class Character:
    race: str
    temperament: str
    motives: str
    weapon: str


def get_race(deck: Deck):
    race_card = deck.deal_face_card()
    race = RACE_MAP[race_card.suit]
    return race

def get_temperament(deck: Deck):
    temperament_card = deck.deal_face_card()
    temperament = TEMPERAMENT_MAP[(temperament_card.value, temperament_card.suit)]
    return temperament

def get_motives(deck: Deck):
    motives_card = deck.deal_face_card()
    motives = INNER_MOTIVES_MAP[(motives_card.suit)]
    return motives

def get_weapon(deck: Deck):
    weapon_card = deck.deal_numeric_card()
    weapon = PRIMARY_WEAPON[weapon_card.numeric_value]
    return weapon

def make_character():
    deck = Deck.new()
    deck.shuffle()
    race = get_race(deck)
    temperament = get_temperament(deck)
    motives = get_motives(deck)
    weapon = get_weapon(deck)

    return Character(race, temperament, motives, weapon)


if __name__ == '__main__':
    print(make_character())