$( document ).ready(function() {

  // Edit Button
  $('#edit_btn').click( function(){
    $('.edit_text').toggle();
    $('.edit_input').toggle();
    $('#edit_submit').toggle();
  });

  // Cancel
  $('#cancel_btn').click( function(){
    $('.edit_text').toggle();
    $('.edit_input').toggle();
    $('#edit_submit').toggle();
  });    
  
  //Save Button
  $('#save_btn').click( function() {
    edit_type = 'company';
    data = {}
    $('.edit_input').each( function() {
      data[ $(this).attr('name') ] = $(this).attr('value');
    });
    console.log( data );
    $.ajax({
      type : 'POST',
      url  : '/admin/edit_ajax/' + edit_type,
      data : data,
      success: function( result ){
        alert( result );
        $('.edit_text').toggle();
        $('.edit_input').toggle();
        $('#edit_submit').toggle();          
      }
    });
  });

});