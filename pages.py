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
    self.vertical_breadcrumb_siblings = None
    
    
  def update_url(self, root=None, parent=None):
    self.parent = parent
    if root:
      self._url = root + self._url
    for child in self.children:
      child.update_url(self._url, self)
  
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
      return '/'
      
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
  page.update_horizontal_breadcrumb()
  page.update_vertical_breadcrumb()