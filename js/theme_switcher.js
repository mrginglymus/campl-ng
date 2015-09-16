function set_theme(theme) {
  Cookies.set('theme', theme);
  $('link[href*="campl"][title="'+theme+'"]').prop('disabled', false).prop('enabled', true);
  $('link[href*="campl"]:not([title="'+theme+'"])').prop('disabled', true).prop('enabled', false);
}
theme = Cookies.get('theme');
if (typeof theme === 'undefined'){
  theme = 'turquoise';
}
set_theme(theme);

$(document).ready(function() {
  $('a[data-toggle="theme"]').click(function() {
    set_theme($(this).data('colour'));
  });
});