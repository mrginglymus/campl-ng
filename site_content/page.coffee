

class Page
  constructor: (@title, @source=null, @children=[],@side_menu=false) ->
    @type = 'page'
    @horizontal_breadcrumb = []
    @vertical_breadcrumb = []
    @vertical_breadcrumb_parent = null
    @vertical_breadcrumb_children = null
    @vertical_breadcrumb_siblings = []

module.exports = Page