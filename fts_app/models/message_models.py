from django.db import models
from .user_models import User 
from .documents_models import StoreDocument

class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    from_email = models.EmailField(null=True) 
    to_email = models.EmailField(null=True)   
    document = models.ForeignKey(StoreDocument, on_delete=models.CASCADE)
    message = models.TextField()  
    created = models.DateTimeField(auto_now_add=True)   
    updated = models.DateTimeField(auto_now=True) 
    is_opened = models.IntegerField(default=0)
    is_forwarded = models.IntegerField(default=0)
    status = models.IntegerField(default=0)  

    def __str__(self):  
        return f"From: {self.from_user.username}, To: {self.to_user.username}"   

