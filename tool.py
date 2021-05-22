import random
from dataclasses import asdict
from pprint import pformat
from random import choice

import click

from character_generator import NAME_TYPE_MAP, make_character


@click.group()
def cli():
    pass

@cli.command()
@click.option(
    '-r',
    '--race',
    type=click.Choice(NAME_TYPE_MAP.keys()),
    default=lambda: random.choice(list(NAME_TYPE_MAP.keys()))
)
@click.option(
    '-a',
    '--ability-level',
    type=click.INT,
    default=0
)
def generate_character(race, ability_level):
    result = make_character(race, ability_level)
    result_dict = asdict(result)
    click.echo(pformat(result_dict))


if __name__ == '__main__':
    cli.main()
