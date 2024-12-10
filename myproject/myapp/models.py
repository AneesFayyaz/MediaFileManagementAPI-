from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class mediafile(models.Model):
    file=models.FileField(upload_to='mediafile/')
    uploaded_by=models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='mediafile_uploaded', default=1)
    
class mediafiledata(models.Model):
    media_file=models.ForeignKey(mediafile, on_delete=models.CASCADE,related_name='data')
    name=models.CharField(max_length=100)
    size=models.PositiveIntegerField()
    extension=models.CharField(max_length=10)
    uploaded_by=models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name="mediafiledata_uploaded",default=1)

class logs(models.Model):
    media_file_data=models.ForeignKey(mediafiledata, on_delete=models.CASCADE,related_name='logs')
    before_data=models.JSONField()
    after_data=models.JSONField()
    timestamp=models.DateTimeField(auto_now_add=True)
    