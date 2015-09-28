#!/usr/bin/env python

import os
import shutil
import urllib
from subprocess import call
import argparse

from local_settings import (
  LOCAL_RELEASE_DIR,
  LOCAL_ROOT_URL,
  REMOTE_ROOT_URL,
  REMOTE_RELEASE_DIR,
)

SITE_NAME = 'CamPL-NG'

LOCAL_JS = (
  'lib/bootstrap/dist/js/bootstrap.js',
  'lib/datetimepicker/src/js/bootstrap-datetimepicker.js',
  'js/menu.js',
  'js/theme_switcher.js',
  'js/select_tab.js',
)

REMOTE_JS = (
  'https://code.jquery.com/jquery-1.11.3.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/moment.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/locale/en-gb.js',
  'https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.0.3/js.cookie.js',
)

JS = [os.path.basename(js) for js in REMOTE_JS + LOCAL_JS]

COLOURS = [
  'blue',
  'turquoise',
  'purple',
  'green',
  'orange',
  'red',
  'grey',
]

CSS_BUILD = os.path.join('build', 'css')
IMG_BUILD = os.path.join('build', 'images')
JS_BUILD = os.path.join('build', 'js')
LP_IMG_BUILD = os.path.join('build', 'lp_img')


def clean_build():
  if os.path.exists('build'):
    shutil.rmtree('build')
  os.mkdir('build')

def make_dist():
  if os.path.exists('dist'):
    shutil.rmtree('dist')
  os.mkdir('dist')
  make_css(True)
  if not os.path.exists(os.path.join('dist', 'css')):
    os.mkdir(os.path.join('dist', 'css'))
  shutil.copy(os.path.join('build', 'css', 'campl.css'), os.path.join('dist', 'css', 'campl.css'))
  if os.path.exists(os.path.join('build', 'css', 'campl_legacy.css')):
    shutil.copy(os.path.join('build', 'css', 'campl_legacy.css'), os.path.join('dist', 'css', 'campl_legacy.css'))
  
def make_css(legacy=False):
  if not os.path.exists(CSS_BUILD):
    os.makedirs(CSS_BUILD)
  call(['sass', '--compass', 'scss/campl.scss', 'build/css/campl.css'])
  if legacy:
    call(['sass', '--compass', 'scss/campl_legacy.scss', 'build/css/campl_legacy.css'])
   
def make_img():
  if os.path.exists(IMG_BUILD):
    shutil.rmtree(IMG_BUILD)
  shutil.copytree('images', IMG_BUILD)


def make_js():
  if os.path.exists(JS_BUILD):
    shutil.rmtree(JS_BUILD)
  os.mkdir(JS_BUILD)
  for js in LOCAL_JS:
    shutil.copy(js, os.path.join(JS_BUILD, os.path.basename(js)))
  for js in REMOTE_JS:
    urllib.urlretrieve(js, os.path.join(JS_BUILD, os.path.basename(js)))

  
def make_html(ROOT_URL=LOCAL_ROOT_URL):

  from jinja2 import FileSystemLoader, Environment
  from site_structure import pages, front_page
  import codecs
    

  if os.path.exists(LP_IMG_BUILD):
    shutil.rmtree(LP_IMG_BUILD)
  os.mkdir(LP_IMG_BUILD)

  env = Environment(loader=FileSystemLoader('templates'))
  
  import functions
  
  # add functions
  for fname in functions.__all__:
    env.globals.update(**{fname:functions.__dict__[fname]})
  
  import links
  
  # add links
  for lname in links.__all__:
    env.globals.update(**{lname:links.__dict__[lname]})
  
  env.globals.update(**{
    'ROOT_URL': ROOT_URL ,
    'SITE_NAME': SITE_NAME,
    'JS': JS,
    'MENU': pages,
    'COLOURS': COLOURS,
    'CACHE_IMAGES': args.cacheimages or args.r,
  })
  

  for page in pages:
    page.render(env)
  
  front_page.render(env)
    

def deploy():
  if args.r:
    if 'html' not in args.mode:
      make_html(REMOTE_ROOT_URL)
    call(['rsync', '-r', 'build/', REMOTE_RELEASE_DIR])
    make_html(LOCAL_ROOT_URL)
  if os.path.exists(LOCAL_RELEASE_DIR):
    shutil.rmtree(LOCAL_RELEASE_DIR)
  shutil.copytree('build', LOCAL_RELEASE_DIR)
  

parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('-l', action='store_true')
parser.add_argument('-r', action='store_true')
parser.add_argument('--cache-images', dest='cacheimages', action='store_true')
parser.add_argument('mode', nargs='*', default=[])

args = parser.parse_args()

if 'all' in args.mode:
  clean_build()
  make_js()
  make_css(legacy=args.l)
  make_img()
  make_html()
  
if 'html' in args.mode:
  if args.r:
    make_html(REMOTE_ROOT_URL)
  else:
    make_html(LOCAL_ROOT_URL)

if 'css' in args.mode:
  make_css(legacy=args.l)
  
if 'js' in args.mode:
  make_js()

if 'img' in args.mode:
  make_img()  

deploy()

if 'dist' in args.mode:
  make_dist()
