import urllib

from jinja2 import contextfunction

from local_settings import LOCAL_RELEASE_DIR

import uuid

import os

from random import random

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