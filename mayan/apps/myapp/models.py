from django.db import models

# Create your models here.
class Document(models.Model):
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
