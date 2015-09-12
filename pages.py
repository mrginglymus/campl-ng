from jinja2 import FileSystemLoader, Environment
import codecs
import os
env = Environment(loader=FileSystemLoader('templates'))

BASE_BREADCRUMB = [('Campl-NG', '/')]

class Pages(list):
  
  def __init__(self, *args):
    list.__init__(self, *args)
    for page in self:
      page.update_url()
    for page in self:
      page.update_breadcrumbs(self)
    

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
    
  def render(self, base_context, colour):
    if self.source:
      template = env.get_template(self.source)
      context = {}
      context.update(**base_context)
      context['page'] = self
      destination = os.path.join('dist', colour, self.url[1:], 'index.html')
      
      if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
      with codecs.open(destination, 'wb', 'utf-8') as fh:
        fh.write(template.render(**context))
    for child in self.children:
      child.render(base_context, colour)
   
  
  @property
  def destination(self):
    return os.path.join(self.url[1:], 'index.html')
  
  def update_url(self, root=None, parent=None):
    self.parent = parent
    if root:
      self._url = root + self._url
    for child in self.children:
      child.update_url(self._url, self)
  
  def update_breadcrumbs(self, pages, vertical_breadcrumb=BASE_BREADCRUMB, horizontal_breadcrumb=BASE_BREADCRUMB, parent=None):
    if self.source:
      self.horizontal_breadcrumb = horizontal_breadcrumb + [(self.title, self.url)]
    else:
      self.horizontal_breadcrumb = horizontal_breadcrumb + [(self.title, None)]
    self.vertical_breadcrumb = vertical_breadcrumb + [(self.title, self.url)]
    for child in self.children:
      child.update_breadcrumbs(pages, self.vertical_breadcrumb, self.horizontal_breadcrumb, self)
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
      
