from pages import Page, Pages, SCSSPage, TemplatePage
from jinja2.utils import generate_lorem_ipsum as lipsum
from random import random
import os
from ordereddict import OrderedDict
import string


A_TO_Z = list(
  [l, lipsum(5) if random() > 0.2 else None, False] for l in string.ascii_uppercase
)

A_TO_Z[0][1] = lipsum(5)
A_TO_Z[0][2] = True


# css pages

def get_directory_structure(rootdir):
  """
  Creates a nested dictionary that represents the folder structure of rootdir
  """
  dir = OrderedDict()
  rootdir = rootdir.rstrip(os.sep)
  start = rootdir.rfind(os.sep) + 1
  for path, dirs, files in os.walk(rootdir):
    folders = path[start:].split(os.sep)
    subdir = OrderedDict.fromkeys(files)
    parent = reduce(OrderedDict.get, folders[:-1], dir)
    parent[folders[-1]] = subdir
  return dir
  

scss = get_directory_structure('scss')['scss']

def shuffle_dirs(dir, cls):
  for p, c in dir.items():
    if p != 'meta':
      if c:
        children = list(shuffle_dirs(c, cls))
        yield cls(p, children=children)
      else:
        yield cls(p, p)

scss_pages = list(shuffle_dirs(scss, SCSSPage))

templates = get_directory_structure('templates')['templates']

template_pages = list(shuffle_dirs(templates, TemplatePage))

pages = Pages([
  Page('About', 'demo.html'),
  Page('Page Layouts', 'layouts/overview.html', children=[
    Page('Subsection with navigation', 'layouts/subnav.html'),
    Page('Subsection without navigation', 'layouts/subnonav.html'),
    Page('Subsection without right column', 'layouts/subnocol.html'),
    Page('App', 'layouts/app.html'),
    Page('Cambridge Front Page', 'layouts/campage.html', globals={'CAM_PAGE': True}),
  ]),
  Page('Core Elements', children=[
    Page('Typography', 'core_elements/typography.html'),
    Page('Links and Buttons', 'core_elements/links_and_buttons.html'),
    Page('Forms', 'core_elements/forms.html'),
    Page('Lists', 'core_elements/lists.html'),
  ]),
  Page('In Page Components', children=[
    Page('Navigation', children=[
      Page('Tabs', 'components/inpage/navigation/tabs.html'),
      Page('Pills', 'components/inpage/navigation/pills.html'),
      Page('Pills (Stacked)', 'components/inpage/navigation/pills_stacked.html'),
      Page('Stages', 'components/inpage/navigation/stages.html'),
      Page('Pagination', 'components/inpage/navigation/pagination.html'),
      Page('A to Z', 'components/inpage/navigation/atoz.html', context={'A_TO_Z': A_TO_Z}),
      Page('Search', 'components/inpage/navigation/search.html'),
    ]),
    Page('Content', children=[
      Page('Tables', 'components/inpage/content/tables.html'),
      Page('Alerts', 'components/inpage/content/alerts.html'),
      Page('Date/Time Picker', 'components/inpage/content/datetimepicker.html'),
    ]),
    Page('Teasers', 'components/teasers/examples.html'),
  ]),
  Page('Stylesheets', children=scss_pages),
  Page('Templates', children=template_pages),
])

front_page = Page(
  'Home',
  'layouts/frontpage_example.html',
  front_page=True,
)
