from django.test import TestCase
from django.test import Client

class SanityCheck(TestCase):
	def setUp(self):
		self.client = Client()

	def test_details(self):
		response_admin = self.client.get('/admin/')
		self.assertEqual(response_admin.status_code, 200)

		response_create_res = self.client.get('/createReservation/')
		self.assertEqual(response_create_res.status_code, 200)

		response_create_res_1 = self.client.get('/createReservation/1/')
		self.assertEqual(response_create_res.status_code, 200)

		response_save_event = self.client.get('/saveEvent/')
		self.assertEqual(response_save_event.status_code, 200)

		response_my_res = self.client.get('/myReservations/')
		self.assertEqual(response_my_res.status_code, 200)

		response_delete_1 = self.client.get('/deleteEvent/1/')
		self.assertEqual(response_delete_1.status_code, 200)


#class EventTestCase(TestCase):
#	def Setup(self):
#		User.objects.create(firstName="Nora", lastName="Shoemaker", email="nora@mindcrafted.com", token=";afgkalkjfgkjaegkjdagrandom")
#		Building.objects.create(name="Gates")
#		Room.objects.create(name="4444", building=Building.objects.filter(name="Gates"), capacity=500)
#		Event.objects.create(name="TestEvent", startTime="9/20/14 4:30 PM", endTime="9/20/14 5:30 PM", user=User.objects.filter(email="nora@mindcrafted.com"), room=Room.objects.filter(name="4444"), notes="testnotes")
