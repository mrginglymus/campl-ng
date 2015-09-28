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
from pages import TemplatePage

from git import Repo

repo = Repo(os.getcwd())
base_repo_url = repo.remotes.origin.url
if ':' in base_repo_url:
  base_repo_url = base_repo_url.replace('git@github.com:', 'https://github.com/')
base_repo_url = base_repo_url.replace('.git', '')

base_template_url = '/'.join([base_repo_url, 'tree', repo.active_branch.name, 'templates'])

SITE_NAME = 'CamPL-NG'

JS = (
  ('lib/bootstrap/dist/js/bootstrap.js', 'bootstrap.js'),
  ('lib/datetimepicker/src/js/bootstrap-datetimepicker.js', 'datetimepicker.js'),
  ('js/menu.js', 'menu.js'),
  ('js/theme_switcher.js', 'theme_switcher.js'),
  ('js/select_tab.js', 'select_tab.js'),
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
CSS_BUILD = os.path.join('build', 'css')
IMG_BUILD = os.path.join('build', 'images')
JS_BUILD = os.path.join('build', 'js')
LP_IMG_BUILD = os.path.join('build', 'lp_img')

def clean_build():
  if os.path.exists('build'):
    shutil.rmtree('build')
  os.mkdir('build')

def clean_dist():
  if os.path.exists('dist'):
    shutil.rmtree('dist')
  os.mkdir('dist')
  
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
  for src, dst in JS:
    shutil.copy(src, os.path.join('build', 'js', dst))
  
def make_html(RELEASE_URL=LOCAL_RELEASE_URL):

  from jinja2 import FileSystemLoader, Environment
  from site_structure import pages, front_page
  import codecs
    
    
  from functions import random_image, random_word, random_sentence, random_date, print_macro
  
  if os.path.exists(LP_IMG_BUILD):
    shutil.rmtree(LP_IMG_BUILD)
  os.mkdir(LP_IMG_BUILD)

  env = Environment(loader=FileSystemLoader('templates'))
  env.globals.update(random_image=random_image)
  env.globals.update(random_word=random_word)
  env.globals.update(random_sentence=random_sentence)
  env.globals.update(random_date=random_date)
  env.globals.update(print_macro=print_macro)
  
  base_context = {
    'ROOT_URL': RELEASE_URL ,
    'SITE_NAME': SITE_NAME,
    'JS': JS,
    'MENU': pages,
    'COLOURS': COLOURS,
    'QUICKLINKS': QUICKLINKS,
    'TEMPLATE_REPO_ROOT': base_template_url,
  }
  
  env.globals.update(**base_context)
  env.globals.update(CACHE_IMAGES = args.cacheimages or args.r)

  for page in pages:
    page.render(env)
  
  front_page.render(env)
    

def deploy():
  if args.r:
    if 'html' not in args.mode:
      make_html(REMOTE_RELEASE_URL)
    call(['rsync', '-r', 'build/', REMOTE_RELEASE_DIR])
    make_html(LOCAL_RELEASE_URL)
  if os.path.exists(LOCAL_RELEASE_DIR):
    shutil.rmtree(LOCAL_RELEASE_DIR)
  shutil.copytree('build', LOCAL_RELEASE_DIR)
  if not os.path.exists(os.path.join('dist', 'css')):
    os.mkdir(os.path.join('dist', 'css'))
  shutil.copy(os.path.join('build', 'css', 'campl.css'), os.path.join('dist', 'css', 'campl.css'))
  if os.path.exists(os.path.join('build', 'css', 'campl_legacy.css')):
    shutil.copy(os.path.join('build', 'css', 'campl_legacy.css'), os.path.join('dist', 'css', 'campl_legacy.css'))
  
    


parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('-l', action='store_true')
parser.add_argument('-r', action='store_true')
parser.add_argument('--cache-images', dest='cacheimages', action='store_true')
parser.add_argument('mode', nargs='*', default=[])

args = parser.parse_args()

if 'all' in args.mode:
  clean_build()
  clean_dist()
  make_js()
  make_css(legacy=args.l)
  make_img()
  make_html()
  
if 'html' in args.mode:
  if args.r:
    make_html(REMOTE_RELEASE_URL)
  else:
    make_html(LOCAL_RELEASE_URL)

if 'css' in args.mode:
  make_css(legacy=args.l)
  
if 'js' in args.mode:
  make_js()

if 'img' in args.mode:
  make_img()  

deploy()
