from django.db import models
# Create your models here.


class Kalag(models.Model):
    cemetery_section = models.TextField()
    name = models.TextField()
    date_born = models.TextField()
    date_died = models.TextField()
    address = models.TextField()
    
class Plot(models.Model):
    cemetery_section = models.TextField()
    name = models.TextField()
    number = models.IntegerField()