from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from models_app.factories import UserFactory, MediaItemFactory
from models_app.models import MediaItem
from config import proj_settings


class ListMediaItemsTest(APITestCase):
    NUM_PAGES = 3
    MEDIA_ITEMS_NUM = NUM_PAGES*proj_settings.get("PAGINATION.media_items", 10) # 3 pages of items

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('api:media_items')
        cls.user = UserFactory.create()
        cls.media_items = MediaItemFactory.create_batch(
            cls.MEDIA_ITEMS_NUM, 
            user=cls.user,
        )

    def setUp(self):
        self.client.force_login(self.user)
    
    def tearDown(self):
        self.client.logout()

    def test_get_media_items_no_params_200(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        self.assertEqual(response.data['total_count'], len(self.media_items))
        self.assertEqual(len(response.data['objects']), proj_settings.get("PAGINATION.media_items", 10))

    def test_get_media_items_some_params_200(self):
        PAGE = 2
        PER_PAGE = 4
        response = self.client.get(
            self.url,
            data={'page': PAGE, 'per_page': PER_PAGE, 'order': 'status'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        self.assertEqual(response.data['page'], PAGE)
        self.assertEqual(response.data['per_page'], PER_PAGE)
        self.assertEqual(len(response.data['objects']), PER_PAGE)
    
    def test_get_media_items_incorrect_order_400(self):
        response = self.client.get(
            self.url,
            data={'page': 2, 'per_page': 4, 'order': 'gibberish'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=f"Unexpected response: {response.data}"
        )
    
    def test_get_media_items_unathenticated_401(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )

        
class CreateMediaItemTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("api:media_items")
        cls.user = UserFactory.create()
        
    def setUp(self):
        self.client.force_login(self.user)
    
    def tearDown(self):
        self.client.logout()
        
    def test_post_media_items_success_201(self):
        response = self.client.post(
            self.url,
            data={"title": "TEST", "media_type": MediaItem.MediaType.GAME},
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f"Unexpected response: {response.data}"
        )
        
        # correct values on obj instance
        self.assertEqual(response.data['title'], 'TEST')
        self.assertEqual(response.data['media_type'], MediaItem.MediaType.GAME)
        
        # object actually exists in DB
        self.assertTrue(
            MediaItem.objects.filter(
                title='TEST',
                media_type=MediaItem.MediaType.GAME,
                user=self.user
                ).exists())
        
        # owner is assigned correctly
        item = MediaItem.objects.get(title='TEST')
        self.assertEqual(item.user, self.user)
        
    def test_post_media_items_missing_fields_400(self):
        response = self.client.post(
            self.url,
            data={"media_type": MediaItem.MediaType.GAME},
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=f"Unexpected response: {response.data}"
        )
    
    def test_post_media_items_incorrect_media_type_400(self):
        response = self.client.post(
            self.url,
            data={"media_type": "gibberish"},
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_post_media_items_unathenticated_401(self):
        self.client.logout()
        response = self.client.post(
            self.url,
            data={"title": "TEST", "media_type": MediaItem.MediaType.GAME},
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )