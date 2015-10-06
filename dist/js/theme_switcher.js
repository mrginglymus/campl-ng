(function() {
  window.set_theme = function(theme) {
    var clist;
    Cookies.set('theme', theme);
    clist = document.body.classList;
    clist.remove(clist.item(clist.length - 1));
    return clist.add("theme-" + theme);
  };

  jQuery(function($) {
    var theme;
    window.themes = $("a[data-toggle='theme']").map(function() {
      return $(this).data('colour');
    }).get();
    theme = Cookies.get("theme");
    theme = theme != null ? theme : "turquoise";
    set_theme(theme);
    $("a[data-toggle='theme']").click(function() {
      set_theme($(this).data('colour'));
      return false;
    });
    return $("a[href='#disco']").click(function() {
      if (window.disco) {
        clearInterval(window.disco);
        window.disco = false;
      } else {
        window.discoidx = -1;
        window.disco = setInterval(function() {
          ++window.discoidx;
          if (window.discoidx >= window.themes.length) {
            window.discoidx = 0;
          }
          return set_theme(window.themes[window.discoidx]);
        }, 500);
      }
      return false;
    });
  });

}).call(this);
