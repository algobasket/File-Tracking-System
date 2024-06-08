from django.shortcuts import render, redirect
from django.http import HttpResponse
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, UserRoleMap , Department , SubDepartment, Correspondence  
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Prefetch
from django.utils.dateparse import parse_date
from .decorators import check_session_exists  


@check_session_exists
def list_users(request):
    users = User.objects.all().prefetch_related('userdetail', 'userrolemap_set')
    
    data = {'section': "list", 'users': users}
    return render(request, 'admin/user.html', data)




def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')  # Get the raw password
        hashed_password = make_password(raw_password)  # Hash the password
        
        role = request.POST.get('role')
        status = 1  # Assuming 1 means active, adjust according to your needs
        
        user = User(username=username, password=hashed_password, status=status)
        user.save()
        
        user_id = user.id
        
        user_detail = UserDetail(user_id=user_id, status=status) 
        user_detail.save()
        
        user_role_map = UserRoleMap(user_id=user_id, role_id=role, status=status)
        user_role_map.save() 
        
        messages.success(request, 'User added successfully!')
        
        return redirect('admin-list-users') 
    
    roles = Role.objects.all() 
    data = {'section': "add", 'roles': roles} 
    return render(request, 'admin/user.html', data) 