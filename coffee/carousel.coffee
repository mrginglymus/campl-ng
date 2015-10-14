jQuery ($) ->
  $('.carousel').hammer().bind 'swipeleft', ->
    $(this).carousel 'next'
  $('.carousel').hammer().bind 'swiperight', ->
    $(this).carousel 'prev'
