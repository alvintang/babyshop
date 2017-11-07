$(document).ready(function() {

  $('.payment-info-paypal').hide();

  $('input[name="payment_option"]').change(function(){
    option = $(this).val();
    console.log(option);

    if(option == 1){
      $('.payment-info-bank').show();
      $('.payment-info-paypal').hide();
      $('#submitForm').show();
      $('#total1').show();
      $('#total2').hide();
      $('#convenience_fee').hide();
    }else if (option == 2){
      $('.payment-info-bank').hide();
      $('.payment-info-paypal').show();
      $('#submitForm').hide();
      $('#total2').show();
      $('#total1').hide();
      $('#convenience_fee').show();
    }
  });

});