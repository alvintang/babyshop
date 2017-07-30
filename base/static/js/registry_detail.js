$(document).ready(function() {

  $('.edit-button').click(function(){
    item_id = $(this).prev().prev().val();
    console.log(item_id);
    item_name = $(this).siblings('.list-group-item-heading').html()
    console.log(item_name);

    $('.item-name').html(item_name);
    $('#item_id').val(item_id);
  });

});