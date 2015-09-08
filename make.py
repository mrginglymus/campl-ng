#!/usr/bin/env python

import os

def make_css():

  from subprocess import call

  call(['sass', 'scss/campl.scss', 'dist/css/campl.css'])

def make_html():

  from jinja2 import FileSystemLoader, Environment

  import codecs

  env = Environment(loader=FileSystemLoader('templates'))

  template = env.get_template('demo.html')

  build_file = os.path.join('dist', 'demo.html')

  with codecs.open(build_file, 'wb', 'utf-8') as fh:
    fh.write(template.render(**{}))

import argparse

parser = argparse.ArgumentParser(description='Make campl-ng')

parser.add_argument('mode', nargs='?', default='all')

args = parser.parse_args()

if args.mode == 'all':
  make_css()
  make_html()
  
if args.mode == 'html':
  make_html()

if args.mode == 'css':
  make_css()
