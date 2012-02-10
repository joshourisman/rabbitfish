import datetime
import os
import yaml

from jinja2 import Environment, FileSystemLoader

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
        return {content['slug']: template.render({'object': content}) for
                content in content_list}

    def render_to_output(self):
        print("Rendering dynamic page {0} with {1}".format(
                self.name, self.template))
        template = env.get_template(self.template)
        content_list = yaml.load_all(open("content/{}.yaml".format(self.name)))
        for content in content_list:
            print(" - Rendering {}".format(content['slug']))
            html = template.render({'object': content})
            url_context = {
                'slug': content['slug'],
            }
            if 'date' in content and type(content['date']) in [datetime.date, datetime.datetime]:
                url_context['date'] = content['date']
            url = self.url.format(**url_context)
            output = "output/{}".format(url)
            directory = os.path.dirname(output)
            if not os.path.exists(directory):
                os.makedirs(directory)
            open(output, 'w').write(html)


class IndexPage(Page):
    yaml_tag = '!IndexPage'

    def render_to_string(self):
        print("Rendering index page {0} with {1}".format(
                self.name, self.template))
        template = env.get_template(self.template)
        content_list = yaml.load_all(
            open("content/{}.yaml".format(self.to_index)))

        index = []
        for i in range(self.num_to_index):
            index.append(content_list.__next__())
        return template.render({'object_list': index})
