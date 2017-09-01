$(document).ready(function() {

  $('.buy-button').click(function(){
    item_id = $(this).prev().prev().prev().prev().val();
    console.log(item_id);
    item_price = $(this).prev().prev().prev().val();
    console.log(item_price);
    item_name = $(this).siblings('.list-group-item-heading').html()
    console.log(item_name);
    item_qty_left = $(this).siblings('.item_qty_left').val() - $(this).siblings('.item-qty-bought').val()
    console.log(item_qty_left);
    item_img = $(this).siblings('.item-img').val()
    console.log(item_img);
    item_notes = $(this).siblings('.item-notes').val()
    console.log(item_notes);

    $('.item-name').html(item_name);
    $('#item_id').val(item_id);
    $('#modal-price').html("Price: Php "+item_price);
    $('#modal-notes').html("Notes: "+item_notes);
    $('#modal-img').attr('src',item_img);

    $('#item_qty').attr('max',item_qty_left);
  });

    // $('#modal-instructions').modal('show');

});