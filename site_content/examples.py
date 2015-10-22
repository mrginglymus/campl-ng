from functions import lipsum, random_image, random_article
from random import random
import string

NAV_ITEMS = [
  {
    'title': 'Active',
    'id': 'tab1',
    'disabled': False,
    'active': True,
    'content': lipsum(2),
  },
  {
    'title': 'Link',
    'id': 'tab2',
    'disabled': False,
    'active': False,
    'content': lipsum(2),
  },
  {
    'title': 'Another Link',
    'id': 'tab3',
    'disabled': False,
    'active': False,
    'content': lipsum(2),
  },
  {
    'title': 'Disabled',
    'disabled': True
  }
]

LOCAL_FOOTER_LINKS = [
  [
    {
      "header": "About the Faculty",
      "links": [
        "Lorem ipsum dolor",
        "Sit amet",
        "Consectetur adipisicing elit",
        "Sed do eiusmod",
        "Tempor Incididunt"
      ]
    },
    {
      "header": "Research",
      "links": [
        "Ut labore et dolore",
        "Ut enim ad minim veniam",
        "Magna aliqua"
      ]
    }
  ],
  [
    {
      "header": "About the University",
      "links": [
        "Quis nostrud exercitation",
        "Ullamco laboris nisi",
        "Ut aliquip ex ea commodo",
        "Duis aute irure dolor"
      ]
    },
    {
      "header": "Libraries & facilities",
      "links": [
        "In reprehenderit in voluptate",
        "Velit esse cillum dolore",
        "Eu fugiat nulla pariatur",
        "Duis aute irure dolor"
      ]
    }
  ],
  [
    {
      "header": "Graduate",
      "links": [
        "Excepteur sint occaecat",
        "Cupidatat non proident"
      ]
    }
  ],
  [
    {
      "header": "Subjects",
      "links": [
        "Sunt in culpa qui officia",
        "Deserunt mollit anim",
        "Id est laborum",
        "Duis aute irure dolor"
      ]
    }
  ]
]

A_TO_Z = list(
  [
    l, lipsum(5) if random() > 0.2 else None, False
  ] for l in string.ascii_uppercase
)

A_TO_Z[0][1] = lipsum(5)
A_TO_Z[0][2] = True

CAROUSEL = [
  (random_article(), random_image(885, 432)),
  (random_article(), random_image(885, 432)),
  (random_article(), random_image(885, 432)),
]

CAMPAGE_CAROUSEL = [
  (random_article(), random_image(785, 428)),
  (random_article(), random_image(785, 428)),
  (random_article(), random_image(785, 428)),
]

VIDEOS = {
  "16by9": "https://www.youtube.com/embed/Nz8gqWsSpm8",
  "4by3": "https://www.youtube.com/embed/8-QNAwUdHUQ",
}

EXAMPLES = {
  'NAV_ITEMS': NAV_ITEMS,
  'LOCAL_FOOTER_LINKS': LOCAL_FOOTER_LINKS,
  'A_TO_Z': A_TO_Z,
  'CAROUSEL': CAROUSEL,
  'CAMPAGE_CAROUSEL': CAMPAGE_CAROUSEL,
  'VIDEOS': VIDEOS,
}
