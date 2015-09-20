import urllib

from jinja2 import contextfunction

from local_settings import LOCAL_RELEASE_DIR

import uuid

import os

from random import random, randrange

from datetime import timedelta, date

from jinja2.utils import generate_lorem_ipsum as lipsum

@contextfunction
def random_image(context, width, height=None):
  if not height:
    height=width
  scale = random() + 1
  height = int(height*scale)
  width = int(width*scale)
  id = str(uuid.uuid4())
  urllib.urlretrieve("http://lorempixel.com/%s/%s" % (width, height), os.path.join('dist', 'lp_img', id))
  return os.path.join(context['ROOT_URL'], 'lp_img', id)
  

def random_word():
  return lipsum(1, False, 1, 2).rstrip('.')
  
def random_sentence(min=None, max=30):
  if min is None:
    min = int(max * 0.75)-1
  return lipsum(1, False, min, max)
  
def random_date():
  d = date.today() - timedelta(days=randrange(100))
  return d.strftime('%-d %B %Y')