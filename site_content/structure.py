from pages import Page, Pages, SCSSPage, TemplatePage, FrontPage
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
    Page('Subsection without navigation', 'layouts/subnonav.html', side_menu=False),
    Page('Subsection without right column', 'layouts/subnocol.html'),
    Page('App', 'layouts/app.html', side_menu=False),
    Page('Cambridge Front Page', 'layouts/campage.html', globals={'CAM_PAGE': True}),
  ]),
  Page('Core Elements', children=[
    Page('Typography', 'core_elements/typography.html', scss=['core_elements/_typography.scss', 'core_elements/_blockquote.scss']),
    Page('Links and Buttons', 'core_elements/links_and_buttons.html', scss=['core_elements/_buttons.scss']),
    Page('Forms', 'core_elements/forms.html'),
    Page('Lists', 'core_elements/lists.html'),
    Page('Themes', 'core_elements/themes.html'),
  ]),
  Page('In Page Components', children=[
    Page('Navigation', children=[
      Page('Tabs', 'components/inpage/navigation/tabs.html', scss=['components/navigation/_nav.scss']),
      Page('Pills', 'components/inpage/navigation/pills.html', scss=['components/navigation/_nav.scss']),
      Page('Pills (Stacked)', 'components/inpage/navigation/pills_stacked.html', scss=['components/navigation/_nav.scss']),
      Page('Stages', 'components/inpage/navigation/stages.html', scss=['components/navigation/_nav.scss']),
      Page('Pagination', 'components/inpage/navigation/pagination.html', scss=['components/navigation/_pagination.scss']),
      Page('A to Z', 'components/inpage/navigation/atoz.html', context={'A_TO_Z': A_TO_Z}, side_menu=False),
      Page('Search', 'components/inpage/navigation/search.html', scss=['components/navigation/_search.scss']),
    ]),
    Page('Content', children=[
      Page('Tables', 'components/inpage/content/tables.html', scss=['components/inpage/_tables.scss']),
      Page('Alerts', 'components/inpage/content/alerts.html', scss=['components/inpage/_alerts.scss']),
      Page('Date/Time Picker', 'components/inpage/content/datetimepicker.html'),
    ]),
    Page('Teasers', 'components/teasers/examples.html', side_menu=False),
  ]),
  Page('Templates', children=template_pages),
  Page('Stylesheets', children=scss_pages),
])

front_page = FrontPage(
  'Home',
  'layouts/frontpage_example.html',
  pages,
)