#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('templates'))

print("One dead, unjugged rabbitfish later...")
config = yaml.load(open("config.yaml", 'r'))

index = env.get_template('index.html')
open("output/index.html", 'w').write(index.render(**config))
