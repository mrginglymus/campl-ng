import Cookies from 'js-cookie';

$("#global-header-drawers").on('hidden.bs.collapse', () => {
    $("#global-header-drawers div.tab-pane.active").removeClass
    "active"
    $(".global-header a.nav-link.active").removeClass
    "active"
});

$(".global-header [data-parent='#global-header-drawers']").on('shown.bs.tab', () => {
    if (!$("#global-header-drawers").hasClass("in")) {
        $("#global-header-drawers").collapse("show")
    }
});

$(".global-header [data-parent='#global-header-drawers']").click(() => {
    if ($("#global-header-drawers").hasClass("in")) {
        if ($(this).hasClass("active")) {
            $("#global-header-drawers").collapse("hide")
        }
    }
});

$("[data-toggle='offcanvas']").click(e => {
    e.preventDefault()
    $(".offcanvas").toggleClass("active")
});


if (Cookies.get("mobile_menu_open")) {
    $("#vertical-menu").addClass("in");
}

$("#vertical-menu").on("show.bs.collapse", () => {
    Cookies.set("mobile_menu_open", true)
}).on("hide.bs.collapse", () => {
    Cookies.remove("mobile_menu_open")
});
