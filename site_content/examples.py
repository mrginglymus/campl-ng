__all__ = ['NAV_ITEMS']

from functions import lipsum

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
