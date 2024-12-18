from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class mediaFile(models.Model):
    file = models.FileField(upload_to='mediafile/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mediafiles')

class mediaFileData(models.Model):
    media_file = models.ForeignKey(mediaFile, on_delete=models.CASCADE, related_name='data')
    name = models.CharField(max_length=100, null=True, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    properties_available_at = models.DateTimeField(null=True, blank=True) 

class logs(models.Model):
    media_file_data = models.ForeignKey(mediaFileData, on_delete=models.CASCADE, related_name='logs')
    before_data = models.JSONField()
    after_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)