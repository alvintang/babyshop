$(document).ready(function() {
    $(".checkout-remove").click(function(e) {
        e.preventDefault();
        item_qty = $(this).parent().prev().prev().text();
        delete_qty = $(this).siblings('.delete_qty').val();

        if(delete_qty == ''){
            return 1;
        }

        var data = {
            'delete_id': $(this).siblings('.item_id').val(),
            'delete_qty': delete_qty
        };

        // if(delete_qty > item_qty){
        //     alert("Quantity to be removed is less than quantity in cart!")
        // }else{
            $.ajax({
                "type": "POST",
                "url": "/show-cart/",
                "async": "false",
                "data": data,
                "success": function(result) {
                    // console.log(result);
                    location.reload();
                },
            });
        // }
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
