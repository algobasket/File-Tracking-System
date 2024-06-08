# operations_views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, UserRoleMap , Department , SubDepartment, Correspondence, CorrespondenceUserMap  
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Prefetch
from django.utils.dateparse import parse_date
import datetime
from ..decorators import check_session_exists
import os
from django.db.models import F 


@check_session_exists
def list_users(request): 
     users = User.objects.prefetch_related('user_details', 'user_role_maps').order_by('-pk')

     user_data = []
     for user in users:
         user_info = {
            'user': user,
            'user_details': list(user.user_details.all()),
            'user_role_maps': list(user.user_role_maps.all())
         }
         user_data.append(user_info)

     data = {'section': "list", 'users': user_data,'user_count':users.count}
     return render(request, 'admin/user.html', data)




@check_session_exists
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')  # Get the raw password
        hashed_password = make_password(raw_password)  # Hash the password
        phone = request.POST.get('phone')  
        full_name = request.POST.get('full_name')  
        
        
        role_id = request.POST.get('role')
        status = 1 
        
        user = User.objects.create(username=username, password=hashed_password, status=status) 
        user_detail = UserDetail.objects.create(user=user,full_name=full_name,phone=phone,status=status)  
        user_role_map = UserRoleMap.objects.create(user=user, role_id=role_id, status=status) 
        
        messages.success(request, 'New staff added successfully!')
        return redirect('admin-list-users')     
    
    roles = Role.objects.all() 
    data = {'section': "add", 'roles': roles} 
    return render(request, 'admin/user.html', data) 




@check_session_exists
def list_roles(request):
    roles = Role.objects.all()  
    data = {'section': "list", 'roles': roles} 
    return render(request, 'admin/role.html',data)




@check_session_exists
def add_role(request): 
    if request.method == 'POST':
        rolename = request.POST.get('role_name')
        description = request.POST.get('role_description')
        
        role = Role(role_name=rolename, description=description)
        role.save()
        messages.success(request, 'Role added successfully!')
        
    data = {'section': "add"}    
    return render(request, 'admin/role.html', data)




@check_session_exists
def delete_role(request,role_id):
    role = Role.objects.get(id=role_id)
    role.delete()
    messages.error(request, 'Role deleted!')

    return redirect('admin-list-roles')



@check_session_exists
def edit_user(request): 
    data = {'section' : "edit"} 
    return render(request,'admin/user.html',data)




@check_session_exists
def delete_user(request,user_id): 
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        user.delete()

        messages.error(request, 'User deleted!')

        return redirect('admin-list-users')     
         


@check_session_exists
def list_correspondence(request):
    uid = request.session.get('user_id')
    correspondences = Correspondence.objects.filter().order_by('-pk')
    
    for correspondence in correspondences:
        document_ids = correspondence.documents.split(',')
        documents = StoreDocument.objects.filter(pk__in=document_ids)
        correspondence.documents = documents
    
    data = {'section': "list", 'correspondences': correspondences,'corr_count' : correspondences.count()}
    return render(request, 'admin/correspondence.html', data)



@check_session_exists
def add_correspondence(request):  
    uid = request.session.get('user_id')
    if request.method == 'POST':
        priority = request.POST.get('priority')
        int_ext = request.POST.get('int_ext')
        name_of_designation = request.POST.get('name_of_designation')
        date_of_forwarding = parse_date(request.POST.get('date_of_forwarding'))
        type_of_doc = request.POST.get('type_of_doc')
        do_received_from = request.POST.get('do_received_from')
        reference_number = request.POST.get('reference_number')
        reference_date = request.POST.get('reference_date')
        subject = request.POST.get('subject')
        action_marked = request.POST.get('action_marked')
        selected_documents = request.POST.get('selected_documents')
        status = request.POST.get('status')
        role = request.POST.get('role')
        now = datetime.datetime.now()
        corr_no = now.strftime("%d%m%y%H%M%S")
        corr_no = "CO-" + corr_no

        if not selected_documents:
            messages.error(request, 'At least one document is required!')
            return HttpResponseRedirect(request.path)
        
        correspondence = Correspondence( 
        user_id = uid,
        corr_no = corr_no,
        priority=priority,
        int_ext=int_ext,
        name_of_designation=name_of_designation,
        date_of_forwarding=date_of_forwarding,
        type_of_doc=type_of_doc,
        do_received_from=do_received_from,
        reference_number=reference_number,
        reference_date=reference_date,
        subject=subject,
        action_marked=action_marked,
        documents = selected_documents,
        role_id = role, 
        status = status
        )
        correspondence.save()  
        
        correspondence_inserted_id = correspondence.id
        select_all_user = request.POST.get('select_all_user')

         
        if select_all_user == '1': 
            user_details = UserDetail.objects.filter( 
            user__user_role_maps__role_id=role
             ).select_related('user')
            user_ids = [detail.user_id for detail in user_details] 
            for user_id in user_ids:  
                CorrespondenceUserMap.objects.create(
                    from_user_id = uid, 
                    to_user_id = user_id, 
                    correspondence_id = correspondence_inserted_id,
                    status = 1 
                ) 
        else:
            selected_users = request.POST.get('selected-roles-users')
            CorrespondenceUserMap.objects.create(
                    from_user_id = uid, 
                    to_user_id = selected_users, 
                    correspondence_id = correspondence_inserted_id,
                    status = 1 
                ) 

        
        messages.success(request, 'Correspondence Added Successfully!') 
        return redirect('admin-list-correspondence') 

    messagesObj = Message.objects.filter(to_user_id=uid).select_related('document', 'from_user')
    # roles = Role.objects.all() 

    session_role = request.session.get('role')
    role_map = {
        'admin': ['gms','gm','co','go','do','hos']
    }
    roles = Role.objects.filter(role_name__in=role_map.get(session_role, [])) 
    
    data = {'section': "add", 'messagesObj': messagesObj, 'roles' : roles}     
    return render(request, 'admin/correspondence.html', data)   




@check_session_exists
# def edit_correspondence(request,correspondence_id):
#     uid = request.session.get('user_id')
#     correspondences = Correspondence.objects.filter(pk=correspondence_id)
    
#     for correspondence in correspondences:
#         document_ids = correspondence.documents.split(',')
#         documents = StoreDocument.objects.filter(pk__in=document_ids)
#         correspondence.documents = documents
#         user_role_maps = UserRoleMap.objects.filter(role_id=correspondence.role_id).select_related('user', 'role', 'user__user_details').values(
#             role_name=F('role__role_name'),
#             username=F('user__username'),
#             full_name=F('user__user_details__full_name'),
#             'user_id'
#         )
#         correspondence.userdetails = user_role_maps
    
#     messagesObj = Message.objects.filter(to_user_id=uid).select_related('document', 'from_user')
#     roles = Role.objects.all()


#     data = {'section' : "edit" ,'correspondences' : correspondences,'roles' : roles, 'messagesObj': messagesObj}
#     return render(request, 'admin/correspondence.html',data)




@check_session_exists  
def edit_correspondence(request, correspondence_id):
    uid = request.session.get('user_id')

    if request.method == 'POST':
        priority = request.POST.get('priority')
        int_ext = request.POST.get('int_ext')
        name_of_designation = request.POST.get('name_of_designation')
        date_of_forwarding = parse_date(request.POST.get('date_of_forwarding'))
        type_of_doc = request.POST.get('type_of_doc')
        do_received_from = request.POST.get('do_received_from')
        reference_number = request.POST.get('reference_number')
        reference_date = request.POST.get('reference_date')
        subject = request.POST.get('subject')
        action_marked = request.POST.get('action_marked')
        selected_documents = request.POST.get('selected_documents')
        status = request.POST.get('status')
        role = request.POST.get('role')

        # Get the correspondence object to edit
        correspondence = Correspondence.objects.get(pk=correspondence_id)  

        # Update the attributes of the correspondence object
        correspondence.priority = priority
        correspondence.int_ext = int_ext
        correspondence.name_of_designation = name_of_designation
        correspondence.date_of_forwarding = date_of_forwarding
        correspondence.type_of_doc = type_of_doc
        correspondence.do_received_from = do_received_from
        correspondence.reference_number = reference_number
        correspondence.reference_date = reference_date
        correspondence.subject = subject
        correspondence.action_marked = action_marked
        correspondence.documents = selected_documents
        correspondence.role_id = role
        correspondence.status = status 

        # Save the updated correspondence object
        correspondence.save()
        messages.success(request, 'Correspondence Added Successfully!')
        redirect(request.get_full_path())

    
    # Use get_object_or_404 for single object retrieval
    correspondence = get_object_or_404(Correspondence, pk=correspondence_id)
    
    # Process documents
    document_ids = correspondence.documents.split(',')
    documents = StoreDocument.objects.filter(pk__in=document_ids)
    correspondence.documents = documents
    document_count = len(document_ids)

    # Process user roles
    user_role_maps = UserRoleMap.objects.filter(role_id=correspondence.role_id).select_related('user', 'role', 'user__user_details').values(
        'user_id',
        role_name=F('role__role_name'),
        username=F('user__username'),
        full_name=F('user__user_details__full_name')
    )
    correspondence.userdetails = user_role_maps

    # Fetch messages for the current user
    messages_obj = Message.objects.filter(to_user_id=uid).select_related('document', 'from_user')

    # Fetch all roles
    roles = Role.objects.all()

    # Prepare context data
    data = {
        'section': "edit",
        'correspondence': correspondence,
        'roles': roles,
        'messagesObj': messages_obj,
        'document_count': document_count
    }
    
    return render(request, 'admin/correspondence.html', data)





@check_session_exists
def forward_correspondence(request, correspondence_id):
    corr_instance = get_object_or_404(Correspondence,pk=correspondence_id)
    uid = request.session.get('user_id')
    role_id = corr_instance.role_id

    user_details = UserDetail.objects.filter( 
    user__user_role_maps__role_id=role_id
     ).select_related('user')
    user_ids = [detail.user_id for detail in user_details]
    # return HttpResponse(user_ids)
    for user_id in user_ids:  
        CorrespondenceUserMap.objects.create(
            from_user_id = uid, 
            to_user_id = user_id, 
            correspondence_id = correspondence_id, 
            status = 1 
        )       
    corr_instance.status = 1 
    corr_instance.save()
    messages.success(request, 'Correspondence Added Successfully!') 
    return redirect('admin-list-correspondence') 




@check_session_exists
def forward_correspondence_list(request):
    uid = request.session.get('user_id')
    queryset = CorrespondenceUserMap.objects \
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
    ).order_by('-pk') 
    
    for correspondence in queryset:
        document_ids = correspondence['correspondence__documents'].split(',')  # Access the field using dictionary syntax
        documents = StoreDocument.objects.filter(pk__in=document_ids)
        correspondence['documents'] = documents  # Store documents in the correspondence dictionary

    total_forwarded_corr_count = CorrespondenceUserMap.objects.count()  
    corr_count = {'total_forwarded_corr_count':total_forwarded_corr_count}        
    
    data = {'section': "forward_correspondence_list", 'correspondences': queryset,'corr_count':corr_count}  
    return render(request,'admin/correspondence.html',data); 




@check_session_exists
def monitoring_documents(request):
    messagesObj = Message.objects.filter().select_related('document', 'from_user').order_by('-pk')
    data = {'section' : "list",'messagesObj': messagesObj,'doc_count' : messagesObj.count()} 
    return render(request, 'admin/monitoring-documents.html',data)     




@check_session_exists
def view_monitoring_document(request,doc_id,msg_id): 

    doc = get_object_or_404(StoreDocument, pk=doc_id)
    
    # Determine file type
    file_type_map = {
        '.pdf': 'pdf',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.png': 'image',
        '.doc': 'word',
        '.docx': 'word',
    }
    
    file_extension = os.path.splitext(doc.filename)[1].lower()
    doc.filetype = file_type_map.get(file_extension, 'unsupported')
    
    # If msg_id is provided, mark the message as opened
    if msg_id and msg_id != 0:
        try:
            message = Message.objects.get(pk=msg_id)
            message.is_opened = True
            message.save()
        except Message.DoesNotExist:
            raise Http404("Message not found") 
    
    # Prepare data for the template
    data = {'section': "view_doc", 'documents': [doc]}

    return render(request, 'admin/monitoring-documents.html',data)   

 



# def delete_monitoring_document(request,doc_id):
#     doc_id = request.GET.get('doc_id')

#     messagesObj = StoreDocument.objects.filter(pk=doc_id)
#     messagesObj.delete()

#     return redirect('admin-monitoring-documents') 

@check_session_exists
def delete_monitoring_document(request,doc_id):
    # doc_id = request.GET.get('doc_id') 
    messagesObj = Message.objects.filter(pk=doc_id)
    messagesObj.delete()
    messages.error(request, 'Document Map removed!')
    return redirect('admin-monitoring-documents')  


@check_session_exists
def delete_correspondence(request,correspondence_id): 
   corr = Correspondence.objects.get(pk=correspondence_id)
   corr.delete()
   messages.error(request, 'Correspondence Removed!') 
   return redirect('admin-list-correspondence')