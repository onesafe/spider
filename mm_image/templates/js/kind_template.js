jQuery(document).ready(function($) {
    $('.btn_praise').click(function(event) {
        /* Act on the event */
        var $this = $(this);
        // alert($(this).parent().parent().prevAll('.imgs').children().children().attr('src'));
        $.ajax({
            url: 'praise/',
            type: 'POST',
            data: {path: $(this).parent().parent().prevAll('.imgs').children().children().attr('src')},
        })
        .done(function(data) {
            $this.addClass('yizan');
            $this.text("赞一个"+data);
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
        // alert($(this).parent().parent().prevAll('#images').children().children().attr('src'));
        $this = $(this);
        $.ajax({
            url: 'step/',
            type: 'POST',
            data: {path: $(this).parent().parent().prevAll('.imgs').children().children().attr('src')},
        })
        .done(function(data) {
            // console.log(data);
            // console.log($(this).prevAll())
            $this.text("踩你" + data);
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });
        
    });

    $('.view_image_a').click(function(event) {
        /* Act on the event */
        path = $(this).children().attr('src');
        $('.big_image').css({
            'display': 'block'        
        });
        $('body').find('.img_body').attr('src',path);
        $('.big_image_div').css(
            {
                'display': 'block'
            }
        )
    });
    $('.big_image_div').click(function(event) {
        /* Act on the event */
        $(this).parents('body').children('.big_image').css({
            'display': 'none'        
        });
        $('body').children('.big_image').children('.photo_box').children('.imgs').children().attr('src','...');
        $(this).parents('body').children('.big_image_div').css(
            {
                'display': 'none'
            }
        )
    });
    $(".lazy_load").lazy_load()
});