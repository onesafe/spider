jQuery(document).ready(function($) {
    $('.btn_praise').click(function(event) {
        /* Act on the event */
        alert($(this).parent().parent().prevAll('#images').children().attr('src'));
        $.ajax({
            url: 'praise/',
            type: 'POST',
            data: {path: $(this).parent().parent().prevAll('#images').children().attr('src')},
        })
        .done(function(data) {
            console.log(data);
            $(this).text(function (i, oldtext) {
                // body...
                console.log(oldtext)
            });
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });
        
    });
    $('.btn_step').click(function(event) {
        /* Act on the event */
        alert($(this).parent().parent().prevAll('#images').children().attr('src'));
        $.ajax({
            url: 'step/',
            type: 'POST',
            data: {path: $(this).parent().parent().prevAll('#images').children().attr('src')},
        })
        .done(function(data) {
            console.log(data);
            console.log($(this).prevAll())
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });
        
    });
});