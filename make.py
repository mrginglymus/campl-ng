#!/usr/bin/env python

import os
import shutil
from subprocess import call
import argparse

from local_settings import (
  LOCAL_RELEASE_DIR,
  LOCAL_RELEASE_URL,
  REMOTE_RELEASE_URL,
  REMOTE_RELEASE_DIR,
)
from quicklinks import QUICKLINKS

SITE_NAME = 'CamPL-NG'

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

  
def make_css(colours=['turquoise'], legacy=False):
  if not os.path.exists(CSS_DIST):
    os.makedirs(CSS_DIST)
  for colour in colours:
    call(['sass', '--compass', 'scss/themes/campl_%s.scss'%colour, 'dist/css/campl_%s.css'%colour])
    if legacy:
      call(['sass', '--compass', 'scss/themes/campl_%s_legacy.scss'%colour, 'dist/css/campl_%s_legacy.css'%colour])
   
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
  from site_structure import pages, front_page
  import codecs
  
  env = Environment(loader=FileSystemLoader('templates'))
  
  MEDIA_URL = RELEASE_URL
  
  with codecs.open(os.path.join('dist', 'index.html'), 'wb', 'utf-8') as fh:
    template = env.get_template('index.html')
    fh.write(template.render(ROOT_URL=RELEASE_URL + '/turquoise/'))
  
  for colour in COLOURS:
  
    base_context = {
      'ROOT_URL': RELEASE_URL + '/' + colour,
      'SITE_NAME': SITE_NAME,
      'MEDIA_URL': MEDIA_URL,
      'THEME_VARIANT': colour,
      'JS': JS,
      'MENU': pages,
      'COLOURS': COLOURS,
      'QUICKLINKS': QUICKLINKS,
    }


    for page in pages:
      page.render(base_context, colour)
    
    front_page.render(base_context, colour)

def deploy():
  if args.r:
    if 'html' not in args.mode:
      make_html(REMOTE_RELEASE_URL)
    call(['rsync', '-r', 'dist/', REMOTE_RELEASE_DIR])
    make_html(LOCAL_RELEASE_URL)
  if os.path.exists(LOCAL_RELEASE_DIR):
    shutil.rmtree(LOCAL_RELEASE_DIR)
  shutil.copytree('dist', LOCAL_RELEASE_DIR)
  
    


parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('-l', action='store_true')
parser.add_argument('-r', action='store_true')
parser.add_argument('-a', action='store_true')
parser.add_argument('mode', nargs='*', default=[])

args = parser.parse_args()

if 'all' in args.mode:
  clean_dist()
  make_js()
  make_themes()
  make_img()
  make_html()
  deploy()
  
if 'html' in args.mode:
  if args.r:
    make_html(REMOTE_RELEASE_URL)
  else:
    make_html(LOCAL_RELEASE_URL)

if 'css' in args.mode:
  if args.a:
    make_css(colours=COLOURS, legacy=args.l)
  else:
    make_css(legacy=args.l)
  
if 'js' in args.mode:
  make_js()

if 'img' in args.mode:
  make_img()  

deploy()
