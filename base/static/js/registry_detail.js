$(document).ready(function() {

  $('.edit-button').click(function(){
    item_id = $(this).prev().prev().val();
    console.log(item_id);
    item_name = $(this).siblings('.list-group-item-heading').html()
    console.log(item_name);

    $('.item-name').html(item_name);
    $('#item_id').val(item_id);
  });

  var url = window.location.href;
  if(url.indexOf('?initial=1') != -1 || url.indexOf('/initial1') != -1) {
      $('#modal-instructions').modal('show');
  }

  $('.delete-button').click(function(e){
    e.preventDefault();

    if(confirm('Are you sure you want to delete this item?')){
      window.location.href = $(this).attr('href');
    }
  });

  $('.bookmarklet').click(function(e){
    e.preventDefault();
  });

  $("#submit_url").submit(function(e){
    var url = $('#url').val();
    console.log(url);

    if(!ValidURL(url)){
      alert("Please enter a valid URL.");
      return false;
    }

    var modal = document.createElement('iframe');
    var reg_id = $('#reg_id').val();
    // var url = encodeURIComponent(window.location.href)
    modal.setAttribute('src', 'https://localhost:8000/external/add/?url='+url+'&reg_id='+reg_id);
    modal.setAttribute('scrolling', 'yes'); // no scroll bars on the iframe please
    modal.className = 'modal';
    modal.id = 'babysetgo-iframe';
    document.body.appendChild(modal);

    $(document).add(parent.document).click(function(e) {
        var iframe = $('iframe');
        if (!iframe.is(e.target) && iframe.has(e.target).length === 0) {
            modal.parentNode.removeChild(modal);
        }
    });

    window.onmessage=function(msg) {
          var fra=document.getElementById("babysetgo-iframe");
          if(msg.data && msg.data.name=="Close" && msg.source==fra.contentWindow) {
              fra.style.display="none";
              }
          };

    return false;
  });

  function ValidURL(str) {
    var pattern = new RegExp('^(https?:\/\/)?'+ // protocol
      '((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|'+ // domain name
      '((\d{1,3}\.){3}\d{1,3}))'+ // OR ip (v4) address
      '(\:\d+)?(\/[-a-z\d%_.~+]*)*'+ // port and path
      '(\?[;&a-z\d%_.~+=-]*)?'+ // query string
      '(\#[-a-z\d_]*)?$','i'); // fragment locater
    if(!pattern.test(str)) {
      // alert("Please enter a valid URL.");
      return false;
    } else {
      return true;
    }
  }
});


