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
from quicklinks import QUICKLINKS
from pages import TemplatePage

from git import Repo

repo = Repo(os.getcwd())
base_repo_url = repo.remotes.origin.url
if ':' in base_repo_url:
  base_repo_url = base_repo_url.replace('git@github.com:', 'https://github.com/')
base_repo_url = base_repo_url.replace('.git', '')

base_template_url = '/'.join([base_repo_url, 'tree', repo.active_branch.name, 'templates'])

SITE_NAME = 'CamPL-NG'
CSS_DIST = os.path.join('dist', 'css')
IMG_DIST = os.path.join('dist', 'images')
JS_DIST = os.path.join('dist', 'js')
LP_IMG_DIST = os.path.join('dist', 'lp_img')

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


def clean_dist():
  DIST = 'dist'
  if os.path.exists(DIST):
    shutil.rmtree(DIST)
  os.mkdir(DIST)

  
def make_css(legacy=False):
  if not os.path.exists(CSS_DIST):
    os.makedirs(CSS_DIST)
  call(['sass', '--compass', 'scss/campl.scss', 'dist/css/campl.css'])
  if legacy:
    call(['sass', '--compass', 'scss/campl_legacy.scss', 'dist/css/campl_legacy.css'])
   
def make_img():
  if os.path.exists(IMG_DIST):
    shutil.rmtree(IMG_DIST)
  shutil.copytree('images', IMG_DIST)


def make_js():
  if os.path.exists(JS_DIST):
    shutil.rmtree(JS_DIST)
  os.mkdir(JS_DIST)
  for js in LOCAL_JS:
    shutil.copy(js, os.path.join(JS_DIST, os.path.basename(js)))
  for js in REMOTE_JS:
    urllib.urlretrieve(js, os.path.join(JS_DIST, os.path.basename(js)))
  
def make_html(ROOT_URL=LOCAL_ROOT_URL):

  from jinja2 import FileSystemLoader, Environment
  from site_structure import pages, front_page
  import codecs
    
  if os.path.exists(LP_IMG_DIST):
    shutil.rmtree(LP_IMG_DIST)
  os.mkdir(LP_IMG_DIST)

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
    'TEMPLATE_REPO_ROOT': base_template_url,
    'CACHE_IMAGES': args.cacheimages or args.r,
  })
  

  for page in pages:
    page.render(env)
  
  front_page.render(env)
    

def deploy():
  if args.r:
    if 'html' not in args.mode:
      make_html(REMOTE_ROOT_URL)
    call(['rsync', '-r', 'dist/', REMOTE_RELEASE_DIR])
    make_html(LOCAL_ROOT_URL)
  if os.path.exists(LOCAL_RELEASE_DIR):
    shutil.rmtree(LOCAL_RELEASE_DIR)
  shutil.copytree('dist', LOCAL_RELEASE_DIR)
  
    


parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('-l', action='store_true')
parser.add_argument('-r', action='store_true')
parser.add_argument('--cache-images', dest='cacheimages', action='store_true')
parser.add_argument('mode', nargs='*', default=[])

args = parser.parse_args()

if 'all' in args.mode:
  clean_dist()
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
