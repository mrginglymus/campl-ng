if (document.createElement('p').style.objectFit === undefined) {
    $('.image-wrapper').each(function() {
        const $img = $('img', this).hide();
        $(this).css('background-image', `url(${$img.attr('src')})`)
    })
}