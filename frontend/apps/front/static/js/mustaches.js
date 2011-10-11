base_uri = 'http://gesagt-im-parlament.ch'

$(document).ready(function() {
    $('.person img').each(function() {
        src = $(this).attr('src');
        $(this).attr('src', 'http://mustachify.me/?src=' + base_uri + src);
    });
})
