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

    def get_context(self, **kwargs):
        return kwargs

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

        pages = []
        for content in content_list:
            html = template.render({'object': content})
            url_context = {
                'slug': content['slug'],
            }
            if 'date' in content and type(content['date']) in \
                [datetime.date, datetime.datetime]:
                url_context['date'] = content['date']
            url = self.url.format(**url_context)
            pages.append((url, html))

        return pages

    def render_to_output(self):
        pages = self.render_to_string()
        print(" - Rendered {} instances of DynamicPage {}".format(
            len(pages), self.name))
        for page in pages:
            url = page[0]
            html = page[1]
            output = "output/{}".format(url)
            directory = os.path.dirname(output)
            if not os.path.exists(directory):
                os.makedirs(directory)
            open(output, 'w').write(html)


class ListPage(Page):
    yaml_tag = '!ListPage'

    def get_page_url(self, page):
        page_type = self.dynamic_pages[self.to_index]
        url_format = page_type.url
        url_context = {'slug': page['slug']}
        if 'date' in page and type(page['date']) in \
            [datetime.date, datetime.datetime]:
            url_context['date'] = page['date']

        url = url_format.format(**url_context)
        return url

    def render_to_string(self):
        print("Rendering list page {0} with {1}".format(
                self.name, self.template))
        template = env.get_template(self.template)
        content_list = yaml.load_all(
            open("content/{}.yaml".format(self.to_index)))

        index = []
        for i in range(self.num_to_index):
            page = content_list.__next__()
            page['url'] = self.get_page_url(page)
            index.append(page)
        return template.render({'object_list': index})

    def render_to_output(self, dynamic_pages):
        self.dynamic_pages = dynamic_pages
        super(ListPage, self).render_to_output()
