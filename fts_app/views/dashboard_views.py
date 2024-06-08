from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, CorrespondenceUserMap, Correspondence
from django.core.exceptions import ValidationError  
from django.utils import timezone
from django.contrib import messages
import os
from .helpers.common_helper import download_file
from .decorators import check_session_exists 
from django.db.models import F  
from django.conf import settings




@check_session_exists
def index(request):
   return HttpResponse("Hello")
    




@check_session_exists
def dakghar(request): 
    if request.method == 'POST':
        ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'png', 'jpg']
        if 'uploadfile' in request.FILES:
            upload_file = request.FILES['uploadfile']
            title = request.POST.get('title')
            user_id = request.session.get('user_id')

            # Get the file extension
            file_extension = upload_file.name.split('.')[-1].lower()

            # Check if the file extension is allowed
            if file_extension not in ALLOWED_EXTENSIONS:
                # Return a bad request response with an error message
                error_message = 'Unknown file format. Only PDF, DOC, DOCX, PNG, and JPG files are allowed.'
                messages.error(request, error_message)
                return redirect('dashboard-dakghar')
            try:
                filename = f"{timezone.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
                fs = FileSystemStorage()
                filename = fs.save(filename, upload_file)

                # Create a StoreDocument object to store metadata about the uploaded file
                document = StoreDocument.objects.create(title=title, filename=filename, user_id=user_id)

                # Redirect to a success page or perform any additional actions
                return redirect('dashboard-dakghar-documents')

            except ValidationError:
                # Handle validation errors
                messages.error(request, 'Error occurred while uploading the file.')
                return redirect('dashboard-dakghar')
        else:
            # No file was uploaded
            messages.error(request, 'Please select a file to upload.')
            return redirect('dashboard-dakghar')

    data = {'section' : "upload_form"}
    return render(request, 'dakghar.html', data)






@check_session_exists
def dakghar_documents(request):
    uid = request.session.get('user_id')
    role = request.session.get('role')

    documents = StoreDocument.objects.filter().order_by('-pk') 

    data = {
        'section': "dakghar_documents",
        'documents': documents
    }
    return render(request, 'dakghar.html', data)





@check_session_exists
def dakghar_documents_forward(request, doc_id): 
    documents = StoreDocument.objects.filter(id=doc_id).order_by('-pk') if doc_id else None
    
    if request.method == 'POST':
        role_ids = request.POST.getlist('sentTo[]')
        users = User.objects.filter(user_role_maps__role__id__in=role_ids)
        note_msg = request.POST.get('note_msg')
        sender_id = request.session.get('user_id')
        sender_email = User.objects.get(id=sender_id).email if sender_id else ''

        for user in users:
            to_email = user.email
            msg = Message(
                from_email=sender_email,
                to_email=to_email,
                message=note_msg,
                status=1,
                from_user_id=sender_id,
                to_user_id=user.id,
                document_id=doc_id  
            )
            msg.save() 

        StoreDocument.objects.filter(id=doc_id).update(status=2)
        messages.success(request, 'Messages sent successfully!')

    roles = Role.objects.filter(role_name__in=['admin','gms','gm'])   
    data = {'section': 'dakghar_documents_forward', 'documents': documents, 'roles': roles, 'doc_id': doc_id} 
    return render(request, 'dakghar.html', data)






@check_session_exists
def dakghar_delete_document(request, doc_id):
    # Retrieve the document object
    dakghar_document = get_object_or_404(StoreDocument, pk=doc_id)

    # Get the filename from the document object
    filename = dakghar_document.filename

    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Delete the file from the filesystem
    try:
        os.remove(file_path)
        messages.success(request, 'File deleted successfully!')
    except OSError as e:
        messages.error(request, f'Error deleting file: {e}')

    # Delete the document object from the database
    dakghar_document.delete()

    messages.success(request, 'Document Deleted!')
    return redirect('dashboard-dakghar-documents')






@check_session_exists
def manager(request): 
    return render(request,'dashboard-gm.html');
  
   


# def department(request): 
#     uid = request.session.get('user_id')

#     correspondence_ids = []

#     getCorrespondenceIds = CorrespondenceUserMap.objects.filter(to_user_id=uid) 

#     for corr in getCorrespondenceIds:
#         correspondence_ids.append(corr.correspondence_id)

#     # Fetch all Correspondence instances corresponding to the collected correspondence_ids
#     correspondences = Correspondence.objects.filter(pk__in=correspondence_ids)
    
#     # Fetch StoreDocument instances for each Correspondence instance
#     for correspondence in correspondences:
#         document_ids = correspondence.documents.split(',')
#         documents = StoreDocument.objects.filter(pk__in=document_ids)
#         correspondence.documents = documents 

#     # return HttpResponse(correspondences)    
    
#     data = {'section': "list", 'correspondences': correspondences} 
#     return render(request,'dashboard-department.html',data); 



@check_session_exists
def dashboard_department(request):
    uid = request.session.get('user_id')

    received_corr_count = CorrespondenceUserMap.objects.filter(to_user_id = uid).count()
    forwarded_corr_count = CorrespondenceUserMap.objects.filter(from_user_id = uid).count()
    corr_count = {'received_corr_count' : received_corr_count,'forwarded_corr_count':forwarded_corr_count}
    data = {'section': "dashboard_department",'corr_count':corr_count}
    return render(request,'dashboard-department.html',data);




@check_session_exists 
def incoming_correspondence_department(request):  
    uid = request.session.get('user_id')
    

    # queryset = CorrespondenceUserMap.objects \
    #     .filter(to_user_id = uid) \
    #     .select_related('correspondence','user') \
    #     .values('id', 'status', 'correspondence__id', 'correspondence__corr_no', 'correspondence__priority', 'correspondence__int_ext', 'correspondence__name_of_designation', 'correspondence__email_id', 'correspondence__type_of_doc', 'correspondence__do_received_from', 'correspondence__reference_number', 'correspondence__reference_date', 'correspondence__subject', 'correspondence__action_marked', 'correspondence__date_of_forwarding', 'correspondence__department_id', 'correspondence__sub_department_id', 'correspondence__documents', 'correspondence__status', 'correspondence__user_id', 'correspondence__role_id')
    
    queryset = CorrespondenceUserMap.objects \
    .filter(to_user_id=uid) \
    .select_related('correspondence', 'from_user', 'to_user') \
    .values(
        'id','is_opened','message','is_forwarded', 'status', 'correspondence__id', 'correspondence__corr_no', 
        'correspondence__priority', 'correspondence__int_ext', 
        'correspondence__name_of_designation', 'correspondence__email_id', 
        'correspondence__type_of_doc', 'correspondence__do_received_from', 
        'correspondence__reference_number', 'correspondence__reference_date', 
        'correspondence__subject', 'correspondence__action_marked', 
        'correspondence__date_of_forwarding','correspondence__documents', 
        'correspondence__status', 'correspondence__user_id', 
        'correspondence__role_id',
        from_user_name=F('from_user__username'),  # Assuming 'username' is the field in User for the username
        from_user_role_name=F('from_user__user_role_maps__role__role_name'),  # Assuming 'role_name' is the field in Role for the user's role
        to_user_name=F('to_user__username')  # Assuming 'username' is the field in User for the username
    )

    for correspondence in queryset:
        document_ids = correspondence['correspondence__documents'].split(',')  # Access the field using dictionary syntax
        documents = StoreDocument.objects.filter(pk__in=document_ids)
        correspondence['documents'] = documents  # Store documents in the correspondence dictionary

    # queryset2 = CorrespondenceUserMap.objects.filter(to_user_id=uid)
    # queryset2.update(is_opened = 1)    
    
    received_corr_count = CorrespondenceUserMap.objects.filter(to_user_id = uid).count()
    forwarded_corr_count = CorrespondenceUserMap.objects.filter(from_user_id = uid).count()
    corr_count = {'received_corr_count' : received_corr_count,'forwarded_corr_count':forwarded_corr_count}    
    
    data = {'section': "incoming_list", 'correspondences': queryset,'corr_count':corr_count}
    return render(request,'dashboard-department.html',data);





@check_session_exists
def outgoing_correspondence_department(request): 
    uid = request.session.get('user_id')
    
    queryset = CorrespondenceUserMap.objects \
    .filter(from_user_id=uid) \
    .select_related('correspondence', 'from_user', 'to_user') \
    .values(
        'id', 'status', 'correspondence__id', 'correspondence__corr_no', 
        'correspondence__priority', 'correspondence__int_ext', 
        'correspondence__name_of_designation', 'correspondence__email_id', 
        'correspondence__type_of_doc', 'correspondence__do_received_from', 
        'correspondence__reference_number', 'correspondence__reference_date', 
        'correspondence__subject', 'correspondence__action_marked', 
        'correspondence__date_of_forwarding','correspondence__documents', 
        'correspondence__status', 'correspondence__user_id', 
        'correspondence__role_id','is_opened','is_forwarded',
        from_user_name=F('from_user__username'),  # Assuming 'username' is the field in User for the username
        to_user_role_name=F('to_user__user_role_maps__role__role_name'),  # Assuming 'role_name' is the field in Role for the user's role
        to_user_name=F('to_user__username'),  # Assuming 'username' is the field in User for the username
    ) 
    
    for correspondence in queryset:
        document_ids = correspondence['correspondence__documents'].split(',')  # Access the field using dictionary syntax
        documents = StoreDocument.objects.filter(pk__in=document_ids)
        correspondence['documents'] = documents  # Store documents in the correspondence dictionary

    received_corr_count = CorrespondenceUserMap.objects.filter(to_user_id = uid).count()
    forwarded_corr_count = CorrespondenceUserMap.objects.filter(from_user_id = uid).count() 
    corr_count = {'received_corr_count' : received_corr_count,'forwarded_corr_count':forwarded_corr_count}    
    
    data = {'section': "outgoing_list", 'correspondences': queryset,'corr_count':corr_count}  
    return render(request,'dashboard-department.html',data);




@check_session_exists
def download_document(request,file_name):
   return download_file("20240510130830.pdf")




@check_session_exists
def dashboard_account(request):
    uid = request.session.get('user_id')

    if request.method == 'POST':
        phone = request.POST.get('phone')  
        fullname = request.POST.get('full_name')

        try:
            userdetail = UserDetail.objects.get(user_id=uid)
            userdetail.phone = phone
            userdetail.full_name = fullname
            userdetail.save()
            messages.success(request, 'User Detail Updated!')
        except UserDetail.DoesNotExist:
            messages.error(request, 'User Detail not found.')
        
        return redirect(request.path)  # Redirect back to the same page

    users = User.objects.filter(pk=uid).prefetch_related('user_details', 'user_role_maps')

    user_data = []
    for user in users:
        user_info = {
            'user': user,
            'user_details': list(user.user_details.all()),
            'user_role_maps': list(user.user_role_maps.all())
        }
        user_data.append(user_info)    

    data = {'section': "dashboard-account", 'user_data': user_data}
    return render(request, 'dashboard-account.html', data) 