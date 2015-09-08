#!/usr/bin/env python

import os
import shutil

RELEASE_DIR = '/var/www/html/demo/campl-ng'
RELEASE_URL = '/demo/campl-ng'

def make_css():

  from subprocess import call

  call(['sass', 'scss/campl.scss', 'dist/css/campl.css'])

def make_js():

  shutil.copy('lib/bootstrap/dist/js/bootstrap.js', 'dist/js/bootstrap.js')
  
def make_html():

  from jinja2 import FileSystemLoader, Environment

  import codecs

  menu = [
    ('About', 'demo.html'),
    ('Page Layouts', (
      ('Subsection with navigation', 'layouts/subnav.html'),
      ('Subsection without navigation', 'layouts/subnonav.html'),
      ('Subsection without right column', 'layouts/subnocol.html'),
    )),
  ]
  
  base_context = {
    'menu': menu,
    'ROOT_URL': RELEASE_URL,
  }

  env = Environment(loader=FileSystemLoader('templates'))

  def render_node(title, node):
    if not isinstance(node, str):
      for t, n in node:
        render_node(t, n)
    else:
      template = env.get_template(node)
      dest = os.path.join('dist', node)
      if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
      with codecs.open(dest, 'wb', 'utf-8') as fh:
        fh.write(template.render(**base_context))
  
  for title, node in menu:
    render_node(title, node)


def deploy():
  if os.path.exists(RELEASE_DIR):
    shutil.rmtree(RELEASE_DIR)
  shutil.copytree('dist', RELEASE_DIR)
    
import argparse

parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('mode', nargs='*', default=['all'])

args = parser.parse_args()

if 'all' in args:
  make_js()
  make_css()
  make_html()
  deploy()
  
if 'html' in args.mode:
  make_html()

if 'css' in args.mode:
  make_css()

if 'js' in args.mode:
  make_js()
  
if 'deploy' in args.mode:
  deploy()