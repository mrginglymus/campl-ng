$(document).ready(function() {
  $('a[href="#global-header-drawer-close"]').click(function() {
    $('#global-header-drawers div.tab-pane.active').removeClass('active');
    $('.navbar-global a.nav-link.active').removeClass('active');
  });
  
  $('[data-toggle="offcanvas"]').click(function(e) {
    e.preventDefault();
    $('.offcanvas').toggleClass('active');
  });
});
