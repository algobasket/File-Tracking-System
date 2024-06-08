from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend the default User model
class User(AbstractUser):
    # Add any additional fields for the user here
    pass

# Define a model for user details
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for user details
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

# Define a model for roles
class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# Define a model for user role mapping
class UserRoleMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    # Add any additional fields for the mapping
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}" 

