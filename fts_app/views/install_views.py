from .decorators import check_session_exists
from django.shortcuts import render, redirect
from django.http import HttpResponse
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, UserRoleMap , Department , SubDepartment, Correspondence, CorrespondenceUserMap  
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Prefetch
from django.utils.dateparse import parse_date
from django.db.models import F, Q
 

rolesArray = [
    {'id': 1, 'role_name': 'ADMIN', 'description': 'admin', 'status': 1},
    {'id': 2, 'role_name': 'GMS', 'description': 'gms', 'status': 1},
    {'id': 3, 'role_name': 'DAKGHAR', 'description': 'dak', 'status': 1},
    {'id': 4, 'role_name': 'HOS', 'description': 'hos', 'status': 1},
    {'id': 5, 'role_name': 'GO', 'description': 'go', 'status': 1},
    {'id': 6, 'role_name': 'CO', 'description': 'co', 'status': 1},
    {'id': 7, 'role_name': 'DO', 'description': 'do', 'status': 1},
    {'id': 8, 'role_name': 'GM', 'description': 'gm', 'status': 1}
]

usersArray = [
    {'username': 'admin', 'email': 'admin@oefhz.com', 'full_name': 'Ankit Admin', 'phone': '1111111111', 'role_id': 1, 'status': 1},
    {'username': 'gms', 'email': 'gms@oefhz.com', 'full_name': 'Sunil', 'phone': '1111111111', 'role_id': 2, 'status': 1},
    {'username': 'dakghar', 'email': 'dakghar@oefhz.com', 'full_name': 'Rahul', 'phone': '1111111111', 'role_id': 3, 'status': 1},
    {'username': 'hos', 'email': 'hos@oefhz.com', 'full_name': 'Amit', 'phone': '1111111111', 'role_id': 4, 'status': 1},
    {'username': 'go', 'email': 'go@oefhz.com', 'full_name': 'Rakesh', 'phone': '1111111111', 'role_id': 5, 'status': 1},
    {'username': 'co', 'email': 'co@oefhz.com', 'full_name': 'Mohit', 'phone': '1111111111', 'role_id': 6, 'status': 1},
    {'username': 'do', 'email': 'do@oefhz.com', 'full_name': 'Lavit', 'phone': '1111111111', 'role_id': 7, 'status': 1},
    {'username': 'gm', 'email': 'gm@oefhz.com', 'full_name': 'Ravi', 'phone': '1111111111', 'role_id': 8, 'status': 1}
]

def install(request):
    if request.method == 'POST':
        roles = Role.objects.all()
        if roles.exists():
            messages.error(request, 'Role Record Already Exists!')
        else:
            try:
                for role_data in rolesArray: 
                    role = Role(
                        id=role_data['id'],
                        role_name=role_data['role_name'],
                        description=role_data['description'],
                        status=role_data['status']
                    )
                    role.save()
                    messages.success(request, f'Role {role.role_name} added successfully!')

                for user_data in usersArray:
                    user = User.objects.create(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=make_password(user_data['username']),
                        status=user_data['status']
                    )
                    UserDetail.objects.create(
                        user=user,
                        email=user_data['email'],
                        full_name=user_data['full_name'],
                        phone=user_data['phone'],
                        status=user_data['status']
                    )
                    UserRoleMap.objects.create(
                        user=user,
                        role_id=user_data['role_id'],
                        status=user_data['status']
                    )
                    messages.success(request, f'User {user.username} added successfully!')
            except Exception as e:
                messages.error(request, f'Error occurred: {str(e)}')

    data = {'section': "install"}
    return render(request, 'install.html', data)