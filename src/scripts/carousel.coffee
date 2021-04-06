jQuery ($) ->
  $('.carousel').hammer().bind 'swipeleft', ->
    $(@).carousel 'next'
  $('.carousel').hammer().bind 'swiperight', ->
    $(@).carousel 'prev'
