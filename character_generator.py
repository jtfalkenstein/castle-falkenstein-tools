import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict

import pandas as pd

from card import Color
from deck import Deck, Suit
from name_generator import generate_random_name

TEMPERAMENT_MAP = {
    ('K', Suit.Diamonds): 'Plodder, hard worker, dull, unimaginative',
    ('K', Suit.Clubs): 'Energetic, showoff, entertainer, wiseguy',
    ('K', Suit.Hearts): 'Romantic, lover, and a dreamer',
    ('K', Suit.Spades): 'Domineering, strong-willed, forceful, a bully',
    ('Q', Suit.Diamonds): 'An organizer, blunt, goal-oriented, active',
    ('Q', Suit.Clubs): 'Expensive tastes, vain, self-absorbed, a star',
    ('Q', Suit.Spades): 'Two-faced, conniving, treacherous, sneaking',
    ('Q', Suit.Hearts): 'Mothering, domestic, loving, & supportive',
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
    Suit.Spades: 'Ruthless, ambitious, treacherous'
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

NAME_TYPE_MAP = {
    'Faerie': ['elf_names', 'dark-elf-names', 'nymph-names', 'selkie-names'],
    'Dwarf': ['dwarf_names'],
    'Dragon': ['dragon_names'],
    'Human': ['french_names', 'british-english-names', 'spanish-names', 'italian_names', 'dutch_names']
}

class SkillLevel(IntEnum):
    poor = -2
    average = 0
    good = 1
    great = 2
    exceptional = 4
    extraordinary = 6

SKILL_WEIGHTS = {
    SkillLevel.poor: 30,
    SkillLevel.average: 70,
    SkillLevel.good: 30,
    SkillLevel.great: 10,
    SkillLevel.exceptional: 4,
    SkillLevel.extraordinary: 1
}



skills = [
    'Perception',
    'Athletics',
    'Marksmanship',
    'Fisticuffs',
    'Fencing',
    'Physique',
    'Courage',
]

HEALTH_TABLE = pd.DataFrame(
    data=[
        [3, 4, 5, 6, 7, 8],
        [4, 5, 6, 7, 8, 8],
        [5, 6, 7, 8, 8, 8],
        [6, 7, 8, 8, 8, 9],
        [7, 8, 8, 8, 9, 9],
        [8, 8, 8, 8, 8, 10]
    ],
    columns=[l.name for l in SkillLevel],
    index=[l.name for l in SkillLevel]
)

@dataclass
class Character:
    race: str
    temperament: str
    motives: str
    weapon: str
    name: str
    abilities: Dict[str, SkillLevel]
    health: int
    name_type: str

def select_abilities(overall_ability_level: int, race: str):
    current_total = 0
    abilities = {}
    all_abilities = list(skills)
    if race == 'Faerie':
        all_abilities.extend(['Etherealness', 'Glamour', 'Kindred Powers'])
    elif race in ('Human', 'Dragon'):
        all_abilities.append('Sorcery')

    ability_selection_iterations = 0
    while current_total != overall_ability_level or ability_selection_iterations < 1:
        ability_selection_iterations += 1
        random.shuffle(all_abilities)
        for ability in all_abilities:
            if ability in abilities and abilities[ability].value > 0:
                abilities.pop(ability)

            if ability_selection_iterations > 1 and current_total == ability_selection_iterations:
                break
            elif ability_selection_iterations > 1 and current_total > overall_ability_level:
                ability_level = SkillLevel.poor
            else:
                ability_level = random.choices(list(SKILL_WEIGHTS.keys()), list(SKILL_WEIGHTS.values()))[0]
            
            if ability_level == SkillLevel.average:
                continue

            abilities[ability] = ability_level
            current_total = sum(e.value for e in abilities.values())

    print(f'Iterations required to create ability level of {overall_ability_level}: {ability_selection_iterations}')
    return abilities


def get_race(deck: Deck):
    race_card = deck.deal_card()
    numeric_value = race_card.numeric_value
    if numeric_value >= 14:
        return 'Dragon'
    elif numeric_value >= 11 and race_card.color == Color.Red:
        return 'Dwarf'
    elif numeric_value >= 11 and race_card.color == Color.Black:
        return 'Faerie'
    else:
        return 'Human'
    

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

def get_name(race_name: str):
    name_types = NAME_TYPE_MAP[race_name]
    return generate_random_name(name_types)

def calculate_health(abilities: Dict[str, SkillLevel], race: str):
    physique = abilities.get('Physique', SkillLevel.average).name
    courage = abilities.get('Courage', SkillLevel.average).name
    health = HEALTH_TABLE.loc[physique, courage]
    if race == 'Dragon':
        health += 2

    return health

def make_character(race: None, ability_level=0):
    deck = Deck.new()
    deck.shuffle()
    if not race:
        race = get_race(deck)
    temperament = get_temperament(deck)
    motives = get_motives(deck)
    weapon = get_weapon(deck)
    name_type, name = get_name(race)
    abilities = select_abilities(ability_level, race)
    health = calculate_health(abilities, race)

    return Character(race, temperament, motives, weapon, name, abilities, health, name_type)


if __name__ == '__main__':
    from dataclasses import asdict
    from pprint import pprint
    pprint(asdict(make_character(0)))
