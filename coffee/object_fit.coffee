jQuery ($) ->
  if not Modernizr.objectfit
    $('.image-wrapper').each ->
      $img = $('img', @).hide()
      $(@).css "background-image", "url(#{$img.attr('src')})"
