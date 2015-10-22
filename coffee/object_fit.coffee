jQuery ($) ->
  if !Modernizr.objectfit
    $('.image-wrapper').each ->
      $img = $('img', this).hide()
      $(this).css "background-image", "url(#{$img.attr('src')})"
