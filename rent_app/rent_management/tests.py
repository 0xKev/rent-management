
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rent_management.models import *
from rent_management.views import *
from rest_framework.test import force_authenticate



class UserTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="bobbert",
            email="bob@gmail.com"
        )

    def test_user_with_username_email_password(self):
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.username, "bobbert")
        self.assertEqual(self.user.email, "bob@gmail.com")
        

