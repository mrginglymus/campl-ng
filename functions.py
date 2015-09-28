import urllib

from jinja2 import contextfunction

from local_settings import LOCAL_RELEASE_DIR

import uuid
import re
import os

from random import random, randrange

from datetime import timedelta, date

from jinja2.utils import generate_lorem_ipsum as lipsum
from markupsafe import escape

@contextfunction
def random_image(context, width, height=None):
  if not height:
    height=width
  scale = random() + 1
  height = int(height*scale)
  width = int(width*scale)
  lploc = "http://lorempixel.com/%s/%s" % (width, height)
  if context['CACHE_IMAGES']:
    id = str(uuid.uuid4())
    urllib.urlretrieve(lploc, os.path.join('build', 'lp_img', id))
    return os.path.join(context['ROOT_URL'], 'lp_img', id)
  else:
    return lploc
  

def random_word():
  return lipsum(1, False, 1, 2).rstrip('.')
  
def random_sentence(min=None, max=30):
  if min is None:
    min = int(max * 0.75)-1
  return lipsum(1, False, min, max)
  
def random_date(raw=False):
  d = date.today() - timedelta(days=randrange(100))
  if raw:
    return d
  return d.strftime('%-d %B %Y')
  
@contextfunction
def print_macro(context, macro):
  env = context.environment
  t = env.loader.get_source(env, context.name)[0]
  res = re.search('({%% macro %s\(.*?{%% endmacro %%})'%macro.name, t, re.S).group(1)
  return escape(res)
