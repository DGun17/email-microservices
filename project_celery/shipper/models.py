from django.db import models
# from django.conf import settings


# Create your models here.
class Report(models.Model):
    shipper = models.FileField(upload_to='reports')
