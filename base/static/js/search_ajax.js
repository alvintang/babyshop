$(document).ready(function() {
    $.ajaxSetup({ cache: false }); // or iPhones don't get fresh data

    $('.search-loading').hide();

    // $("#search-text").keypress(function(e) {
    //     if(e.which == 13){
    //         e.preventDefault();
    $('#search-button').click(function(e){
            var data = {
                'query': $("#search-text").val()
            };

            $('.search-results').empty();
            $('.search-loading').show();
            $('.search-none').hide();

            $.ajax({
                "type": "POST",
                "dataType": "json",
                "url": "/public/registry/search/",
                "async": "false",
                "data": data,
                "success": function(result) {
                    // console.log(result);
                    $('.search-loading').hide();
                    if(result.length <= 0){
                        $('.search-none').show();
                    }
                    for(i = 0; i<result.length; i++){
                        addToSearchResults(result[i]);
                    }
                },
            });
        // }
    });
});

function addToSearchResults(result){
    // console.log(result['name']);

    var row = document.createElement('div');
    row.className = "list-group-item row";

    var img_separator = document.createElement('div');
    img_separator.className = "img-separator col-md-3";

    var text_separator = document.createElement('div');
    text_separator.className = "text-separator col-md-9";

    var eventName = document.createElement('h3');
    eventName.innerHTML = result['name'];
    var eventDateText = document.createElement('p');
    var eventTimeText = document.createElement('p');
    var eventDate = new Date(result['event_date']);
    eventDateText.innerHTML = eventDate.toDateString();
    eventTimeText.innerHTML = eventDate.toTimeString();
    var eventVenue = document.createElement('p');
    eventVenue.innerHTML = result['event_venue'];

    var id = result['id'];
    var link = '/public/registry/detail/'+id;
    var anchor = document.createElement('a');
    anchor.className = "btn btn-info";
    anchor.href = link;
    anchor.innerHTML = "View Registry";

    text_separator.appendChild(eventName);
    text_separator.appendChild(eventDateText);
    text_separator.appendChild(eventTimeText);
    text_separator.appendChild(eventVenue);
    text_separator.appendChild(anchor);
    // row.append(img_separator);
    row.appendChild(text_separator);

    $('.search-results').append(row);
}

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
