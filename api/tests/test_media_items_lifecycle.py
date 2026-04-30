from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from models_app.models import MediaItem
from models_app.factories import MediaItemFactory, UserFactory


class MediaItemLifecycletest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create()
    
    def setUp(self):
        self.client.force_login(self.user)
    
    def tearDown(self):
        self.client.logout()
        
    def test_transition_to_in_progress_200(self):
        media_item = MediaItemFactory.create(user=self.user, want=True)
        response = self.client.post(
            reverse("api:start_media_item", args=[media_item.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            MediaItem.Status.IN_PROGRESS,
            MediaItem.objects.get(id=media_item.id).status
        )
        media_item.delete()
        
    def test_transition_to_completed_200(self):
        media_item = MediaItemFactory.create(user=self.user, in_progress=True)
        response = self.client.post(
            reverse("api:complete_media_item", args=[media_item.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            MediaItem.Status.COMPLETED,
            MediaItem.objects.get(id=media_item.id).status
        )
        media_item.delete()

    def test_transition_to_dropped_200(self):
        media_item = MediaItemFactory.create(user=self.user, in_progress=True)
        response = self.client.post(
            reverse("api:drop_media_item", args=[media_item.id])            
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            MediaItem.Status.DROPPED,
            MediaItem.objects.get(id=media_item.id).status
        )
        media_item.delete()

    def test_incorrect_transition_400(self):
        media_item = MediaItemFactory.create(user=self.user, want=True)
        response = self.client.post(
            reverse("api:complete_media_item", args=[media_item.id])            
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            MediaItem.Status.WANT,
            MediaItem.objects.get(id=media_item.id).status
        )

    def test_not_owner_403(self):
        other_user = UserFactory.create()
        media_item = MediaItemFactory.create(user=other_user, want=True)
        response = self.client.post(
            reverse("api:start_media_item", args=[media_item.id])            
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)