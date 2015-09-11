#!/usr/bin/env python

import os
import shutil

from local_settings import RELEASE_DIR, RELEASE_URL

SITE_NAME = 'Campl-NG'

JS = (
  ('lib/bootstrap/dist/js/bootstrap.js', 'bootstrap.js'),
  ('js/menu.js', 'menu.js'),
)

def make_css():

  from subprocess import call

  call(['sass', '--compass', 'scss/campl_turqouise.scss', 'dist/css/campl.css'])

def make_themes():

  from subprocess import call

  COLOURS = [
    'blue',
    'green',
    'grey',
    'orange',
    'purple',
    'red',
    'turqouise',
  ]
  
  for colour in COLOURS:
    call(['sass', '--compass', 'scss/campl_%s.scss'%colour, 'dist/css/campl_%s.css'%colour])
   
    

def make_js():

  for src, dst in JS:
    shutil.copy(src, os.path.join('dist', 'js', dst))
  
def make_html():

  from jinja2 import FileSystemLoader, Environment

  import codecs
  
  HOME_PAGE = 'layouts/frontpage.html'
  
  pages = [
    ('About', 'demo.html', {'image': 'placeholder.jpg'}, None),
    ('Page Layouts', 'layouts/overview.html', None, (
      ('Subsection with navigation', 'layouts/subnav.html', None, None),
      ('Subsection without navigation', 'layouts/subnonav.html', None, None),
      ('Subsection without right column', 'layouts/subnocol.html', None, None),
    )),
    ('Core Elements', None, None, (
      ('Typography', 'core_elements/typography.html', None, None),
      ('Links & Buttons', 'core_elements/links_and_buttons.html', None, None),
      ('Forms', 'core_elements/forms.html', None, None),
      ('Lists', 'core_elements/lists.html', None, None),
    )),
    ('In Page Components', None, None, (
      ('Navigation', 'components/inpage/navigation/navigation.html', None, (
        ('Tables', 'components/inpage/navigation/tables.html', None, None),
        ('Tabs', 'components/inpage/navigation/tabs.html', None, None),
        ('Pills', 'components/inpage/navigation/pills.html', None, None),
        ('Pagination', 'components/inpage/navigation/pagination.html', None, None),
      )),
      ('Content', 'components/inpage/content/content.html', None, None)
    )),
    ('Themes', None, None, (
      ('Blue', 'themes/blue.html', {'THEME_VARIENT':'blue'}, None),
      ('Turqouise', 'themes/turqouise.html', {'THEME_VARIENT':'turqouise'}, None),
      ('Purple', 'themes/purple.html', {'THEME_VARIENT':'purple'}, None),
      ('Green', 'themes/green.html', {'THEME_VARIENT':'green'}, None),
      ('Orange', 'themes/orange.html', {'THEME_VARIENT':'orange'}, None),
      ('Red', 'themes/red.html', {'THEME_VARIENT':'red'}, None),
      ('Grey', 'themes/grey.html', {'THEME_VARIENT':'grey'}, None),
    )),
  ]
  
  base_context = {
    'ROOT_URL': RELEASE_URL,
    'SITE_NAME': SITE_NAME,
    'HOME_PAGE': HOME_PAGE,
    'JS': JS,
    'MENU': pages,
  }

  env = Environment(loader=FileSystemLoader('templates'))
  
  def get_page(page, children):
    if page:
      return page
    elif children:
      return get_page(children)
    else:
      return ''
  
  def render_page(title, page, context, children, breadcrumb, siblings, uncles=None, parent=None, root=False):
    
    breadcrumb.append((title, page, children))
    
    if page:
      template = env.get_template(page)
      context = context or {}
      context.update(base_context)
      context['BREADCRUMB'] = breadcrumb
      context['TITLE'] = title
      
      # work out the side nav
      if root:
        context['SIDE_MENU_PARENT'] = (title, page)
        context['SIDE_MENU_BREADCRUMB'] = []
        context['SIDE_MENU_SIBLINGS'] = siblings
        context['SIDE_MENU_CHILDREN'] = children
      else:
        if children: #ie, it's not a leaf
          context['SIDE_MENU_PARENT'] = (title, page)
          context['SIDE_MENU_CHILDREN'] = children
          context['SIDE_MENU_SIBLINGS'] = siblings
          context['SIDE_MENU_BREADCRUMB'] = breadcrumb[:-1]
        else: # it is a leaf!
          context['SIDE_MENU_PARENT'] = (parent[0], parent[1])
          context['SIDE_MENU_CHILDREN'] = siblings
          context['SIDE_MENU_SIBLINGS'] = uncles
          context['SIDE_MENU_BREADCRUMB'] = breadcrumb[:-2]
      
      dest = os.path.join('dist', page)
      if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
      with codecs.open(dest, 'wb', 'utf-8') as fh:
        fh.write(template.render(**context))
    if children:
      for t, p, c, n in children:
        render_page(t, p, c, n, breadcrumb, siblings=children, uncles=siblings, parent=(title, page))
    breadcrumb.pop()
  
  
  CAROUSEL = [
    ('carousel-1.png', RELEASE_URL, 'Lorem ipsum'),
    ('carousel-2.png', RELEASE_URL, 'Lorem ipsum'),
    ('carousel-3.png', RELEASE_URL, 'Lorem ipsum'),
  ]
  
  template = env.get_template(HOME_PAGE)
  context = base_context
  context['breadcrumb'] = []
  context['carousel'] = CAROUSEL
  dest = os.path.join('dist', 'index.html')
  with codecs.open(dest, 'wb', 'utf-8') as fh:
    fh.write(template.render(**context))
  
  
  for title, page, context, children in pages:
    breadcrumb = []
    render_page(title, page, context, children, breadcrumb, pages, root=True)


def deploy():
  if os.path.exists(RELEASE_DIR):
    shutil.rmtree(RELEASE_DIR)
  shutil.copytree('dist', RELEASE_DIR)
    
import argparse

parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('mode', nargs='*', default=['all'])

args = parser.parse_args()

if 'all' in args.mode:
  make_js()
  make_css()
  make_html()
  deploy()
  
if 'html' in args.mode:
  make_html()
  deploy()

if 'css' in args.mode:
  make_css()
  deploy()

if 'js' in args.mode:
  make_js()
  deploy()

if 'themes' in args.mode:
  make_themes()
  deploy()
  
if 'deploy' in args.mode:
  deploy()
