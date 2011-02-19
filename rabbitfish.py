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

    def render_to_string(self):
        print("Rendering page {0} with {1}.".format(self.name, self.template))
        template = env.get_template(self.template)
        content = yaml.load(open("content/{}.yaml".format(self.name)))
        return template.render(**content)

    def render_to_output(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        open(self.output, 'w').write(self.render_to_string())

class DynamicPage(Page):
    yaml_tag = '!DynamicPage'

    def __setstate__(self, state):
        if 'url' not in state:
            state['url'] = "{}.html"
        self.__dict__.update(state)

    def render_to_string(self):
        print("Rendering dynamic page {0} with {1}".format(
                self.name, self.template))
        template = env.get_template(self.template)
        content_list = yaml.load_all(open("content/{}.yaml".format(self.name)))
        return {content['slug']:template.render(**content) for
                content in content_list}
        
    def render_to_output(self):
        pages = self.render_to_string()
        for slug in pages:
            url = self.url.format(slug=slug)
            output = "output/{}".format(url)
            directory = os.path.dirname(output)
            if not os.path.exists(directory):
                os.mkdirs(directory)
            open(output, 'w').write(pages[slug])
    
config = yaml.load(open("config.yaml", 'r'))
pages = config['pages']
if os.path.exists('output'):
    shutil.rmtree('output')
for page in pages:
    page.render_to_output()
