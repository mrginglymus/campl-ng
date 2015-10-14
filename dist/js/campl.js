(function() {
  jQuery(function($) {
    $("#global-header-drawers").on('hidden.bs.collapse', function() {
      $("#global-header-drawers div.tab-pane.active").removeClass("active");
      return $(".global-header a.nav-link.active").removeClass("active");
    });
    $(".global-header [data-parent='#global-header-drawers']").on('shown.bs.tab', function() {
      if (!$("#global-header-drawers").hasClass("in")) {
        return $("#global-header-drawers").collapse("show");
      }
    });
    $(".global-header [data-parent='#global-header-drawers']").click(function() {
      if ($("#global-header-drawers").hasClass("in")) {
        if ($(this).hasClass("active")) {
          return $("#global-header-drawers").collapse("hide");
        }
      }
    });
    $("[data-toggle='offcanvas']").click(function(e) {
      e.preventDefault();
      return $(".offcanvas").toggleClass("active");
    });
    if (Cookies.get("mobile_menu_open")) {
      $("#vertical-menu").addClass("in");
    }
    return $("#vertical-menu").on("show.bs.collapse", function() {
      return Cookies.set("mobile_menu_open", true);
    }).on("hide.bs.collapse", function() {
      return Cookies.remove("mobile_menu_open");
    });
  });

}).call(this);

(function() {
  jQuery(function($) {
    return $("select[data-toggle='tab']").change(function() {
      return $("[href='" + ($(this).val()) + "']").tab('show');
    });
  });

}).call(this);

(function() {
  jQuery(function($) {
    var carousel;
    carousel = new Hammer($('.carousel')[0]);
    carousel.on('swipeleft', function() {
      return $('.carousel').carousel('next');
    });
    return carousel.on('swiperight', function() {
      return $('.carousel').carousel('prev');
    });
  });

}).call(this);
