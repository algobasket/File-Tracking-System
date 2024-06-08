# user_models.py code

from django.db import models  

class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.username 

class UserDetail(models.Model):       
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')  
    email = models.EmailField(unique=True, null=True)
    full_name = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=15,null=True)
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)   
    
    def __str__(self):
        return self.email  

class Role(models.Model):
    role_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100) 
    status = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.role_name 

class UserRoleMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role_maps')
    role = models.ForeignKey('fts_app.Role', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"

