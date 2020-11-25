
"use strict";

const button = $('#user_form');

button.on('click', () => {
    $('#create_user').show();
    
});


$('#create_user').on('submit', (evt) => {
    
    evt.preventDefault();
    // serialize --- changes form to js object that can be used in Ajax
    const formUser = $('#create_user').serialize();

    $.post('/create_user', formUser, (res) => {

        if(res === '1'){
            
            alert('A user account with the same email exists. Log in using your email or try with different email!');
            
            
        } else if (res === '2'){
            
            alert('Account successfuly created. Please Log In');
            // TODO reset or clear form
            $('#create_user')[0].reset();
            $('#create_user').hide();

        }

        // alert(res);

    });

});