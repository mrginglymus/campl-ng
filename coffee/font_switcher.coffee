window.set_font = (font) ->
  Cookies.set 'font', font
  jQuery ($) ->
    $("body").removeClass (index, css) ->
      css.match (/(^|\s)font-\S+/g) || []
        .join ' '
    .addClass "font-#{font}"

  clist = document.body.classList
  if !!clist
    clist.add "font-#{font}"

jQuery ($) ->
  window.fonts = $("a[data-toggle='font']").map ->
    $(@).data 'fontname'
  .get()

  font = Cookies.get "font"
  font = font ? "myriad"
  set_font font
  $("a[data-toggle='font']").click ->
    set_font $(@).data 'fontname'
    false

