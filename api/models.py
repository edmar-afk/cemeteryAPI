from django.db import models
# Create your models here.


class Cemetery(models.Model):
    section = models.TextField()
    location = models.TextField()
    slots = models.IntegerField()


class Kalag(models.Model):
    cemetery_section = models.ForeignKey(Cemetery, on_delete=models.CASCADE)
    name = models.TextField()
    date_born = models.TextField()
    date_died = models.TextField()
    address = models.TextField()