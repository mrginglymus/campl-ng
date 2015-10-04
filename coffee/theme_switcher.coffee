
window.set_theme = (theme) ->
  Cookies.set 'theme', theme
  clist = document.body.classList
  clist.remove(clist.item(clist.length-1))
  clist.add "theme-#{theme}"

$ ->
  theme = Cookies.get "theme"
  theme = theme ? "turquoise"
  set_theme theme
  $("a[data-toggle='theme']").click ->
    set_theme $(@).data 'colour'
    false
