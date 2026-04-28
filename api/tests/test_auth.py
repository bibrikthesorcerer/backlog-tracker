from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from models_app.factories import UserFactory


class RegisterUserTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("api:register")

    def test_register_user_success_200(self):
        response = self.client.post(
            self.url,
            {"username": "TEST", "password": "TESTPASS"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            get_user_model().objects.filter(username="TEST").exists()
        )

    def test_register_user_missing_data_400(self):
        response = self.client.post(
            self.url,
            {"username": "TEST"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class LoginUserTest(APITestCase):
    UNAME = "TEST"
    UPASS = "TEST123"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(username=cls.UNAME, set_pass=cls.UPASS)
        cls.postdata = {"username": cls.UNAME, "password": cls.UPASS}
        cls.url = reverse("api:login")
        
    def test_login_success_200(self):
        response = self.client.post(
            self.url,
            self.postdata,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.cookies.get("csrftoken"))
        self.assertIsNotNone(response.cookies.get("sessionid"))
        
    def test_login_incorrect_password_401(self):
        response = self.client.post(
            self.url,
            {"username": self.UNAME, "password": "123"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_login_user_does_not_exist_401(self):
        response = self.client.post(
            self.url,
            {"username": "GIBBERISH", "password": "123"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

class LogoutUserTest(APITestCase):
    UNAME = "TEST"
    UPASS = "TEST123"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(username=cls.UNAME, set_pass=cls.UPASS)
        cls.url = reverse("api:logout")
        
    def setUp(self):
        self.client.force_login(self.user)
        
    def test_logout_success_200(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout_no_user_200(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        