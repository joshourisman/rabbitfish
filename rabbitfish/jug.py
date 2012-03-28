import yaml

from pages import Page, DynamicPage, ListPage


class Site(object):
    def __init__(self, config_file=None):
        self.config = None
        self.pages = []
        self.dynamic_pages = {}

        if config_file is not None:
            self.load_configuration(config_file)

    def load_configuration(self, config_file):
        self.config = yaml.load(open(config_file, 'r'))
        self.pages = self.config['pages']
        for page in self.pages:
            if type(page) is DynamicPage:
                self.dynamic_pages[page.name] = page

    def generate(self):
        for page in self.pages:
            if type(page) is ListPage:
                page.render_to_output(self.dynamic_pages)
            else:
                page.render_to_output()


def generatesite():
    site = Site("config.yaml")
    site.generate()
