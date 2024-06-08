from django.db import models
from .user_models import User, Role  

class Correspondence(models.Model): 
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'), 
        ('low', 'Low'),
    ]

    INTERNAL_EXTERNAL_CHOICES = [ 
        ('internal', 'Internal'),
        ('external', 'External'),
    ]
    
    corr_no = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    int_ext = models.CharField(max_length=10, choices=INTERNAL_EXTERNAL_CHOICES)
    name_of_designation = models.CharField(max_length=255)
    email_id = models.EmailField()
    type_of_doc = models.CharField(max_length=255)
    do_received_from = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=100)
    reference_date = models.DateField()
    subject = models.CharField(max_length=255)
    action_marked = models.CharField(max_length=255)
    date_of_forwarding = models.DateField()
    documents = models.CharField(max_length=255)
    status = models.IntegerField(default=1) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user') 
    role = models.ForeignKey(Role, on_delete=models.CASCADE) 

    def __str__(self):
        return self.subject  



class CorrespondenceUserMap(models.Model):   
      
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_correspondences')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_correspondences')
    correspondence = models.ForeignKey(Correspondence, on_delete=models.CASCADE, related_name='correspondence_mappings')
    created = models.DateTimeField(auto_now_add=True)   
    updated = models.DateTimeField(auto_now=True) 
    status = models.IntegerField(default=1)  # Assuming default status as 1, change it according to your requirements
    is_opened = models.IntegerField(default=0)
    is_forwarded = models.IntegerField(default=0)
    message = models.TextField(null=True)    

    def __str__(self):
        return str(self.status)
