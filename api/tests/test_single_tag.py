from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from models_app.factories import UserFactory, TagFactory, MediaItemFactory
from models_app.models import Tag
from api.serializers import ShowTagSerializer


class ShowTagTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create()
        cls.users_tags = TagFactory.create_batch(5, user=cls.user)
        cls.tags = TagFactory.create_batch(5)
        
    def setUp(self):
        self.client.force_login(self.user)
        
    def tearDown(self):
        self.client.logout()
        
    def test_show_tag_success_200(self):
        response = self.client.get(
            reverse("api:single_tag", args=[self.users_tags[0].id])
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        
        # check that returned tag is the one we've requested
        self.assertEqual(
            response.data,
            ShowTagSerializer(self.users_tags[0]).data
        )

    def test_show_tag_unauthenticated_401(self):
        self.client.logout()
        response = self.client.get(
            reverse("api:single_tag", args=[self.users_tags[0].id])
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_show_tag_not_owner_403(self):
        other_tag = self.tags[0]
        response = self.client.get(
            reverse("api:single_tag", args=[other_tag.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unexpected response: {response.data}"
        )

    def test_show_tag_not_found_404(self):
        response = self.client.get(
            reverse("api:single_tag", args=[0])
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg=f"Unexpected response: {response.data}"
        )


class DeleteTagTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create()
        cls.other_user = UserFactory.create()

    def setUp(self):
        self.test_media_item = MediaItemFactory.create(user=self.user)
        self.test_tag = TagFactory.create(user=self.user, media_items=[self.test_media_item])
        self.url = reverse("api:single_tag", args=[self.test_tag.id])
        self.client.force_login(self.user)
        
    def tearDown(self):
        self.client.logout()
        
    def test_delete_tag_truly_delete_200(self):
        response = self.client.delete(
            self.url,
            data={"media_item_id": self.test_tag.mediaitem_set.first().id},
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        self.assertTrue(response.data["trulyDeleted"])

        self.assertFalse(
            Tag.objects.filter(id=self.test_tag.id).exists()
        )
        
    def test_delete_tag_just_unbind_200(self):
        # bind tag to new item
        new_media_item = MediaItemFactory.create(user=self.user)
        new_media_item.tags.add(self.test_tag)

        # and then unbind it
        delete_data = {"media_item_id": new_media_item.id}
        response = self.client.delete(
            self.url,
            data=delete_data,
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Unexpected response: {response.data}"
        )
        
        # check that deletion flag isnt set
        self.assertFalse(response.data["trulyDeleted"])

        # check that item wasnt deleted from DB
        self.assertTrue(
            Tag.objects.filter(id=self.test_tag.id).exists()
        )
        
        # check that tag is really unbinded from new media item
        self.assertNotIn(self.test_tag, new_media_item.tags.all())
        
    def test_delete_tag_no_media_item_id_400(self):
        response = self.client.delete(self.url, data={}, content_type="application/json")
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_delete_tag_unauthenticated_401(self):
        self.client.logout()
        response = self.client.delete(
            self.url,
            data={"media_item_id": self.test_tag.mediaitem_set.first().id},
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unexpected response: {response.data}"
        )
    
    def test_delete_tag_not_owner_of_media_item_403(self): # overhead
        other_users_media_item = MediaItemFactory.create(user=self.other_user)
        response = self.client.delete(
            self.url,
            data={"media_item_id": other_users_media_item.id},
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_delete_tag_not_owner_403(self):
        self.client.logout()
        self.client.force_login(self.other_user)
        response = self.client.delete(
            self.url,
            data={"media_item_id": self.test_tag.mediaitem_set.first().id},
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unexpected response: {response.data}"
        )
        
    def test_delete_tag_not_found_404(self):
        response = self.client.delete(
            reverse("api:single_tag", args=[0]),
            data={"media_item_id": self.test_tag.mediaitem_set.first().id},
            content_type="application/json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg=f"Unexpected response: {response.data}"
        )