function set_theme(theme) {
  Cookies.set('theme', theme);
  $('body').removeClass( function(idx, css) {
    console.log(idx);
    console.log(css);
    console.log(css.match(/theme-[a-z]+/));
    return (css.match(/theme-[a-z]+/) || []).join(' ');
  }).addClass('theme-'+theme);
  return false;
}


$(document).ready(function() {
  $('a[data-toggle="theme"]').click(function() {
    set_theme($(this).data('colour'));
  });
  theme = Cookies.get('theme');
  if (typeof theme === 'undefined'){
    theme = 'turquoise';
  }
  set_theme(theme);
});