jQuery ($) ->
  carousel = new Hammer $('.carousel')[0]
  carousel.on 'swipeleft', ->
    $('.carousel').carousel 'next'
  carousel.on 'swiperight', ->
    $('.carousel').carousel 'prev'