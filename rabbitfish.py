#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import yaml

print("One dead, unjugged rabbitfish later...")

env = Environment(loader=FileSystemLoader('templates'))

class Page(yaml.YAMLObject):
    yaml_tag = '!Page'

config = yaml.load(open("config.yaml", 'r'))
pages = config['pages']
if os.path.exists('output'):
    shutil.rmtree('output')
for page in pages:
    name = page.name
    template = page.template
    url = getattr(page, 'url', '{}.html'.format(name))
    output = "output/{}".format(url)
    print("Rendering page {0} to {1}.".format(name, output))

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)
    template = env.get_template(template)
    content = yaml.load(open("content/{}.yaml".format(name)))
    open(output, 'w').write(template.render(**content))

