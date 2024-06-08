function browseDocuments()
{
	$('#openModal').modal('show');
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue; 
} 


$(document).ready(function(){


    $(document).on('click', '.addSelectedDoc', function(){
            var selectedDocuments = [];

            $('.documentsCheckbox:checked').each(function(){
                selectedDocuments.push($(this).val());
            }); 

            console.log("Selected Documents Added: ", selectedDocuments); 
			$('#selectedDocuments').html('<br><b class="text-success">Selected Documents Added:' + selectedDocuments.length + '</b>' + '<input type="hidden" name="selected_documents" value="'+selectedDocuments+'"/>' ); 
			$('#openModal').modal('hide');   
    });


    $(document).on('click', '.corr_opened', function(){
             var corr_map_id = $(this).val();
             var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
             var is_status_type = 'is_opened';
             var is_status_value = 1;
             var data = {
                corr_map_id: corr_map_id,
                is_status_type:is_status_type,
                is_status_value:is_status_value,
                csrfmiddlewaretoken: csrfToken // Include CSRF token in the data
            }; 
            $.ajax({
                url: '/ajax/ajaxCorrespondenceMapIsStatus/', 
                type: 'POST',    
                data: data,
                success: function(res){
                    $(this).prop("disabled", true);  
                },
                error: function(xhr, status, error){
                    console.error(error);
                    // Handle any errors that occur during the AJAX request
                } 
            });   
        });


        // $('.department-select').change(function(){  
        //     var department_id = $(this).val();
        //     var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Retrieve CSRF token value
        //     var data = {
        //         department_id: department_id,
        //         csrfmiddlewaretoken: csrfToken // Include CSRF token in the data
        //     }; 
        //     console.log(data);   
        //     $.ajax({
        //         url: '/ajax/ajaxGetSubDepartment/', 
        //         type: 'POST',    
        //         data: data,
        //         success: function(res){
        //             console.log(res); 
        //             // Clear existing options in the select element
        //             $('.sub-department-select').empty();
                    
        //             // Append new options based on the AJAX response 
        //             $.each(res, function(index, sub_departments) { 
        //                 $('.sub-department-select').append('<option value="' + sub_departments.id + '">' + sub_departments.name.toUpperCase() + '</option>');
        //             });

                    
        //         },
        //         error: function(xhr, status, error){
        //             console.error(error);
        //             // Handle any errors that occur during the AJAX request
        //         } 
        //     }); 
        //     $.ajax({
        //         url: '/ajax/ajaxGetDepartmentRoles/',  
        //         type: 'POST',      
        //         data: data, 
        //         success: function(res2){
        //             console.log(res2); 
        //             // Clear existing options in the select element
        //             $('.department-roles').empty(); 
                    
        //             // Append new options based on the AJAX response  
        //             $.each(res2, function(index, sub_department_role) { 
        //                 $('.department-roles').append('<option value="' + sub_department_role.role_id + '">' + sub_department_role.role_name + '</option>'); 
        //             });
        //         },
        //         error: function(xhr, status, error){
        //             console.error(error); 
        //             // Handle any errors that occur during the AJAX request
        //         }
        //     });
        // });  



         $('.selected_role').change(function(){   
            var role_id = $(this).val();
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Retrieve CSRF token value
            var data = {
                role_id: role_id,
                csrfmiddlewaretoken: csrfToken // Include CSRF token in the data
            }; 
            console.log(data);   
            $.ajax({
                url: '/ajax/ajaxGetRoleUsers/', 
                type: 'POST',    
                data: data,
                success: function(res){
                    console.log(res);    
                    // Clear existing options in the select element
                    $('.selected-roles-users').empty(); 
                    
                    // Append new options based on the AJAX response 
                    $.each(res, function(index, user) { 
                        $('.selected-roles-users').append('<option value="' + user.user_id + '">' + user.username.toUpperCase() + ' - ' + user.full_name.toUpperCase() + '</option>');
                    }); 

                    
                },
                error: function(xhr, status, error){
                    console.error(error);
                    // Handle any errors that occur during the AJAX request
                } 
            }); 
        });


        $('.message_note').click(function(){
           var txt = $(this).attr('data-msg');
          
           $('#openModal').modal('show');
           $('.showMsg').html(txt); 
       });

      $('.changePassPopup').click(function(){
           
           $('#openModal').modal('show');
       });



       $('.submitPassword').click(function(){
           
            var password = $('.passwordTxt').val();
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Retrieve CSRF token value
            var data = {
                password: password,
                csrfmiddlewaretoken: csrfToken // Include CSRF token in the data
            };
            if(password == "" || password == null)
            {
               $('.password-change').html('<b class="text-danger">' + res.error + '</b>'); 
           }else{
                  $.ajax({
                        url: '/ajax/ajaxChangeUserPassword/',
                        type: 'POST', 
                        data: data,
                        success: function(res) {
                            if (res.success) {
                                $('.password-change').html('<b class="text-success">' + res.success + '</b>');
                            } else if (res.error) {
                                $('.password-change').html('<b class="text-danger">' + res.error + '</b>');
                            }
                            $('.passwordTxt').val('');
                        },
                        error: function(xhr, status, error) {
                            console.error(error);
                            // Display a generic error message in case of failure
                            $('.password-change').html('<b class="text-danger">Error changing password. Please try again.</b>');
                        }
                 }); 
            } 
       });


});

