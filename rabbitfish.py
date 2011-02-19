#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import yaml

print("One dead, unjugged rabbitfish later...")

env = Environment(loader=FileSystemLoader('templates'))

class Page(yaml.YAMLObject):
    yaml_tag = '!Page'

    def __setstate__(self, state):
        if 'url' not in state:
            state['url'] = "{}.html".format(state['name'])
        state['output'] = "output/{}".format(state['url'])
        state['directory'] = os.path.dirname(state['output'])
        self.__dict__.update(state)

    def render(self):
        print("Rendering page {0} with {1}.".format(self.name, self.template))
        template = env.get_template(self.template)
        content = yaml.load(open("content/{}.yaml".format(self.name)))
        return template.render(**content)

config = yaml.load(open("config.yaml", 'r'))
pages = config['pages']
if os.path.exists('output'):
    shutil.rmtree('output')
for page in pages:
    if not os.path.exists(page.directory):
        os.makedirs(page.directory)
    open(page.output, 'w').write(page.render())
