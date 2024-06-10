
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
        


class PropertyTests(APITestCase):
    
    def setUp(self):
        self.url = reverse("rent_management:property-api-list")
        self.user = CustomUser.objects.create_user(
            username="bobbert",
            email="bob@gmail.com",
            password="test_pw_bob"
        )

        self.client = APIClient(enforce_csrf_checks=False)
        self.client.login(username="bobbert", password="test_pw_bob")
        
        self.address = Address.objects.create(
            owner = self.user,
            country = "USA",
            state = "NY",
            city = "NYC",
            line1 = "123 Test Street",
            zipcode = 12345
        )

    def test_property_creation_with_all_details(self):
        """
        test_property_creation_with_all_details() returns True if property is created.
        """
        property_data = {
            'property_type': 'house',
            'name': 'Test House',
            'address': reverse("rent_management:address-api-detail", args=[self.address.pk]),
            'is_active': True,
            'description': 'Test description',
            'status': 'available',
            'payment_freq': 'monthly',
            'default_rent': 1000
        }

        request = self.client.post(self.url, property_data, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Property.objects.get().owner, self.user)
        self.assertEqual(Property.objects.get().address, self.address)
        self.assertEqual(Property.objects.get().property_type, "house")
        self.assertEqual(Property.objects.get().name, "Test House")
        self.assertEqual(Property.objects.get().is_active, True)