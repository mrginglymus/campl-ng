window.set_theme = (theme) ->
  Cookies.set 'theme', theme
  jQuery ($) ->
    $("body").removeClass (index, css) ->
      css.match (/(^|\s)theme-\S+/g) || []
        .join ' '
    .addClass "theme-#{theme}"

jQuery ($) ->
  window.themes = $("a[data-toggle='theme']").map ->
    $(@).data 'colour'
  .get()
  window.discoidx = 0

  theme = Cookies.get "theme"
  theme = theme ? "turquoise"
  set_theme theme
  $("a[data-toggle='theme']").click ->
    set_theme $(@).data 'colour'
    false

  $("a[href='#disco']").click ->
    if window.disco
      clearInterval window.disco
      window.disco = false
    else
      window.disco = setInterval ->
        window.discoidx = (window.discoidx + Math.floor(Math.random() * (window.themes.length - 1)) + 1) % window.themes.length
        set_theme window.themes[window.discoidx]
      , 500
    false
