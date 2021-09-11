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
  
    if len(postData['destination']) < 0:
      errors['description'] = 'Should not be empty'

    if len(postData['plan']) < 0:
      errors['plan'] = 'Should not be empty'
    
    if len(postData['datefrom']) < 0:
      errors['datefrom'] = 'Should not be empty'
    
    if len(postData['dateto']) < 0:
      errors['dateto'] = 'Should not be empty'
    
    if datetime.strptime(postData['datefrom'],"%Y-%m-%d").date() < datetime.today().date():
      errors['datefrom'] = 'Travel Date From Should not be in the past'
    
    if datetime.strptime(postData['dateto'],"%Y-%m-%d").date() < datetime.strptime(postData['datefrom'],"%Y-%m-%d").date():
      errors['datefrom'] = 'Travel Date From should not be past the Date To'

    return errors


class Users(models.Model):
  name = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  avatar = models.URLField(default='https://i.pinimg.com/originals/13/f4/09/13f4093020fc96ba87eae8221d071af7.jpg')
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