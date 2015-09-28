import urllib

from jinja2 import contextfunction

from local_settings import LOCAL_RELEASE_DIR

import uuid
import re
import os
import pathlib

from random import random, randrange

from datetime import timedelta, date

from jinja2.utils import generate_lorem_ipsum as lipsum
from markupsafe import escape

__all__ = ['random_image', 'random_word', 'random_sentence', 'random_date', 'print_macro', 'get_sources_links']

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
    urllib.urlretrieve(lploc, os.path.join('dist', 'lp_img', id))
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
  p = pathlib.Path(macro._func.func_code.co_filename)
  env = context.environment
  t = env.loader.get_source(env, str(p.relative_to(*p.parts[:1])))[0]
  res = re.search('({%% macro %s\(.*?{%% endmacro %%})'%macro.name, t, re.S).group(1)
  return '<pre><code class="django">%s</code></pre>' % escape(res)
  
@contextfunction
def get_sources_links(context, page):
  if page.type=='page':
    return [(' > '.join(page.source.split('/')), '%s/templates/%s/'%(context['ROOT_URL'], page.source))] + [
      (' > '.join(scss.split('/')), '%s/stylesheets/%s/'%(context['ROOT_URL'], scss)) for scss in page.scss
    ]
  return []