$ ->
  $("select[data-toggle='tab']").change ->
    $("[href='#{$(@).val()}']").tab 'show'