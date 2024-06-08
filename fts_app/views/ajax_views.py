from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, UserRoleMap , Department , SubDepartment, DepartmentRoleMap, CorrespondenceUserMap  
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Prefetch
from django.db.models import F

def ajaxGetSubDepartment(request):
    department_id = request.POST.get('department_id')
    sub_departments = SubDepartment.objects.filter(department_id=department_id).prefetch_related('created_user', 'department_id')
    sub_department_data = list(sub_departments.values())
    return JsonResponse(sub_department_data, safe=False)



def ajaxGetDepartmentRoles(request):
    department_id = request.POST.get('department_id')
    department_roles = DepartmentRoleMap.objects.filter(department_id=department_id).annotate(
        role_name=F('role__role_name')
    ).values(
        'department_id',
        'sub_department_id',
        'role_id',
        'role_name'
    ).distinct() 
    return JsonResponse(list(department_roles), safe=False)



def ajaxGetRoleUsers(request):
    role_id = request.POST.get('role_id')

    user_details = UserDetail.objects.filter( 
        user__user_role_maps__role_id=role_id
    ).select_related('user').values('user_id','full_name',username = F('user__username'))

    return JsonResponse(list(user_details), safe=False) 



def ajaxCorrespondenceMapIsStatus(request):
     corr_map_id = request.POST.get('corr_map_id')
     is_status_type = request.POST.get('is_status_type')
     is_status_value = request.POST.get('is_status_value')
     corrUserMap = CorrespondenceUserMap.objects.filter(pk=corr_map_id)

     if is_status_type == 'is_opened':
        corrUserMap.update(is_opened = is_status_value)

     if is_status_type == 'is_forwarded':
        corrUserMap.update(is_forwarded = is_status_value)
        
     return 1



def ajaxChangeUserPassword(request):
    if request.method == 'POST':
        uid = request.session.get('user_id')
        password = request.POST.get('password')

        if not uid or not password:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)

        try:
            user = User.objects.get(pk=uid)
            user.password = make_password(password)
            user.save()
            return JsonResponse({'success': 'Password changed successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
