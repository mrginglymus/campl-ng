$("select[data-toggle='tab']").change(function() {
    $(`[href='${$(this).val()}']`).tab('show');
});
