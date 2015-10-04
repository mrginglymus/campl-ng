(function() {
  $(function() {
    $("a[href='#global-header-drawer-close']").click(function() {
      $("#global-header-drawers div.tab-pane.active").removeClass("active");
      return $(".global-header a.nav-link.active").removeClass("active");
    });
    $("[data-toggle='offcanvas']").click(function(e) {
      e.preventDefault();
      return $(".offcanvas").toggleClass("active");
    });
    if (Cookies.get("mobile_menu_open")) {
      $("#vertical-navigation").addClass("in");
    }
    return $("#vertical-navigation").on("show.bs.collapse", function() {
      return Cookies.set("mobile_menu_open", true);
    }).on("hide.bs.collapse", function() {
      return Cookies.remove("mobile_menu_open");
    });
  });

}).call(this);

(function() {
  $(function() {
    return $("select[data-toggle='tab']").change(function() {
      return $("[href='" + ($(this).val()) + "']").tab('show');
    });
  });

}).call(this);
