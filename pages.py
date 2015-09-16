from jinja2 import FileSystemLoader, Environment, meta
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

  
TEMPLATE_REFERENCES = {}

REFERENCING_TEMPLATES = {}

TEMPLATE_PAGES = []

def template_to_tuple(templates, root_url):
  return [
    (
      ' > '.join(t.split('/')),
      '%s/templates/%s' % (root_url, t)
    ) for t in templates
  ]

for template_name in env.list_templates():
  if template_name != 'template.html':
    refs = list(meta.find_referenced_templates(env.parse(env.loader.get_source(env, template_name)[0])))
    TEMPLATE_REFERENCES[template_name] = refs
    for ref in refs:
      REFERENCING_TEMPLATES.setdefault(ref, []).append(template_name)

class XTemplatePage(object):
  def __init__(self, template_name):
    self.title = template_name.split('/')[-1]
    self.source = template_name
    self.url = 'templates/' + template_name
    self.children = []
    self.horizontal_breadcrumb = BASE_BREADCRUMB + [('Templates', None)] + [(t.replace('_', ' ').title(), None) for t in self.source.split('/')[:-1]] + [(self.title, None)]
    self.vertical_breadcrumb = []
    self.vertical_breadcrumb_parent = None
    self.vertical_breadcrumb_children = None
    self.vertical_breadcrumb_siblings = []
    self.front_page=False
    
  def render(self, base_context):
    template = env.get_template('template.html')
    context = {
      'page': self,
      'template': env.loader.get_source(env, self.source)[0],
      'template_references': template_to_tuple(TEMPLATE_REFERENCES.get(self.source, []), base_context['ROOT_URL']),
      'referencing_templates': template_to_tuple(REFERENCING_TEMPLATES.get(self.source, []), base_context['ROOT_URL']),
    }
    context.update(**base_context)
    destination = os.path.join('dist', self.url)
    
    if not os.path.exists(os.path.dirname(destination)):
      os.makedirs(os.path.dirname(destination))
    with codecs.open(destination, 'wb', 'utf-8') as fh:
      fh.write(template.render(**context))
    

class Page(object):

  def __init__(self, title, source=None, context={}, children=[], front_page=False):
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
    self.front_page=front_page
            
    
  def render(self, base_context):
    if self.source:
      template = env.get_template(self.source)
      context = self.context
      context.update(**base_context)
      context['page'] = self
      destination = os.path.join('dist', self.url[1:], 'index.html')
      
      if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
      with codecs.open(destination, 'wb', 'utf-8') as fh:
        fh.write(template.render(**context))
    for child in self.children:
      child.render(base_context)
   
  
  @property
  def destination(self):
    if self.front_page:
      return 'index.html'
    else:
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
    if self.front_page:
      return ''
    elif self.source:
      return self._url
    elif self.children:
      return self.children[0].url
    else:
      return ''
      
  @property
  def context(self):
    return self._context

class SCSSPage(Page):

  def render(self, base_context):
    if self.source:
      with open(os.path.join('scss', *self.url.split('/')[2:]), 'r') as scss_file:
        scss = scss_file.read()
      template = env.get_template('meta/stylesheet.html')
      context = {
        'page': self,
        'scss': scss,
      }
      context.update(**base_context)
      destination = os.path.join('dist', self.url[1:], 'index.html')
      if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
      with codecs.open(destination, 'wb', 'utf-8') as fh:
        fh.write(template.render(**context))
    for child in self.children:
      child.render(base_context)
 

class TemplatePage(Page):
     
    
  def render(self, base_context):
    if self.source:
      template = env.get_template('meta/template.html')
      template_file = os.path.join(*self.url.split('/')[2:])
      context = {
        'page': self,
        'template': env.loader.get_source(env, template_file)[0],
        'template_references': template_to_tuple(TEMPLATE_REFERENCES.get(template_file, []), base_context['ROOT_URL']),
        'referencing_templates': template_to_tuple(REFERENCING_TEMPLATES.get(template_file, []), base_context['ROOT_URL']),
      }
      context.update(**base_context)
      destination = os.path.join('dist', self.url[1:], 'index.html')
    
      if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
      with codecs.open(destination, 'wb', 'utf-8') as fh:
        fh.write(template.render(**context))
    for child in self.children:
      child.render(base_context)
    
    