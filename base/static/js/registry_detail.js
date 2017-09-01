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
});