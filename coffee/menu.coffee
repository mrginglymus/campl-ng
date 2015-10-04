$ ->
  $("a[href='#global-header-drawer-close']").click ->
    $("#global-header-drawers div.tab-pane.active").removeClass "active"
    $(".global-header a.nav-link.active").removeClass "active"

  $("[data-toggle='offcanvas']").click (e) ->
    e.preventDefault()
    $(".offcanvas").toggleClass "active"

  if Cookies.get "mobile_menu_open"
    $("#vertical-navigation").addClass "in"

  $("#vertical-navigation")
    .on "show.bs.collapse", ->
      Cookies.set "mobile_menu_open", true
    .on "hide.bs.collapse", ->
      Cookies.remove "mobile_menu_open"
