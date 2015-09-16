function set_theme(theme) {
  Cookies.set('theme', theme);
  clist = document.body.classList;
  clist.remove(clist.item(clist.length-1))
  clist.add('theme-'+theme);
}


$(document).ready(function() {
  theme = Cookies.get('theme');
  if (typeof theme === 'undefined'){
    theme = 'turquoise';
  }
  set_theme(theme);
  $('a[data-toggle="theme"]').click(function() {
    set_theme($(this).data('colour'));
    return false;
  });
});