
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Files(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True,blank = True)
    File_name = models.CharField(max_length =200)
    FileS3 = models.CharField(max_length=200)
    Job_id = models.CharField(max_length=200)
    status_to_s3 = models.BooleanField(default = False)
    status_of_job = models.BooleanField(default = False)
    Logtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Job_id
    
    class Meta:
        ordering = ['Logtime']

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to = 'documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    message=models.TextField()
    date = models.DateField(null=True)