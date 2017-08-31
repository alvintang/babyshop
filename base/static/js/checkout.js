$(document).ready(function() {

  $('.payment-info-paypal').hide();

  $('input[name="payment_option"]').change(function(){
    option = $(this).val();
    console.log(option);



    if(option == 1){
      $('.payment-info-bank').show();
      $('.payment-info-paypal').hide();
    }else if (option == 2){
      $('.payment-info-bank').hide();
      $('.payment-info-paypal').show();
    }
  });

  $('.checkout-next').click(function(e){
    e.preventDefault();
    $('.payment-options').show();
    $('.checkout-form').hide();
  })

});