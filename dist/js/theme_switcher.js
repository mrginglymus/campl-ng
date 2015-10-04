(function() {
  window.set_theme = function(theme) {
    var clist;
    Cookies.set('theme', theme);
    clist = document.body.classList;
    clist.remove(clist.item(clist.length - 1));
    return clist.add("theme-" + theme);
  };

  $(function() {
    var theme;
    theme = Cookies.get("theme");
    theme = theme != null ? theme : "turquoise";
    set_theme(theme);
    return $("a[data-toggle='theme']").click(function() {
      set_theme($(this).data('colour'));
      return false;
    });
  });

}).call(this);
