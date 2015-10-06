window.set_theme = (theme) ->
  Cookies.set 'theme', theme
  clist = document.body.classList
  clist.remove(clist.item(clist.length-1))
  clist.add "theme-#{theme}"

jQuery ($) ->
  window.themes = $("a[data-toggle='theme']").map ->
    $(@).data 'colour'
  .get()

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
      window.discoidx = -1
      window.disco = setInterval ->
        ++window.discoidx
        if window.discoidx >= window.themes.length
          window.discoidx = 0
        set_theme window.themes[window.discoidx]
      , 500
    false
