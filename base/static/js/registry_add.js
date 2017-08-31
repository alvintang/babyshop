$(document).ready(function() {

  // $('#due_date').hide();
  // $('#baby_birthdate').hide();

  $('.buy-button').click(function(){
    item_id = $(this).prev().prev().val();
    console.log(item_id);
    item_price = $(this).prev().val();
    console.log(item_price);
    item_name = $(this).siblings('.list-group-item-heading').html()
    console.log(item_name);

    $('.item-name').html(item_name);
    $('#item_id').val(item_id);
    $('#item_price').val(item_price);
  });

    // $('#modal-instructions').modal('show');

});