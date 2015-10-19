jQuery ($) ->
  if !Modernizr.flexbox
    max_height = Math.max [
      $('.vertical-menu').height() - 50,
      $('.sidebar, .main-content').height()
    ] ...
    $('.vertical-menu').height max_height + 50
    $('.sidebar, .main-content').height max_height
