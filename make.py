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

from site_content.examples import EXAMPLES
from site_content.functions import FUNCTIONS
from site_content.structure import pages, front_page

env = Environment(loader=FileSystemLoader('templates'))

env.globals['SITE_NAME'] = 'CamPL-NG'

env.globals['LOCAL_JS'] = (
  'js/campl.js',
  'js/theme_switcher.js',
)

env.globals['REMOTE_JS'] = (
  'https://code.jquery.com/jquery-1.11.3.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/moment.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/locale/en-gb.js',
  'https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.0.3/js.cookie.js',
  'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.37/js/bootstrap-datetimepicker.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/js/bootstrap.min.js',
)

with open('themes.json') as f:
  env.globals['COLOURS'] = json.loads(f.read(), object_pairs_hook=OrderedDict)

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


