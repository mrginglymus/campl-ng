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

  call(['sass', '--compass', 'scss/campl.scss', 'dist/css/campl.css'])

def make_js():

  for src, dst in JS:
    shutil.copy(src, os.path.join('dist', 'js', dst))
  
def make_html():

  from jinja2 import FileSystemLoader, Environment

  import codecs
  
  HOME_PAGE = 'layouts/frontpage.html'
  
  menu = [
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
      ('Tables', 'components/inpage/tables.html', None, None),
      ('Tabs', 'components/inpage/tabs.html', None, None),
      ('Pills', 'components/inpage/pills.html', None, None),
    )),
  ]
  
  base_context = {
    'menu': menu,
    'ROOT_URL': RELEASE_URL,
    'SITE_NAME': SITE_NAME,
    'HOME_PAGE': HOME_PAGE,
    'JS': JS,
  }

  env = Environment(loader=FileSystemLoader('templates'))
  
  def render_node(title, page, context, node, breadcrumb):
    breadcrumb.append((title, page, node))
    if page:
      template = env.get_template(page)
      context = context or {}
      context.update(base_context)
      context['breadcrumb'] = breadcrumb
      context['title'] = title
      dest = os.path.join('dist', page)
      if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
      with codecs.open(dest, 'wb', 'utf-8') as fh:
        fh.write(template.render(**context))
    if node:
      for t, p, c, n in node:
        render_node(t, p, c, n, breadcrumb)
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
  
  
  for title, page, context, node in menu:
    breadcrumb = []
    render_node(title, page, context, node, breadcrumb)


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
  
if 'deploy' in args.mode:
  deploy()
