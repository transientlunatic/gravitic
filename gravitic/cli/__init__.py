import click
import os
import yaml

@click.group()
def gravitic():
    pass

@gravitic.command()
def init():
    """
    Initialise a gravitic pipeline.
    """
    data = {}

    data['blocks'] = []
    
    with open("specification.yml", "w") as yaml_file:
        yaml_file.write(yaml.dump(data))

