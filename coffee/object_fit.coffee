jQuery ($) ->
  if !Modernizr.objectfit
    $('.image-wrapper').each ->
      $img = $('img', this).hide();
      $('<div>')
        .css "background-image", "url(#{$img.attr('src')})"
        .appendTo $(this)
