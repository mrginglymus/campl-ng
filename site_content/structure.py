from .pages import Page, Pages, SCSSPage, TemplatePage, FrontPage, CoffeePage
from jinja2.utils import generate_lorem_ipsum as lipsum
import os
from ordereddict import OrderedDict


def get_directory_structure(rootdir, ext):
  """
  Creates a nested dictionary that represents the folder structure of rootdir
  """
  dir = OrderedDict()
  rootdir = rootdir.rstrip(os.sep)
  start = rootdir.rfind(os.sep) + 1
  for path, dirs, files in os.walk(rootdir):
    folders = path[start:].split(os.sep)
    files = filter(lambda x: x.endswith('.%s' % ext), files)
    subdir = OrderedDict.fromkeys(files)
    parent = reduce(OrderedDict.get, folders[:-1], dir)
    parent[folders[-1]] = subdir
  return dir


def shuffle_dirs(dir, cls):
  for p, c in dir.items():
    if c:
      children = list(shuffle_dirs(c, cls))
      yield cls(p, children=children)
    else:
      yield cls(p, p)


scss = get_directory_structure('scss', 'scss')['scss']

scss_pages = list(shuffle_dirs(scss, SCSSPage))

templates = get_directory_structure('templates', 'html')['templates']

template_pages = list(shuffle_dirs(templates, TemplatePage))

coffee = get_directory_structure('coffee', 'coffee')['coffee']

coffee_pages = list(shuffle_dirs(coffee, CoffeePage))

pages = Pages([
  Page('About', 'pages/about.html'),
  Page('Page Layouts', children=[
    Page('App', 'layout/app.html', side_menu=False),
    Page('Cambridge Front Page', 'layout/campage.html', globals={'CAM_PAGE': True}),
  ]),
  Page('Core Elements', children=[
    Page('Typography', 'pages/core_elements/typography.html', scss=['core_elements/_typography.scss', 'core_elements/_blockquote.scss']),
    Page('Links and Buttons', 'pages/core_elements/links_and_buttons.html', scss=['core_elements/_buttons.scss']),
    Page('Forms', 'pages/core_elements/forms.html'),
    Page('Lists', 'pages/core_elements/lists.html'),
    Page('Images', 'pages/core_elements/images.html'),
    Page('Embedded Media', 'pages/core_elements/embedded_media.html'),
    Page('Themes', 'pages/core_elements/themes.html'),
  ]),
  Page('In Page Components', children=[
    Page('Navigation', children=[
      Page('Tabs', 'pages/components/navigation/tabs.html', scss=['components/navigation/_nav.scss']),
      Page('Pills', 'pages/components/navigation/pills.html', scss=['components/navigation/_nav.scss']),
      Page('Pills (Stacked)', 'pages/components/navigation/pills_stacked.html', scss=['components/navigation/_nav.scss']),
      Page('Stages', 'pages/components/navigation/stages.html', scss=['components/navigation/_nav.scss']),
      Page('Pagination', 'pages/components/navigation/pagination.html', scss=['components/navigation/_pagination.scss']),
      Page('A to Z', 'pages/components/navigation/atoz.html', side_menu=False),
      Page('Search', 'pages/components/navigation/search.html', scss=['components/navigation/_search.scss']),
    ]),
    Page('Content', children=[
      Page('Tables', 'pages/components/content/tables.html', scss=['core_elements/_tables.scss']),
      Page('Collapse', 'pages/components/content/collapse.html', scss=['components/_collapse.scss']),
      Page('Alerts', 'pages/components/content/alerts.html', scss=['components/_alerts.scss']),
      Page('Well', 'pages/components/content/well.html', scss=['components/_well.scss']),
      Page('Date/Time Picker', 'pages/components/content/datetimepicker.html'),
    ]),
    Page('Teasers', 'pages/components/teasers/teasers.html', children=[
      Page('Teaser Examples', 'pages/components/teasers/examples.html', side_menu=False),
    ]),
  ]),
  Page('Templates', children=template_pages),
  Page('Stylesheets', children=scss_pages),
  Page('Scripts', children=coffee_pages)
])

front_page = FrontPage(
  'Home',
  'pages/frontpage.html',
  pages,
)
