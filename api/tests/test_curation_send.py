from rest_framework.test import APITestCase
from django.core import mail

from config import proj_settings
from api.tasks import send_single_curation_mail
from models_app.factories import UserFactory, MediaItemFactory


class EmailTaskTests(APITestCase):
    
    def test_single_curation_mail_success(self):
        user = UserFactory.create(email="user@example.com")
        queue_items = MediaItemFactory.create_batch(proj_settings.PAGINATION.queue_N, user=user, want=True) #queue
        started_item = MediaItemFactory.create(user=user, in_progress=True)
        send_single_curation_mail.apply(args=(user,))

        self.assertEqual(len(mail.outbox), 1)
        
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, "Your daily curation from Backlog")
        self.assertIn("user@example.com", sent_mail.to)
        self.assertIn(queue_items[0].title, sent_mail.body)
        self.assertIn(started_item.title, sent_mail.body)
