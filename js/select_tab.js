$(document).ready(function() {
  $('select[data-toggle="tab"]').change(function() {
    $('a[href="'+$(this).val()+'"]').tab('show');
  });
});