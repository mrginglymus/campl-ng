#!/usr/bin/env python

import os
import shutil
import urllib
from subprocess import call
import argparse
import simplejson as json
from ordereddict import OrderedDict
from jinja2 import FileSystemLoader, Environment
import codecs




parser = argparse.ArgumentParser()
parser.add_argument('--photo', dest='photo', action="store_true")

args = parser.parse_args()

env = Environment(loader=FileSystemLoader('templates'))

env.globals['SITE_NAME'] = 'CamPL-NG'

if args.photo:
  IMAGE_SOURCE = "http://loremflickr.com/%s/%s/?user=cambridge%%20university"
else:
  IMAGE_SOURCE = "http://placehold.it/%sx%s"

def main():
  from site_content.examples import EXAMPLES
  from site_content.functions import FUNCTIONS
  from site_content.structure import pages, front_page

  with open('themes.json') as f:
    env.globals['COLOURS'] = json.loads(f.read(), object_pairs_hook=OrderedDict)['themes']

  with open('images.json') as f:
    env.globals['IMAGE_STYLES'] = json.loads(f.read(), object_pairs_hook=OrderedDict)['images']
    
  # add functions
  for f in FUNCTIONS:
    env.globals[f.func_name] = f

  with open('site_content/links.json') as f:
    env.globals['LINKS'] = json.loads(f.read(), object_pairs_hook=OrderedDict)
    
  env.globals['EXAMPLES'] = EXAMPLES

  env.globals['MENU'] = pages

  for page in pages:
    page.render(env)

  front_page.render(env)

if __name__== "__main__":
  main()