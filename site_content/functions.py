from jinja2 import contextfunction

import re
import pathlib
import feedparser
import bleach

from random import random, randrange

from datetime import timedelta, date, datetime
from time import mktime

from jinja2.utils import generate_lorem_ipsum as lipsum
from markupsafe import escape

from make import IMAGE_SOURCE

FEED = feedparser.parse('http://www.cam.ac.uk/news/feed?')

def random_image(width, height=None):
  if not height:
    height = width
  scale = random() + 1
  height = int(height * scale)
  scale = random() + 1
  width = int(width * scale)
  return IMAGE_SOURCE % (width, height)


def random_word():
  return lipsum(1, False, 1, 2).rstrip('.')


def random_sentence(min=None, max=30):
  if min is None:
    min = int(max * 0.75) - 1
  return lipsum(1, False, min, max)


def random_article():
  article = FEED['items'][randrange(len(FEED['items']))]
  return {
    'title': article['title'],
    'link': article['links'][0]['href'],
    'body': bleach.clean(
      article['description'],
      strip=True, tags=[]
    ).split('.')[0] + '.',
    'date': datetime.fromtimestamp(mktime(article['published_parsed'])),
  }


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
  res = re.search(
    '({%% macro %s\(.*?{%% endmacro %%})' % macro.name,
    t, re.S
  ).group(1)
  return '<pre><code class="django">%s</code></pre>' % escape(res)


def get_sources_links(page):
  if page.type == 'page':
    return [
      (
        ' > '.join(page.source.split('/')),
        '/templates/%s/' % page.source
      )
    ] + [
      (
        ' > '.join(scss.split('/')),
        '/stylesheets/%s/' % scss
      ) for scss in page.scss
    ]
  return []


FUNCTIONS = [
  random_image,
  random_word,
  random_sentence,
  random_date,
  print_macro,
  get_sources_links,
  random_article,
]
