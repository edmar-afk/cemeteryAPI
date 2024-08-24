from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.


class Kalag(models.Model):
    cemetery_section = models.TextField()
    name = models.TextField()
    date_born = models.TextField()
    date_died = models.TextField()
    address = models.TextField()
    grave_number = models.IntegerField()
    
    relative_name = models.TextField()
    relative_number = models.TextField()
    relative_address = models.TextField()
    relative_relation = models.TextField()


class Memories(models.Model):
    kalag = models.ForeignKey(Kalag, on_delete=models.CASCADE)
    speech = models.TextField()
    background_image = models.FileField(upload_to='background/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], null=True, blank=True)
    profile_pic = models.FileField(upload_to='profile/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], null=True, blank=True)
    video = models.FileField(upload_to='video/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'mkv', 'wmv', 'mpeg'])], null=True, blank=True)
    
class Plot(models.Model):
    cemetery_section = models.TextField()
    name = models.TextField()
    number = models.IntegerField()
    
    
class MasterList(models.Model):
    kalag = models.ForeignKey(Kalag, on_delete=models.CASCADE)
    grave_level = models.TextField()
    amount = models.IntegerField()
    year = models.IntegerField()
    date_registered = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    
    