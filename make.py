#!/usr/bin/env python

import os
import shutil
from subprocess import call

from local_settings import LOCAL_RELEASE_DIR, LOCAL_RELEASE_URL
from quicklinks import QUICKLINKS

SITE_NAME = 'Campl-NG'

JS = (
  ('lib/bootstrap/dist/js/bootstrap.js', 'bootstrap.js'),
  ('lib/datetimepicker/src/js/bootstrap-datetimepicker.js', 'datetimepicker.js'),
  ('js/menu.js', 'menu.js'),
)

COLOURS = [
  'blue',
  'turquoise',
  'purple',
  'green',
  'orange',
  'red',
  'grey',
]
CSS_DIST = os.path.join('dist', 'css')
IMG_DIST = os.path.join('dist', 'img')
JS_DIST = os.path.join('dist', 'js')

def clean_dist():
  DIST = 'dist'
  if os.path.exists(DIST):
    shutil.rmtree(DIST)
  os.mkdir(DIST)


def make_css():

  if not os.path.exists(CSS_DIST):
    os.makedirs(CSS_DIST)
  call(['sass', '--compass', 'scss/themes/campl_turquoise.scss', 'dist/css/campl_turquoise.css'])

def make_themes():

  if not os.path.exists(CSS_DIST):
    os.makedirs(CSS_DIST)
  for colour in COLOURS:
    call(['sass', '--compass', 'scss/themes/campl_%s.scss'%colour, 'dist/css/campl_%s.css'%colour])
   
def make_img():
  if os.path.exists(IMG_DIST):
    shutil.rmtree(IMG_DIST)
  shutil.copytree('img', IMG_DIST)


def make_js():
  if os.path.exists(JS_DIST):
    shutil.rmtree(JS_DIST)
  os.mkdir(JS_DIST)
  for src, dst in JS:
    shutil.copy(src, os.path.join('dist', 'js', dst))
  
def make_html(RELEASE_URL=LOCAL_RELEASE_URL):

  from jinja2 import FileSystemLoader, Environment
  from site_structure import pages
  import codecs
  
  env = Environment(loader=FileSystemLoader('templates'))
  
  HOME_PAGE = 'layouts/frontpage.html'
  
  MEDIA_URL = RELEASE_URL
  
  with codecs.open(os.path.join('dist', 'index.html'), 'wb', 'utf-8') as fh:
    template = env.get_template('index.html')
    fh.write(template.render(ROOT_URL=RELEASE_URL + '/turquoise/'))
  
  for colour in COLOURS:
  
    base_context = {
      'ROOT_URL': RELEASE_URL + '/' + colour,
      'SITE_NAME': SITE_NAME,
      'HOME_PAGE': HOME_PAGE,
      'MEDIA_URL': MEDIA_URL,
      'THEME_VARIANT': colour,
      'JS': JS,
      'MENU': pages,
      'COLOURS': COLOURS,
      'QUICKLINKS': QUICKLINKS,
    }


    for page in pages:
      page.render(base_context, colour)
    
    CAROUSEL = [
      ('carousel-1.png', RELEASE_URL, 'Lorem ipsum'),
      ('carousel-2.png', RELEASE_URL, 'Lorem ipsum'),
      ('carousel-3.png', RELEASE_URL, 'Lorem ipsum'),
    ]
    
    template = env.get_template(HOME_PAGE)
    context = base_context
    context['breadcrumb'] = []
    context['carousel'] = CAROUSEL
    dest = os.path.join('dist', colour, 'index.html')
    with codecs.open(dest, 'wb', 'utf-8') as fh:
      fh.write(template.render(**context))
  

def deploy():
  if os.path.exists(LOCAL_RELEASE_DIR):
    shutil.rmtree(LOCAL_RELEASE_DIR)
  shutil.copytree('dist', LOCAL_RELEASE_DIR)
    
import argparse

parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('mode', nargs='*', default=['all'])

args = parser.parse_args()


if 'all' in args.mode:
  clean_dist()
  make_js()
  make_themes()
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


if 'remote' in args.mode:
  from local_settings import REMOTE_RELEASE_URL, REMOTE_RELEASE_DIR
  make_html(REMOTE_RELEASE_URL)
  from subprocess import call
  call(['rsync', '-r', 'dist/', REMOTE_RELEASE_DIR])
  make_html()
  
if 'deploy' in args.mode:
  deploy()
