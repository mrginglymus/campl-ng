BASE_BREADCRUMB = [['Campl-NG', '/']]

jade = require 'jade'
extend = require('util')._extend

class Page
  constructor: (@title, @source=null, @children=[], options={}) ->
    @type = 'page'

    @_url = encodeURIComponent(@title.toLowerCase()) + '/'

    @horizontal_breadcrumb = []
    @vertical_breadcrumb = []
    @vertical_breadcrumb_parent = null
    @vertical_breadcrumb_children = []
    @vertical_breadcrumb_siblings = []

    @side_menu = true
    if 'side_menu' of options
      @side_menu = options.side_menu

  update_url: (parent=null) ->
    if parent
      @_url = parent._url + @_url
    for page in @children
      page.update_url @

  update_breadcrumbs: (pages, vertical_breadcrumb=BASE_BREADCRUMB, horizontal_breadcrumb=BASE_BREADCRUMB, parent=null) ->
    if @source
      @horizontal_breadcrumb = [[@title, @get_url()]]
    else
      @horizontal_breadcrumb = [[@title, null]]
    @horizontal_breadcrumb.unshift horizontal_breadcrumb...

    @vertical_breadcrumb = [[@title, @get_url()]]
    @vertical_breadcrumb.unshift vertical_breadcrumb...

    vertical_breadcrumb_base = @vertical_breadcrumb

    horizontal_breadcrumb_base = @horizontal_breadcrumb

    if @children.length > 0
      @vertical_breadcrumb_parent = @horizontal_breadcrumb[@horizontal_breadcrumb.length - 1]
      @vertical_breadcrumb = @vertical_breadcrumb.slice 0, @vertical_breadcrumb.length - 1
      for child in @children
        @vertical_breadcrumb_children.push [child.title, child.get_url()]
      if parent
        for child in parent.children
          @vertical_breadcrumb_siblings.push [child.title, child.get_url()]
      else
        for page in pages
          @vertical_breadcrumb_siblings.push [page.title, page.get_url()]
    else if not parent
      @vertical_breadcrumb = BASE_BREADCRUMB
      @vertical_breadcrumb_parent = [@title, @get_url()]
      for page in pages
        @vertical_breadcrumb_siblings.push [page.title, page.get_url()]
    else
      @vertical_breadcrumb_parent = @horizontal_breadcrumb[@horizontal_breadcrumb.length - 2]
      @vertical_breadcrumb = @vertical_breadcrumb.slice 0, @vertical_breadcrumb.length - 2
      if parent
        for child in parent.children
          @vertical_breadcrumb_children.push [child.title, child.get_url()]
        @vertical_breadcrumb_siblings = parent.vertical_breadcrumb_siblings

    for child in @children
      child.update_breadcrumbs pages, vertical_breadcrumb_base, horizontal_breadcrumb_base, @

  get_url: ->
    if @source
      return @_url
    else if @children.length > 0
      return @children[0].get_url()
    return ''

  render: (BASE_CONTEXT, grunt) ->
    if @source
      data = extend {page: @}, BASE_CONTEXT
      html = jade.renderFile 'templates-jade/' + @source, data
      dest = "build/" + decodeURIComponent(@get_url()) + 'index.html'
      grunt.file.write dest, html
    for child in @children
      child.render BASE_CONTEXT, grunt


module.exports = Page
###
 
    if self.children:
      self.vertical_breadcrumb_parent = self.horizontal_breadcrumb[-1]
      self.vertical_breadcrumb = self.vertical_breadcrumb[:-1]
      self.vertical_breadcrumb_children = [(child.title, child.url) for child in self.children]
      if parent:
        self.vertical_breadcrumb_siblings = [(child.title, child.url) for child in parent.children]
      else:
        self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
    elif not parent:
      self.vertical_breadcrumb = BASE_BREADCRUMB
      self.vertical_breadcrumb_parent = (self.title, self.url)
      self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
    else:
      self.vertical_breadcrumb_parent = self.horizontal_breadcrumb[-2]
      self.vertical_breadcrumb = self.vertical_breadcrumb[:-2]
      if parent:
        self.vertical_breadcrumb_children = [(child.title, child.url) for child in parent.children]
        if parent.parent:
          self.vertical_breadcrumb_siblings = [(child.title, child.url) for child in parent.parent.children]
        else:
           self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
  
 
###