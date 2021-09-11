from django.db import models
from typing import Text
from django.db import models
from django.db.models.fields.related import ManyToManyField
from datetime import datetime


class UsersManager(models.Manager):
  
  def basic_validator(self, postData):

    errors={}
  
    if len(postData['name']) < 3:
      errors['name'] = 'Your name should be at least 3 characters'

    if len(postData['email']) < 3:
      errors['email'] = 'Your name should be at least 3 characters'
    
    if len(postData['password']) < 8:
      errors['password'] = 'Password should be at least 8 characters'
    
    if postData['password'] != postData['password_confirm']:
      errors['password'] = 'passwords dont match'
    
    return errors

class TripsManager(models.Manager):
  
  def basic_validator(self, postData):

    errors={}
  
    if len(postData['destination']) < 1:
      errors['description'] = 'Destination Should not be empty'

    if len(postData['plan']) < 1:
      errors['plan'] = ' Plan Should not be empty'
    
    if len(postData['datefrom']) < 1:
      errors['datefrom'] = 'Should not be empty'
    
    if len(postData['dateto']) < 1:
      errors['dateto'] = 'Should not be empty'
    
    if datetime.strptime(postData['datefrom'],"%Y-%m-%d").date() < datetime.today().date():
      errors['datefrom'] = 'Travel Date From Should not be in the past'
    
    if datetime.strptime(postData['dateto'],"%Y-%m-%d").date() < datetime.strptime(postData['datefrom'],"%Y-%m-%d").date():
      errors['datefrom'] = 'Travel Date From should not be past the Travel Date To'

    return errors


class Users(models.Model):
  name = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  avatar = models.URLField(default='https://www.clipartmax.com/png/middle/97-978328_avatar-icon-free-fa-user-circle-o.png')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UsersManager()
  def __str__(self) -> str:
      return f'{self.id} : {self.name}'


class Trips(models.Model):
  description = models.CharField(max_length=255)
  start = models.DateTimeField()
  end = models.DateTimeField()
  plan = models.CharField(max_length=255)
  organizer = models.ForeignKey(Users, related_name='organized', on_delete=models.CASCADE)
  group = ManyToManyField(Users, related_name='joined')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = TripsManager()
  def __str__(self) -> str:
      return f'{self.id} : {self.description}'