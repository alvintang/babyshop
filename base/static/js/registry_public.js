$(document).ready(function() {

  $('.buy-button').click(function(){
    item_id = $(this).prev().prev().val();
    console.log(item_id);
    item_price = $(this).prev().val();
    console.log(item_price);
    item_name = $(this).siblings('.list-group-item-heading').html()
    console.log(item_name);
    item_qty_left = $(this).siblings('.item_qty_left').val()
    console.log(item_qty);

    $('.item-name').html(item_name);
    $('#item_id').val(item_id);
    $('#item_price').val(item_price);

    $('#item_qty').attr('max',item_qty_left);
  });

    // $('#modal-instructions').modal('show');

});