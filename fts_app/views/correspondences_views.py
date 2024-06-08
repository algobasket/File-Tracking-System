# operations_views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, UserRoleMap , Department , SubDepartment, Correspondence, CorrespondenceUserMap, DepartmentRoleMap  
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Prefetch
from django.utils.dateparse import parse_date
import datetime
from .decorators import check_session_exists 
from django.db.models import F 
import os




@check_session_exists 
def list_correspondence(request):
    uid = request.session.get('user_id')
    correspondences = Correspondence.objects.filter(user_id=uid).order_by('-pk')
    
    for correspondence in correspondences:
        document_ids = correspondence.documents.split(',')
        documents = StoreDocument.objects.filter(pk__in=document_ids)
        correspondence.documents = documents
    
    data = {'section': "list", 'correspondences': correspondences,'corr_count' : correspondences.count()}   
    return render(request, 'correspondence.html', data)    




@check_session_exists
def list_incoming_correspondence(request):
    uid = request.session.get('user_id')
    correspondences = Correspondence.objects.filter(user_id=uid).order_by('-pk')
    
    for correspondence in correspondences:
        document_ids = correspondence.documents.split(',')
        documents = StoreDocument.objects.filter(pk__in=document_ids)
        correspondence.documents = documents
    
    data = {'section': "list", 'correspondences': correspondences}
    return render(request, 'correspondence.html', data) 




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
        sending_options = request.POST.get('sending_options') 
        role = request.POST.get('role')
        now = datetime.datetime.now()
        corr_no = now.strftime("%d%m%y%H%M%S")
        corr_no = "CO-" + corr_no

        if not selected_documents:
            messages.error(request, 'At least one document is required!')
            return HttpResponseRedirect(request.path)  # Redirects to the same page    
        
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
        status = 1
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
        
        selected_document_ids = list(map(int, selected_documents.split(','))) 
        Message.objects.filter(document_id__in=selected_document_ids, to_user_id=uid).update(is_forwarded=1)
        
        messages.success(request, 'Correspondence Added Successfully!')  
        return redirect('list-correspondence') 

    messagesObj = Message.objects.filter(to_user_id=uid).select_related('document', 'from_user')

     # Role filtering based on session role
    session_role = request.session.get('role')
    role_map = {
        'gms': ['gm'],
        'gm': ['co','go','do','hos'],
        'co': ['go','do','hos','gm'],
        'go': ['co','do','hos','gm'],
        'do': ['co','go','hos','gm'], 
        'hos': ['co','go','do','gm']
    }
    roles = Role.objects.filter(role_name__in=role_map.get(session_role, []))                    
    
    data = {'section': "add", 'messagesObj': messagesObj, 'roles' : roles}     
    return render(request, 'correspondence.html', data)  






def edit_correspondence(request):
    data = {'section' : "edit"}
    request.name = "edit" 
    return render(request, 'correspondence.html',data)






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
            status = 0 
        )       
    corr_instance.status = 1 
    corr_instance.save()
    messages.success(request, 'Correspondence Forwarded Successfully!') 
    return redirect('list-correspondence')  






@check_session_exists
def delete_monitoring_document(request,doc_id):
    doc_id = request.GET.get('doc_id')

    messagesObj = StoreDocument.objects.filter(pk=doc_id)
    messagesObj.delete()

    return redirect('monitoring-documents')   






@check_session_exists
def monitoring_documents(request):
    role = request.session.get('role')
    uid = request.session.get('user_id') 

    if role == 'admin' or role == 'dakghar':
      messagesObj = Message.objects.filter().select_related('document', 'from_user').order_by('-pk')
    else:
      messagesObj = Message.objects.filter(to_user=uid).select_related('document', 'from_user').order_by('-pk')    

    data = {'section' : "list",'messagesObj': messagesObj,'doc_count' : messagesObj.count()} 
    return render(request, 'monitoring-documents.html',data)     





# def view_monitoring_document(request,doc_id,msg_id): 

#     documents = StoreDocument.objects.filter(pk=doc_id)
#     for doc in documents:
#         filename = doc.filename
#         if filename.endswith(".pdf"):
#             doc.filetype = "pdf"
#         elif filename.endswith(".jpg") or filename.endswith(".png"):
#             doc.filetype = "image"
#         elif filename.endswith(".doc") or filename.endswith(".docx"):
#             doc.filetype = "word"
#         else:
#             doc.filetype = "unsupported"

#     if msg_id
#       message = get_object_or_404(Message,pk=msg_id)
#       message.is_opened = 1
#       message.save() 

#     data = {'section' : "view_doc",'documents': documents} 
#     return render(request, 'monitoring-documents.html',data)   



@check_session_exists
def view_monitoring_document(request, doc_id, msg_id=None):
    # Get the document or raise a 404 error if not found
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
    
    # Render the template with the data
    return render(request, 'monitoring-documents.html', data)


@check_session_exists
def view_correspondence_document(request,doc_id, correspondence_map_id=None):
    # Get the document or raise a 404 error if not found
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
    if correspondence_map_id and correspondence_map_id != 0:
       CorrespondenceUserMap.objects.filter(pk=correspondence_map_id).update(is_opened=1)   


    # Prepare data for the template 
    data = {'section': "view_correspondence_doc", 'documents': [doc]}  
    
    # Render the template with the data
    return render(request, 'monitoring-documents.html', data)




@check_session_exists
def delete_correspondence(request,correspondence_id): 
     corr = Correspondence.objects.get(pk=correspondence_id)
     corr.delete()
     messages.error(request, 'Correspondence Removed!') 
     return redirect('list-correspondence')






@check_session_exists
def forward_departmental_correspondence(request, correspondence_map_id, correspondence_id):
    uid = request.session.get('user_id')
    
    if request.method == 'POST': 

        select_all_user = request.POST.get('select_all_user')  
        message = request.POST.get('message') 
         
        if select_all_user == '1': 
            role = request.POST.get('selectDepartmentRole')
            user_details = UserDetail.objects.filter(
                user__user_role_maps__role_id=role
            ).select_related('user')
            user_ids = [detail.user_id for detail in user_details]

            if not user_ids:  # If no users found
                messages.error(request, 'No users found for the selected department role.')
                return redirect(request.get_full_path())

            for user_id in user_ids:
                CorrespondenceUserMap.objects.create(
                    from_user_id=uid,
                    to_user_id=user_id,
                    correspondence_id=correspondence_id,
                    status=1,
                    message = message
                )
        else:
            selected_users = request.POST.get('selected-roles-users')
            CorrespondenceUserMap.objects.create(
                    from_user_id = uid, 
                    to_user_id = selected_users, 
                    correspondence_id = correspondence_id,
                    status = 1,
                    message = message 
                )          
        CorrespondenceUserMap.objects.filter(pk=correspondence_map_id).update(is_forwarded=1)
        messages.success(request, 'Correspondence Forwarded Successfully!')
        return redirect(request.get_full_path())  # Redirect to a success page or another view



    # Role filtering based on session role
    session_role = request.session.get('role')
    role_map = {
        'gms': ['gm'],
        'gm': ['co','go','do','hos'],
        'co': ['go','do','hos','gm'],
        'go': ['co','do','hos','gm'],
        'do': ['co','go','hos','gm'], 
        'hos': ['co','go','do','gm']
    }
    roles = Role.objects.filter(role_name__in=role_map.get(session_role, []))

    received_corr_count = CorrespondenceUserMap.objects.filter(to_user_id = uid).count()
    forwarded_corr_count = CorrespondenceUserMap.objects.filter(from_user_id = uid).count()
    corr_count = {'received_corr_count' : received_corr_count,'forwarded_corr_count':forwarded_corr_count} 

    data = {'section': "forwarding", 'roles': roles, 'corr_count':corr_count}  
    return render(request, 'dashboard-department.html', data)




@check_session_exists 
def getDepartmentRoles(department_id, sub_department_id):
    department_roles = DepartmentRoleMap.objects.filter(department_id=department_id, sub_department_id=sub_department_id).annotate(
        role_name=F('role__role_name')
    ).values(
        'department_id',
        'sub_department_id',
        'role_id',
        'role_name'
    ).distinct() 
    
    # Serialize queryset into JSON
    department_roles_list = list(department_roles)
    return department_roles_list    