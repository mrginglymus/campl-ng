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
  CSS_DIST = os.path.join('dist', 'css')
  if os.path.exists(CSS_DIST):
    shutil.rmtree(CSS_DIST)
  os.mkdir(CSS_DIST)
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
   
def make_img():
  IMG_DIST = os.path.join('dist', 'img')
  if os.path.exists(IMG_DIST):
    shutil.rmtree(IMG_DIST)
  shutil.copytree('img', IMG_DIST)
  

def make_js():
  JS_DIST = os.path.join('dist', 'js')
  if os.path.exists(JS_DIST):
    shutil.rmtree(JS_DIST)
  os.mkdir(JS_DIST)
  for src, dst in JS:
    shutil.copy(src, os.path.join('dist', 'js', dst))
  
def make_html():

  from jinja2 import FileSystemLoader, Environment
  from pages import pages
  import codecs
  
  HOME_PAGE = 'layouts/frontpage.html'
  
  base_context = {
    'ROOT_URL': RELEASE_URL,
    'SITE_NAME': SITE_NAME,
    'HOME_PAGE': HOME_PAGE,
    'JS': JS,
    'MENU': pages,
  }

  env = Environment(loader=FileSystemLoader('templates'))

  for page in pages:
    page.render(base_context)
  
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
  

def deploy():
  if os.path.exists(RELEASE_DIR):
    shutil.rmtree(RELEASE_DIR)
  shutil.copytree('dist', RELEASE_DIR)
    
import argparse

parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('mode', nargs='*', default=['all'])

args = parser.parse_args()

if 'clean' in args.mode:
  DIST = 'dist'
  if os.path.exists(DIST):
    shutil.rmtree(DIST)
  os.mkdir(DIST)

if 'all' in args.mode:
  make_js()
  make_css()
  make_img()
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

if 'img' in args.mode:
  make_img()
  deploy()
  
if 'themes' in args.mode:
  make_themes()
  deploy()
  
if 'deploy' in args.mode:
  deploy()

