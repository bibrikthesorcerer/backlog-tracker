from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from models_app.factories import TagFactory, UserFactory, MediaItemFactory
from models_app.models import Tag
from api.serializers import ShowTagSerializer


class ListTagsTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create()
        cls.user_empty_tags = UserFactory.create()
        cls.user_tags = TagFactory.create_batch(5, user=cls.user)
        cls.other_tags = TagFactory.create_batch(5)
        cls.other_ids = {t.id for t in cls.other_tags}
        cls.url = reverse("api:tags")
        
    def test_get_tags_success_200(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        
        # check that all user's tags are in response
        self.assertEqual(
            response.data,
            ShowTagSerializer(self.user_tags, many=True).data 
        )
        
        # check that no other tags are in response
        response_ids = {t['id'] for t in response.data}
        self.assertTrue(response_ids.isdisjoint(self.other_ids))

        self.client.logout()
        
    def test_get_tags_empty_list_success_200(self):
        self.client.force_login(self.user_empty_tags)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        
        self.assertEqual(response.data, [])
        
    def test_get_tags_unauthenticated_401(self):
        response = self.client.get(self.url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )
    
        
class CreateTagsTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create()
        cls.other_user = UserFactory.create()
        cls.user_tags = TagFactory.create_batch(5, user=cls.user)
        cls.media_item = MediaItemFactory.create(user=cls.user)
        cls.url = reverse("api:tags")
        
    def setUp(self):
        self.client.force_login(self.user)
    
    def tearDown(self):
        self.client.logout()
        
    def test_create_tags_success_201(self):
        post_data = {"title": "TEST", "media_item_id": self.media_item.id}
        response = self.client.post(
            self.url,
            data=post_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f"Unexpected response: {response.data}"
        )
        
        # quick sanity check
        self.assertEqual(response.data["title"], post_data["title"])
        
        # check DB persistance
        self.assertTrue(
            Tag.objects.filter(
                title=post_data.get("title"),
                user=self.user
            ).exists()
        )
        
        # check tag binding to media_item
        tag = Tag.objects.get(id=response.data["id"])
        self.assertIn(self.media_item, tag.mediaitem_set.all())
        
    def test_create_tag_existing_title_new_binding_201(self):
        existing_tag = self.user_tags[0]
        new_media_item = MediaItemFactory.create(user=self.user)
        response = self.client.post(
            self.url,
            data={"title": existing_tag.title, "media_item_id": new_media_item.id},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # tag wasn't duplicated
        self.assertEqual(Tag.objects.filter(title=existing_tag.title, user=self.user).count(), 1)
        
        # but new binding was created
        self.assertIn(new_media_item, existing_tag.mediaitem_set.all())
        
    def test_create_tag_already_bound_to_media_item(self):
        existing_tag = self.user_tags[0]
        existing_tag.mediaitem_set.add(self.media_item)
        
        response = self.client.post(
            self.url,
            data={"title": existing_tag.title, "media_item_id": self.media_item.id},
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f"Unexpected response: {response.data}"
        )

        self.assertEqual(Tag.objects.filter(title=existing_tag.title, user=self.user).count(), 1)
        self.assertEqual(existing_tag.mediaitem_set.filter(id=self.media_item.id).count(), 1)

    def test_create_tags_media_item_empty_title_400(self):
        response = self.client.post(
            self.url,
            data={"title": "", "media_item_id": self.media_item.id},
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=f"Unexpected response: {response.data}"
        )

    def test_create_tags_unauthenticated_401(self):
        self.client.logout()
        response = self.client.post(
            self.url,
            data={"title": "TEST"},
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )

    def test_create_tag_for_other_users_media_item_403(self):
        other_media_item = MediaItemFactory.create(user=self.other_user)
        response = self.client.post(
            self.url,
            data={"title": "TEST", "media_item_id": other_media_item.id},
            content_type="application/json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unexpected response: {response.data}"
        )

    def test_create_tags_media_item_not_found_404(self):
        response = self.client.post(
            self.url,
            data={"title": "TEST", "media_item_id": 0},
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg=f"Unexpected response: {response.data}"
        )