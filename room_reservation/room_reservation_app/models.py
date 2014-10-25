from django.db import models

# Create your models here.

from django.contrib.auth.models import User

import random


class UserProfile(models.Model):
  firstName=models.CharField(max_length=150)
  lastName=models.CharField(max_length=150)
  username=models.CharField(max_length=150)
  #token=models.CharField(max_length=150, primary_key=True)

class Building(models.Model):
  name=models.CharField(max_length=255)

class Room(models.Model):
  name=models.CharField(max_length=255)
  building=models.ForeignKey(Building)
  capacity=models.IntegerField()


class Event(models.Model):
  name=models.CharField(max_length=255)
  startTime=models.DateTimeField()
  endTime=models.DateTimeField()
  user=models.ForeignKey(User)
  room=models.ForeignKey(Room)
  notes=models.CharField(max_length=255)
  

class Feature(models.Model):
  name=models.CharField(max_length=255)

class RoomFeature(models.Model):
  room=models.ForeignKey(Room)
  feature=models.ForeignKey(Feature)

class Layout(models.Model):
  name=models.CharField(max_length=255)
  room=models.ForeignKey(Room)

