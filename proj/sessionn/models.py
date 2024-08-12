from django.db import models
from accounts.models import User
from django.db.models import Q 
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import base64       
from datetime import date

 
class GeeksModel(models.Model):
       
    geeks_field = models.FileField(upload_to='attachedfiles', null = True , blank=True)
    
class Session(models.Model):
    
    title = models.TextField()
    agenda = models.TextField(null = True,blank=True)
    session_date = models.DateField(null=True)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)
    related_sessions = models.ManyToManyField('self',blank = True)
    participatins = models.ManyToManyField(User,related_name='participatins',blank=True)
    presents = models.ManyToManyField(User,blank=True,related_name='presents')
    hosts = models.ManyToManyField(User,blank=True,related_name='hosts')
    place = models.TextField(null=True,blank=True)
    attachfile = models.ManyToManyField(GeeksModel,blank =True, related_name = 'attachfile')
    link = models.URLField(blank= True,null=True)
    status_session = (
        ( '1' , 'order1'),
        ('2','order2'),
        ('3', 'order3'),
        ('4', 'order4'),
    )
    order = models.CharField(max_length= 1 , choices=status_session,default='1')
    description = models.TextField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)


