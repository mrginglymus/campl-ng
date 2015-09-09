$(document).ready(function() {
  $('.navbar-local li.nav-item.dropdown').hover(
    function(e) {
      if (!$(e.target).parent().hasClass('open')) {
        $(e.target).dropdown('toggle');
      }
    },
    function(e) {
      if ($(e.target).parent().hasClass('open')) {
        $(e.target).dropdown('toggle');
      }
    }
  );
});