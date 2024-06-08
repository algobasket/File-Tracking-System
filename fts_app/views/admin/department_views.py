from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, UserRoleMap, Department, SubDepartment, DepartmentRoleMap 
from django.contrib import messages
from django.db.models import Prefetch
from django.utils.text import slugify
from ..decorators import check_session_exists


@check_session_exists 
def list_department(request):
  departments = Department.objects.select_related('created_user').all()

  data = {'section' : 'list_department', 'departments' : departments}
  return render(request,'admin/department.html',data) 



@check_session_exists 
def create_department(request):   
  if request.method == 'POST':
        name = request.POST.get('department_name')
        slug_name = slugify(request.POST.get('department_name'))
        created_user_id = request.session.get('user_id')
        status = request.POST.get('department_status')
        department = Department(name = name,slug_name = slug_name, created_user_id = created_user_id, status = status)
        department.save() 
        messages.success(request,"New Department Added")  
  
  data = {'section' : 'create_department'}
  return render(request,'admin/department.html',data)



@check_session_exists 
def update_department(request,department_id):
    department = Department.objects.get(id=department_id)
    if request.method == 'POST':
          department = Department.objects.get(id=department_id)
          # department = get_object_or_404(Department, pk = department_id)
          department.name = request.POST.get('department_name')  
          department.slug_name = slugify(request.POST.get('department_name'))
          department.status = request.POST.get('department_status')
          department.save() 
          messages.success(request,"Department Updated") 
    
    data = {'section' : 'update_department','department' : department}
    return render(request,'admin/department.html',data) 



@check_session_exists 
def delete_department(request,department_id): 
  department = Department.objects.get(id=department_id) 
  department.delete()
  return redirect('admin-list-department') 



# ----------- Sub Department -----------    


@check_session_exists 
def list_sub_department(request):
  sub_department = SubDepartment.objects.select_related('created_user','department_id').all() 
  data = {'section' : 'list_sub_department', 'sub_department' : sub_department}
  return render(request,'admin/department.html',data) 



@check_session_exists 
def create_sub_department(request):
    if request.method == 'POST':
        sub_department_name = request.POST.get('sub_department_name')
        slug_sub_department_name = slugify(request.POST.get('sub_department_name'))  
        department_id = request.POST.get('parent_department_id')
        created_user_id = request.session.get('user_id') 
        status = request.POST.get('sub_department_status')
        department_roles = request.POST.getlist('department_roles[]') 
        
        sub_department = SubDepartment(
            name=sub_department_name,
            slug_name=slug_sub_department_name,
            department_id_id=department_id,
            created_user_id=created_user_id,
            status=status
        )
        sub_department.save()

        sub_department_insert_id = sub_department.id

        for role in department_roles:
              DepartmentRoleMap.objects.create(
                  department_id = department_id,
                  sub_department_id = sub_department_insert_id,
                  role_id = role
              ) 
          
        messages.success(request, "New Sub Department Added")
        return redirect('admin-list-sub-department')  # Redirect to a suitable URL after creation
    
    roles = Role.objects.all()
    departments = Department.objects.select_related('created_user').all() 
    data = {'section': 'create_sub_department', 'departments': departments,'roles' : roles}
    return render(request, 'admin/department.html', data)



@check_session_exists 
def update_sub_department(request,sub_department_id):
    sub_department = SubDepartment.objects.get(id=sub_department_id)  
    sub_department_roles = DepartmentRoleMap.objects.filter(sub_department_id=sub_department_id)
    role_ids = []
    for r in sub_department_roles:
        role_ids.append(r.role_id)

    if request.method == 'POST':
        # department = get_object_or_404(Department, pk = department_id)
        sub_department.name = request.POST.get('sub_department_name') 
        sub_department.slug_name = slugify(request.POST.get('sub_department_name'))
        sub_department.department_id_id = request.POST.get('parent_department_id')
        sub_department.status = request.POST.get('sub_department_status')
        department_roles = request.POST.getlist('department_roles[]')    
        sub_department.save()  
  
        # DepartmentRoleMap.objects.filter(sub_department_id=sub_department_id, role_id__in=roles_to_delete).delete()

        for role in department_roles:
              defaults = {'role_id': role}
              DepartmentRoleMap.objects.update_or_create( 
                  department_id = sub_department.department_id_id,
                  sub_department_id = sub_department_id,
                  role_id=role,
                  defaults=defaults
              ) 

        messages.success(request,"Sub Department Updated")
        return redirect('admin-update-sub-department',sub_department_id)
    
    roles = Role.objects.all()
    departments = Department.objects.select_related('created_user').all() 
    data = {'section' : 'update_sub_department','sub_department' : sub_department,'roles' : roles, 'departments': departments,'sub_department_roles' : role_ids}   
    return render(request,'admin/department.html',data)   



@check_session_exists 
def delete_sub_department(request,sub_department_id):  
  sub_department = Department.objects.get(id=sub_department_id)
  sub_department.delete()  

  return redirect('admin-list-sub-department')


