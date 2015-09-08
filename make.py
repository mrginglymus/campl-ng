#!/usr/bin/env python

import os
import shutil

from local_settings import RELEASE_DIR, RELEASE_URL

SITE_NAME = 'Campl-NG'

def make_css():

  from subprocess import call

  call(['sass', 'scss/campl.scss', 'dist/css/campl.css'])

def make_js():

  shutil.copy('lib/bootstrap/dist/js/bootstrap.js', 'dist/js/bootstrap.js')
  
def make_html():

  from jinja2 import FileSystemLoader, Environment

  import codecs

  menu = [
    ('About', 'demo.html', None),
    ('Page Layouts', 'layouts/overview.html', (
      ('Subsection with navigation', 'layouts/subnav.html', None),
      ('Subsection without navigation', 'layouts/subnonav.html', None),
      ('Subsection without right column', 'layouts/subnocol.html', None),
    )),
    ('Core Elements', None, (
      ('Typography', 'core_elements/typography.html', None),
      ('Links & Buttons', 'core_elements/links_and_buttons.html', None),
      ('Forms', 'core_elements/forms.html', None),
      ('Lists', 'core_elements/lists.html', None),
    )),
  ]
  
  base_context = {
    'menu': menu,
    'ROOT_URL': RELEASE_URL,
    'SITE_NAME': SITE_NAME,
  }

  env = Environment(loader=FileSystemLoader('templates'))
  
  def render_node(title, page, node, breadcrumb):
    breadcrumb.append((title, page, node))
    if page:
      template = env.get_template(page)
      context = base_context
      context['breadcrumb'] = breadcrumb
      context['title'] = title
      dest = os.path.join('dist', page)
      if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
      with codecs.open(dest, 'wb', 'utf-8') as fh:
        fh.write(template.render(**base_context))
    if node:
      for t, n, p in node:
        render_node(t, n, p, breadcrumb)
    breadcrumb.pop()
  
  
  
  
  for title, page, node in menu:
    breadcrumb = []
    render_node(title, page, node, breadcrumb)


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
