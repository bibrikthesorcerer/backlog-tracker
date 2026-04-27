from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from models_app.factories import UserFactory, MediaItemFactory
from models_app.models import MediaItem
from config import proj_settings


class ShowMediaItemTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_user = UserFactory.create()
        cls.media_items = MediaItemFactory.create_batch(
            proj_settings.PAGINATION.media_items, 
        )
        cls.mi_test = cls.media_items[0]
        cls.mi_owner = cls.mi_test.user
        cls.url = reverse('api:single_media_item', args=[cls.mi_test.id])


    def setUp(self):
        self.client.force_login(self.mi_owner)
    
    def tearDown(self):
        self.client.logout()
        
    def test_show_media_item_success_200(self):
        response = self.client.get(self.url) 
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        self.assertEqual(response.data['id'], self.mi_test.id)
        self.assertEqual(response.data['title'], self.mi_test.title)
        
    def test_show_media_item_unauthenticated_401(self):
        self.client.logout()
        response = self.client.get(self.url) 
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_show_media_item_not_owner_403(self):
        self.client.logout()
        self.client.force_login(self.other_user)
        response = self.client.get(self.url) 
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_show_media_item_not_found_404(self):
        response = self.client.get(
            reverse('api:single_media_item', args=[0])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg=f"Unexpected response: {response.data}"
        )

    
class UpdateMediaItemTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_user = UserFactory.create()
        cls.media_items = MediaItemFactory.create_batch(
            proj_settings.PAGINATION.media_items, 
        )
        cls.mi_test = cls.media_items[0] #NOTE: potential state bleeding. might move to setUp with refresh_from_db()
        cls.mi_owner = cls.mi_test.user
        cls.url = reverse('api:single_media_item', args=[cls.mi_test.id])


    def setUp(self):
        self.client.force_login(self.mi_owner)
    
    def tearDown(self):
        self.client.logout()
        
    def test_update_media_item_success_200(self):
        patch_data = {"title": "TEST_TITLE", "priority": MediaItem.PriorityLevel.VERY_HIGH}
        response = self.client.patch(
            self.url,
            data=patch_data,
            content_type="application/json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        
        # updated fields assertion
        self.assertEqual(response.data["title"], patch_data.get("title"))
        self.assertEqual(response.data["priority"], patch_data.get("priority"))
        
        # DB persistence assertion
        self.mi_test.refresh_from_db()
        self.assertEqual(self.mi_test.title, patch_data["title"])
        self.assertEqual(self.mi_test.priority, patch_data["priority"])
        
    def test_update_media_item_invalid_priority_400(self):
        response = self.client.patch(
            self.url,
            data={"priority": "not_a_valid_priority"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_media_item_unauthenticated_401(self):
        self.client.logout()
        response = self.client.patch(
            self.url,
            data={"title": "foo"},
            content_type="application/json"
        ) 
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_update_media_item_not_owner_403(self):
        self.client.logout()
        self.client.force_login(self.other_user)
        response = self.client.patch(
            self.url,
            data={"title": "foo"},
            content_type="application/json"
        ) 
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_update_media_item_not_found_404(self):
        response = self.client.patch(
            reverse('api:single_media_item', args=[0]),
            data={"title": "foo"},
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg=f"Unexpected response: {response.data}"
        )
        
class DeleteMediaItemTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_user = UserFactory.create()
        cls.media_items = MediaItemFactory.create_batch(
            proj_settings.PAGINATION.media_items, # decoys
        )
        
    def setUp(self):
        self.mi_test = MediaItemFactory.create()
        self.mi_owner = self.mi_test.user
        self.client.force_login(self.mi_owner)
        self.url = reverse('api:single_media_item', args=[self.mi_test.id])

    def tearDown(self):
        self.client.logout()

    def test_delete_media_item_success_204(self):
        response = self.client.delete(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg=f"Unexpected response: {response.data}"
        )
        
        # deletion persistent in DB
        self.assertFalse(
            MediaItem.objects.filter(id=self.mi_test.id).exists()
        )

    def test_delete_media_item_unauthenticated_401(self):
        self.client.logout()
        response = self.client.delete(self.url) 

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_delete_media_item_not_owner_403(self):
        self.client.logout()
        self.client.force_login(self.other_user)
        response = self.client.delete(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unexpected response: {response.data}"
        )

        self.assertTrue(MediaItem.objects.filter(id=self.mi_test.id).exists())
        
    def test_delete_media_item_not_found_404(self):
        response = self.client.delete(
            reverse("api:single_media_item", args=[0])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg=f"Unexpected response: {response.data}"
        )