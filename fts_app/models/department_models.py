# department_models.py code

from django.db import models 
 

class Department(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey('fts_app.User', on_delete=models.CASCADE)  
    status = models.BooleanField(default=True)     

    def __str__(self):
        return self.name
    
class SubDepartment(models.Model):   
    name = models.CharField(max_length=255)   
    slug_name = models.CharField(max_length=255)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sub_departments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey('fts_app.User', on_delete=models.CASCADE)  
    status = models.BooleanField(default=True)     

    def __str__(self):   
        return self.name
            
class DepartmentRoleMap(models.Model):     
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_departmentrolemaps')
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, related_name='subdepartment_departmentrolemaps')
    role = models.ForeignKey('fts_app.Role', on_delete=models.CASCADE)

    def __str__(self):    
        return str(self.department)   