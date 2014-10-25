OpenSpace
=========

OpenSpace is a webapp designed to help you reserve rooms on campus.
![Alt text](Planning/ScreenShots/CreateReservation.png?raw=true "Reservation View")
-------------------------------------------------------------------------------

This is a project from a Software Development class. I worked on it with 4 other people. 
We had two weeks to plan, design, and implement the project.  
We had it deployed on aws but have since taken it down.

-------------------------------------------------------------------------------
Documentation
=============
This holds the user documentation for the app.

-------------------------------------------------------------------------------
Planning
=============
This holds the planning and design documents for the project.

-------------------------------------------------------------------------------
room_reservation app
================

Open Space Admin Guide (what to do if you want to run things locally):

Dependencies: MySQL, Django 1.7, Python 2.7 (make sure you set your PATH correctly)

To run test from the command prompt, go to the room_reservation folder and run:

python manage.py test

If you want to run the app locally from the command prompt, go to the room_reservation folder and (assuming you have connected your mysql database correctly in settings.py), run:

mysql –u
create database db_name
python manage.py syncdb
python manage.py runserver
In any browser go to: localhost:8000/myReservations/
