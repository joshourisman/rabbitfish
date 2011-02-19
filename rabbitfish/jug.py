import os
import shutil
import yaml

from pages import Page, DynamicPage

def generatesite():
    config = yaml.load(open("config.yaml", 'r'))
    pages = config['pages']
    if os.path.exists('output'):
        shutil.rmtree('output')
    for page in pages:
        page.render_to_output()

