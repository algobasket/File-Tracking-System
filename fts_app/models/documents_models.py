from django.db import models
from fts_app.models import User 

class StoreDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link with your custom user model
    title = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)  # Assuming filename is stored as a string
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(default=1)  

    def __str__(self):
        return self.title