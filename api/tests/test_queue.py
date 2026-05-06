from rest_framework.test import APITestCase
from rest_framework import status
from typing import List
from django.utils import timezone
from django.urls import reverse
from factory import fuzzy

from models_app.models import MediaItem
from models_app.factories import UserFactory, MediaItemFactory


class MediaItemsQueueTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("api:queue")
            
    def setUp(self):
        self.user = UserFactory.create()
        self.client.force_login(self.user)

    def test_queue_success_200(self):
        items: List[MediaItem] = MediaItemFactory.create_batch(size=10, user=self.user, want=True)
        fuzzer = fuzzy.FuzzyDateTime(start_dt=timezone.now() - timezone.timedelta(weeks=1))
        for item in items:
            item.created_at = fuzzer.fuzz()
            item.save()

        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_queue_order_logic_days_since_creation_weight_200(self):
        user = UserFactory.create()
        item_old = MediaItemFactory.create(
            want=True, user=user,
            set_created_at=timezone.now()-timezone.timedelta(weeks=1),
            priority=MediaItem.PriorityLevel.VERY_HIGH
        )
        item_new = MediaItemFactory.create(
            want=True, user=user,
            set_created_at=timezone.now(),
            priority=MediaItem.PriorityLevel.VERY_HIGH
        )

        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [item['id'] for item in response.data]
        
        self.assertEqual(ids, [item_new.id, item_old.id])

    def test_queue_order_logic_priority_weight_200(self):
        item_high_priority = MediaItemFactory.create(
            want=True, user=self.user,
            set_created_at=timezone.now(),
            priority=MediaItem.PriorityLevel.HIGH
        )
        item_medium_priority = MediaItemFactory.create(
            want=True, user=self.user,
            set_created_at=timezone.now(),
            priority=MediaItem.PriorityLevel.MEDIUM
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [item['id'] for item in response.data]
        
        self.assertEqual(ids, [item_high_priority.id, item_medium_priority.id])

    def test_queue_items_with_status_not_want_excluded_200(self):
        MediaItemFactory.create_batch(size=10, user=self.user, in_progress=True)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_queue_items_with_no_priority_excluded_200(self):
        MediaItemFactory.create_batch(size=10, user=self.user, priority=None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_queue_unauthorized_401(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)