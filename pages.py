from jinja2 import FileSystemLoader, Environment
import codecs
import os
env = Environment(loader=FileSystemLoader('templates'))

BASE_BREADCRUMB = [('Campl-NG', '/')]

class Page(object):

  def __init__(self, title, source=None, context={}, children=[]):
    self.title = title
    self.source = source
    self._context = context
    self._url = '/%s' % self.title.lower().replace(' ', '_')
    self.children = children
    self.horizontal_breadcrumb = []
    self.vertical_breadcrumb = []
    self.vertical_breadcrumb_parent = None
    self.vertical_breadcrumb_children = None
    self.vertical_breadcrumb_siblings = []
    
  def render(self, base_context):
    if self.source:
      template = env.get_template(self.source)
      context = {}
      context.update(**base_context)
      context['page'] = self
      if not os.path.exists(os.path.dirname(self.destination)):
        os.makedirs(os.path.dirname(self.destination))
      with codecs.open(self.destination, 'wb', 'utf-8') as fh:
        fh.write(template.render(**context))
    for child in self.children:
      child.render(base_context)
   
  
  @property
  def destination(self):
    return os.path.join('dist', self.url[1:], 'index.html')
  
  def update_url(self, root=None, parent=None):
    self.parent = parent
    if root:
      self._url = root + self._url
    for child in self.children:
      child.update_url(self._url, self)
  
  def update_breadcrumbs(self, vertical_breadcrumb=BASE_BREADCRUMB, horizontal_breadcrumb=BASE_BREADCRUMB, parent=None):
    if self.source:
      self.horizontal_breadcrumb = horizontal_breadcrumb + [(self.title, self.url)]
    else:
      self.horizontal_breadcrumb = horizontal_breadcrumb + [(self.title, None)]
    self.vertical_breadcrumb = vertical_breadcrumb + [(self.title, self.url)]
    for child in self.children:
      child.update_breadcrumbs(self.vertical_breadcrumb, self.horizontal_breadcrumb, self)
    if self.children:
      self.vertical_breadcrumb_parent = self.horizontal_breadcrumb[-1]
      self.vertical_breadcrumb = self.vertical_breadcrumb[:-1]
      self.vertical_breadcrumb_children = [(child.title, child.url) for child in self.children]
      if parent:
        self.vertical_breadcrumb_siblings = [(child.title, child.url) for child in parent.children]
      else:
        self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
    elif not parent:
      self.vertical_breadcrumb = BASE_BREADCRUMB
      self.vertical_breadcrumb_parent = (self.title, self.url)
      self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
    else:
      self.vertical_breadcrumb_parent = self.horizontal_breadcrumb[-2]
      self.vertical_breadcrumb = self.vertical_breadcrumb[:-2]
      if parent:
        self.vertical_breadcrumb_children = [(child.title, child.url) for child in parent.children]
        if parent.parent:
          self.vertical_breadcrumb_siblings = [(child.title, child.url) for child in parent.parent.children]
        else:
           self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
  
  def update_horizontal_breadcrumb(self, breadcrumb=[('Campl-NG', '/')]):
    if self.source:
      self.horizontal_breadcrumb = breadcrumb + [(self.title, self.url)]
    else:
      self.horizontal_breadcrumb = breadcrumb + [(self.title, None)]
    for child in self.children:
      child.update_horizontal_breadcrumb(self.horizontal_breadcrumb)
  
  def update_vertical_breadcrumb(self, breadcrumb=[('Campl-NG', '/')], parent=None):
    self.vertical_breadcrumb = breadcrumb + [(self.title, self.url)]
    for child in self.children:
      child.update_vertical_breadcrumb(self.vertical_breadcrumb, parent=self)
    if self.children:
      self.vertical_breadcrumb_parent = self.vertical_breadcrumb[-1]
      self.vertical_breadcrumb = self.vertical_breadcrumb[:-1]
      self.vertical_breadcrumb_children = [(child.title, child.url) for child in self.children]
      if parent:
        self.vertical_breadcrumb_siblings = [(child.title, child.url) for child in parent.children]
    else:
      self.vertical_breadcrumb_parent = self.vertical_breadcrumb[-2]
      self.vertical_breadcrumb = self.vertical_breadcrumb[:-2]
      if parent:
        self.vertical_breadcrumb_children = [(child.title, child.url) for child in parent.children]
        if parent.parent:
          self.vertical_breadcrumb_siblings = [(child.title, child.url) for child in parent.parent.children]
  
  @property
  def url(self):
    if self.source:
      return self._url
    elif self.children:
      return self.children[0].url
    else:
      return ''
      
  @property
  def context(self):
    return self._context
      
pages = [
  Page('About', 'demo.html', context={'image': 'placeholder.jpg'}),
  Page('Page Layouts', 'layouts/overview.html', children=[
    Page('Subsection with navigation', 'layouts/subnav.html'),
    Page('Subsection without navigation', 'layouts/subnonav.html'),
    Page('Subsection without right column', 'layouts/subnocol.html'),
  ]),
  Page('Core Elements', children=[
    Page('Typography', 'core_elements/typography.html'),
    Page('Links & Buttons', 'core_elements/links_and_buttons.html'),
    Page('Forms', 'core_elements/forms.html'),
    Page('Lists', 'core_elements/lists.html'),
  ]),
  Page('In Page Components', children=[
    Page('Navigation', 'components/inpage/navigation/navigation.html', children=[
      Page('Tables', 'components/inpage/navigation/tables.html'),
      Page('Tabs', 'components/inpage/navigation/tabs.html'),
      Page('Pills', 'components/inpage/navigation/pills.html'),
      Page('Pagination', 'components/inpage/navigation/pagination.html'),
    ]),
    Page('Content', 'components/inpage/content/content.html'),
  ]),
  Page('Themes', children=[
    Page('Blue', 'themes/blue.html', context={'THEME_VARIENT':'blue'}),
    Page('Turqouise', 'themes/turqouise.html', context={'THEME_VARIENT':'turqouise'}),
    Page('Purple', 'themes/purple.html', context={'THEME_VARIENT':'purple'}),
    Page('Green', 'themes/green.html', context={'THEME_VARIENT':'green'}),
    Page('Orange', 'themes/orange.html', context={'THEME_VARIENT':'orange'}),
    Page('Red', 'themes/red.html', context={'THEME_VARIENT':'red'}),
    Page('Grey', 'themes/grey.html', context={'THEME_VARIENT':'grey'}),
  ]),
]
    
    
for page in pages:
  page.update_url()
for page in pages:
  page.update_breadcrumbs()