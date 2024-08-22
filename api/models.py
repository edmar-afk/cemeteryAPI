from django.db import models
# Create your models here.


class Kalag(models.Model):
    cemetery_section = models.TextField()
    name = models.TextField()
    date_born = models.TextField()
    date_died = models.TextField()
    address = models.TextField()
    
    relative_name = models.TextField()
    relative_number = models.TextField()
    relative_address = models.TextField()
    relative_relation = models.TextField()
    
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
    
    