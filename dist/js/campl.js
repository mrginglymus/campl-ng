$(document).ready(function() {
  $('a[href="#global-header-drawer-close"]').click(function() {
    $('#global-header-drawers div.tab-pane.active').removeClass('active');
    $('.global-header a.nav-link.active').removeClass('active');
  });
  
  $('[data-toggle="offcanvas"]').click(function(e) {
    e.preventDefault();
    $('.offcanvas').toggleClass('active');
  });
  
  if (Cookies.get('mobile_menu_open')) {
    $('#tertiary-navigation').addClass('in');
  }
  
  $('#tertiary-navigation').on('show.bs.collapse', function() {
    Cookies.set('mobile_menu_open', true);
  });
  
  $('#tertiary-navigation').on('hide.bs.collapse', function() {
    Cookies.remove('mobile_menu_open');
  });
  
});

$(document).ready(function() {
  $('select[data-toggle="tab"]').change(function() {
    $('a[href="'+$(this).val()+'"]').tab('show');
  });
});