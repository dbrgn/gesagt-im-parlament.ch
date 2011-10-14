$(document).ready(function() {
    $('.person img').each(function() {
        src = $(this).attr('src');
        $(this).attr('src', 'http://mustachify.me/?src=' + src);
    });
})
