from django.shortcuts import render
from django.http import HttpResponse,Http404
from django import template 
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from room_reservation_app.models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from mimetypes import guess_type
from dateutil import parser
from datetime import datetime, timedelta
from pytz import timezone, utc
import re
import json

def register(request):

	context={}
	if request.method=='GET':

		return render(request, 'room_reservation_app/registration.html',context)

	errors = []

	# Checks the validity of the form data
	if not 'firstName' in request.POST or not request.POST['firstName']:
		errors.append('FirstName is required.')
	elif not 'lastName' in request.POST or not request.POST['lastName']:
		errors.append('LastName is required.')
	elif not 'email' in request.POST or not request.POST['email']:
		errors.append('Email is Required')
	# Save the username in the request context to re-fill the username
	# field in case the form has errrors
	#context['username'] = request.POST['username']
	if not 'pass' in request.POST or not request.POST['pass']:
		errors.append('Password is required.')



	if len(User.objects.filter(username = request.POST['email'])) > 0:
		errors.append('Email is already taken.')
	context['errors'] = errors
	if errors:

		return render(request, 'room_reservation_app/registration.html', context)

	# Creates the new user from the valid form data
	new_user = User.objects.create_user(username=request.POST['email'], 
	                            password=request.POST['pass'],
								first_name=request.POST['firstName'],\
								last_name=request.POST['lastName']
								)
	#token=str(default_token_generator.make_token(new_user))

	new_user.is_active=True


	new_user.save()

	userProf = UserProfile(username=request.POST['email'])
	userProf.save()
	

	return redirect('/myReservations')

def confirmCred(request):
	print "gets called"
	#quthenticate users
	context={}
	errors=[]
	context['errors']=errors
	if 'username' in request.POST and request.POST['username'] and 'password' in request.POST and request.POST['password']:
		username=request.POST['username']
		password=request.POST['password']
	else: 
		errors.append("Please login first")
		return render(request,'room_reservation_app/signin.html',context)

	user = authenticate(username=username, password=password)
	if user is not None: 
		if user.is_active:
			login(request, user)
			
			return myReservations(request)
		else: 
			errors.append("You need to verify your email before you can login")
			return render(request,'room_reservation_app/signin.html',context)
	else:
		errors.append("Username and Password do not match")
		return render(request,'room_reservation_app/signin.html',context)

# Delete an event based on id
@login_required
def deleteEvent(request, eventId):
  context = {}
  user = User.objects.get(username=request.user)
  try: 
  	event = Event.objects.get(id=eventId)
  except Event.DoesNotExist:
  	raise Http404
  if (event.user != user):
    raise Exception('User does not own event')
  event.delete()
  return render(request, 'room_reservation_app/my_reservations.html',context)
  

# View the events created by the logged in person
@login_required
def myReservations(request):
  #initialize()
  context = {}
  user = User.objects.get(username=request.user)
  events = Event.objects.filter(user=user)
  context["events"] = []
  eastern = timezone('US/Eastern')
  for event in events:
    title = event.name
    date = event.startTime.astimezone(eastern).strftime("%a %B %d, %Y")
    start = event.startTime.astimezone(eastern).strftime("%H:%M")
    end = event.endTime.astimezone(eastern).strftime("%H:%M")
    room = Room.objects.get(id = event.room_id)
    description = event.notes
    context["events"].append((title, date, start, end, room.name, description, event.id))
  return render(request,'room_reservation_app/my_reservations.html', context)

def initialize():
  building = Building(name='Gates-Hillman Center')
  building.save()
  room = Room(name='Rashid Auditorium', building=building, capacity=10)
  room.save()
  room = Room(name='4406', building=building, capacity=10)
  room.save()
  room = Room(name='7502', building=building, capacity=10)
  room.save()
  room = Room(name='7716', building=building, capacity=10)
  room.save()
  building = Building(name='Doherty')
  building.save()
  room = Room(name='2315', building=building, capacity=10)
  room.save()
  room = Room(name='2305', building=building, capacity=10)
  room.save()
  room = Room(name='2107', building=building, capacity=10)
  building = Building(name='Wean')
  building.save()
  room = Room(name='5213', building=building, capacity=10)
  room.save()
  room = Room(name='5214', building=building, capacity=10)
  room.save()
  room = Room(name='5312', building=building, capacity=10)
  room.save()
  room = Room(name='5318', building=building, capacity=10)
  room.save()
  room = Room(name='5310', building=building, capacity=10)
  room.save()

# Process the form for create a room reservation
@login_required
def saveEvent(request):
  context = {}
  start = request.POST.get("start", "")
  end = request.POST.get("end", "")
  date = request.POST.get("date", "")
  name = request.POST.get("name", "")
  description = request.POST.get("description", "")
  room_id = request.POST.get("room_id", "")
  building_id = request.POST.get("building_id", "")
  data = [start, end, date, name, description]
  # make sure all data is filled out
  for line in data:
    if (len(line) == 0):
      return redirect('/createReservation/')
  eastern = timezone('US/Eastern')
  startTime = eastern.localize(parser.parse(date + " " + start))
  endTime = eastern.localize(parser.parse(date + " " + end))
  # make sure it is valid timing
  if (startTime >= endTime): 
    return redirect("/createReservation/" + building_id + "/" + room_id + "/?warning=End time must be after the start time")
  if (startTime <= utc.localize(datetime.now())):
    return redirect("/createReservation/" + building_id + "/" + room_id + "/?warning=Reservation cannot be for a past time")
  # make sure the event does not conflict with any other event
  otherEvents = Event.objects.filter(startTime__gte=startTime, startTime__lt=endTime)
  if (len(otherEvents) > 0):
    return redirect("/createReservation/" + building_id + "/" + room_id + "/?warning=There is another event at this time")
  otherEvents = Event.objects.filter(endTime__gt=startTime, endTime__lte=endTime)
  if (len(otherEvents) > 0):
    return redirect("/createReservation/" + building_id + "/" + room_id + "/?warning=There is another event at this time")
  otherEvents = Event.objects.filter(startTime__lte=startTime, endTime__gte=endTime)
  if (len(otherEvents) > 0):
    return redirect("/createReservation/" + building_id + "/" + room_id + "/?warning=There is another event at this time")
  user = User.objects.get(username=request.user)
  room = Room.objects.get(id=room_id)
  event = Event(name=name, startTime=startTime, endTime=endTime, user=user, room=room, notes=description)
  event.save()
  return redirect('/myReservations/')

# Show the form for the room reservation. It will get room/building name as well as
# all events in that room so they can be seen in the calendar view
@login_required
def createReserveration(request, building_id, room_id):
  context = {}
  events = Event.objects.filter(room=room_id)
  building = Building.objects.get(id=building_id)
  room = Room.objects.get(id=room_id)
  context["building"] = building.name
  context["room"] = room.name
  eastern = timezone('US/Eastern')
  context["events"] = [(str(event.name), event.startTime.astimezone(eastern).strftime("%B %d, %Y %H:%M"), event.endTime.astimezone(eastern).strftime("%B %d, %Y %H:%M")) for event in events]
  context["room_id"] = room_id
  context["building_id"] = building_id
  context["warning"] = request.GET.get("warning", "")
  return render(request,'room_reservation_app/calendar.html', context)
  
# Will show the page where you will choose a building for your room reservation 
@login_required
def chooseBuilding(request):
  buildings = Building.objects.all() 
  context = {}
  context["title"] = "Choose a Building"
  context["options"] = {building.id : building.name for building in buildings}
  return render(request,'room_reservation_app/chooser.html', context)

# Will show the page where you will choose a room in the building that is 
# specified by the building id in the url so you can start your reservation
@login_required
def chooseRoom(request, building_id):
  rooms = Room.objects.filter(building=building_id)
  building = Building.objects.get(id=building_id)
  context = {}
  context["title"] = "Choose a Room in " + building.name
  context["options"] = {room.id : room.name for room in rooms}
  return render(request,'room_reservation_app/chooser.html', context)
