$(document).ready(function() {
  $('a[href="#global-header-drawer-close"]').click(function() {
    $('#global-header-drawers div.tab-pane.active').removeClass('active');
    $('.global-header a.nav-link.active').removeClass('active');
  });
  
  $('[data-toggle="offcanvas-right"]').click(function(e) {
    e.preventDefault();
    $('.offcanvas').toggleClass('active-right');
  });
  
  $('[data-toggle="offcanvas-left"]').click(function(e) {
    e.preventDefault();
    $('.offcanvas').toggleClass('active-left');
  });
});
