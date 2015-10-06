Page = require './page.coffee'
Pages = require './pages.coffee'


pages = new Pages(
  new Page('About', 'pages/about.jade'),
  new Page('Page Layouts', null, [
    new Page('Subsection with navigation', 'layouts/page.jade'),
    new Page('Subsection without navigation', 'layouts/page.jade', [], {side_menu:false}),
    new Page('Subsection without right column', 'layouts/page.jade'),
    new Page('App', 'layouts/page.jade', [], {side_menu:false}),
    new Page('Cambridge Front Page', 'layouts/page.jade')
  ]),
  new Page('Core Elements', null, [
    new Page('Typography', 'pages/core_elements/typography.jade'),
    new Page('Links and Buttons', 'pages/core_elements/links_and_buttons.jade'),
    new Page('Forms', 'pages/core_elements/forms.jade'),
    new Page('Lists', 'layouts/page.jade'),
    new Page('Themes', 'layouts/page.jade'),
  ])
  new Page('In Page Components', null, [
    new Page('Navigation', null, [
      new Page('Tabs', 'layouts/page.jade'),
      new Page('Pills', 'layouts/page.jade'),
      new Page('Pills (Stacked)', 'layouts/page.jade'),
      new Page('Stages', 'layouts/page.jade'),
      new Page('Pagination', 'layouts/page.jade'),
      new Page('A to Z', 'layouts/page.jade'),
      new Page('Search', 'layouts/page.jade'),
    ]),
    new Page('Content', null, [
      new Page('Tables', 'layouts/page.jade'),
      new Page('Alerts', 'layouts/page.jade'),
      new Page('Date/Time Picker', 'layouts/page.jade'),
    ]),
    new Page('Teasers', 'layouts/page.jade', [], {side_menu:false}),
  ]),
)

module.exports = pages

###
ages = Pages([
  Page('About', 'demo.html'),
  Page('Page Layouts', 'layouts/overview.html', children=[
    Page('Subsection with navigation', 'layouts/subnav.html'),
    Page('Subsection without navigation', 'layouts/subnonav.html', side_menu=False),
    Page('Subsection without right column', 'layouts/subnocol.html'),
    Page('App', 'layouts/app.html', side_menu=False),
    Page('Cambridge Front Page', 'layouts/campage.html', globals={'CAM_PAGE': True}),
=======
A_TO_Z[0][1] = lipsum(5)
A_TO_Z[0][2] = True


# css pages

def get_directory_structure(rootdir, ext):
  """
  Creates a nested dictionary that represents the folder structure of rootdir
  """
  dir = OrderedDict()
  rootdir = rootdir.rstrip(os.sep)
  start = rootdir.rfind(os.sep) + 1
  for path, dirs, files in os.walk(rootdir):
    folders = path[start:].split(os.sep)
    files = filter(lambda x: x.endswith('.%s'%ext), files)
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

pages = Pages([
  Page('About', 'pages/about.html'),
  Page('Page Layouts', children=[
    Page('App', 'layout/app.html', side_menu=False),
    Page('Cambridge Front Page', 'layout/campage.html', globals={'CAM_PAGE': True}),
>>>>>>> master:site_content/structure.py
  ]),
  Page('Core Elements', children=[
    Page('Typography', 'pages/core_elements/typography.html', scss=['core_elements/_typography.scss', 'core_elements/_blockquote.scss']),
    Page('Links and Buttons', 'pages/core_elements/links_and_buttons.html', scss=['core_elements/_buttons.scss']),
    Page('Forms', 'pages/core_elements/forms.html'),
    Page('Lists', 'pages/core_elements/lists.html'),
    Page('Themes', 'pages/core_elements/themes.html'),
  ]),
  Page('In Page Components', children=[
    Page('Navigation', children=[
      Page('Tabs', 'pages/components/navigation/tabs.html', scss=['components/navigation/_nav.scss']),
      Page('Pills', 'pages/components/navigation/pills.html', scss=['components/navigation/_nav.scss']),
      Page('Pills (Stacked)', 'pages/components/navigation/pills_stacked.html', scss=['components/navigation/_nav.scss']),
      Page('Stages', 'pages/components/navigation/stages.html', scss=['components/navigation/_nav.scss']),
      Page('Pagination', 'pages/components/navigation/pagination.html', scss=['components/navigation/_pagination.scss']),
      Page('A to Z', 'pages/components/navigation/atoz.html', context={'A_TO_Z': A_TO_Z}, side_menu=False),
      Page('Search', 'pages/components/navigation/search.html', scss=['components/navigation/_search.scss']),
    ]),
    Page('Content', children=[
      Page('Tables', 'pages/components/content/tables.html', scss=['components/inpage/_tables.scss']),
      Page('Alerts', 'pages/components/content/alerts.html', scss=['components/inpage/_alerts.scss']),
      Page('Date/Time Picker', 'pages/components/content/datetimepicker.html'),
    ]),
    Page('Teasers', 'pages/components/teasers.html', side_menu=False),
  ]),
  Page('Templates', children=template_pages),
  Page('Stylesheets', children=scss_pages),
])

front_page = FrontPage(
  'Home',
  'pages/frontpage.html',
  pages,
)
###
