from django.test import TestCase, Client
from django.contrib.auth.models import User
from labRatsApp.models import *
from datetime import date, timedelta
       

class CreateExperimentTestCase(TestCase):
	def setUp(self):
		c = Client()
		c.post('/register/', {'username':'testRat','password':'test','first_name':'Test','last_name':'Rat','email':'rat@test.com','title':'mr','phone':'012345','userType':'rat','school':'of hard rocks', 'age':21, 'sex':'m', 'firstLanguage':'binary', 'country':'RAMLand', 'educationLevel':'undergraduate','location':'Register TX2'})
		c.post('/register/', {'username':'testExperimenter','password':'test','first_name':'Test','last_name':'Experimenter','email':'experimenter@test.com','title':'mr','phone':'012345','userType':'experimenter'})
		
		
	def test_experimenter_creates(self):
		c = Client()
		response = c.post('/login/', {'username': 'testExperimenter', 'password': 'test'}, follow=True)
		self.assertEqual(response.status_code, 200)
		response = c.post('/experiment/create/', {'title': 'My Test Experiment', 'description':'A test description', 'max_participants':1, 'rewardType':'paid', 'rewardAmount':9001, 'date_start':'12/03/2014', 'date_end':'12/12/2014', 'ageMin':18, 'ageMax':20,'sex':' ',  	'firstLanguage':'binary', 'educationLevel':'undergraduate','location':'Scotland','tags':'test'}, follow=True)
		self.assertEqual(response.status_code, 200)
		
	def test_rat_creates(self):
		c = Client()
		response = c.post('/login/', {'username': 'testRat', 'password': 'test'}, follow=True)
		self.assertEqual(response.status_code, 200)
		response = c.get('/experiment/create/')
		
		self.assertEqual(response.status_code, 403)

		response = c.post('/experiment/create/', {'title': 'My Test Experiment', 'description':'A test description', 'max_participants':1, 'rewardType':'paid', 'rewardAmount':9001, 'date_start':'12/03/2014', 'date_end':'12/12/2014', 'ageMin':18, 'ageMax':20,'sex':' ', 'firstLanguage':'binary', 'educationLevel':'undergraduate','location':'Scotland','tags':'test'})
		print '-------------===---'
		print response
		print '-------------===---'
		self.assertEqual(response.status_code, 403)

	def test_modify_experiment_by_owner(self):
		c = Client()
		response = c.post('/login/', {'username': 'testExperimenter', 'password': 'test'}, follow=True)
		self.assertEqual(response.status_code, 200)
		#todo: wait for the bugfix
		
	def test_modify_experiment_by_stranger(self):
		c = Client()
		response = c.post('/login/', {'username': 'testExperimenter', 'password': 'test'}, follow=True)
		self.assertEqual(response.status_code, 200)
		#todo: wait for the bugfix

