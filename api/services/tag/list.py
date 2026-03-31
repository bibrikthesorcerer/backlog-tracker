from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from models_app.models import Tag    


class ListTags(ServiceWithResult):
    user = ModelField(get_user_model())
    
    def process(self):
        self.result = self._get_users_tags()
        return self

    def _get_users_tags(self):
        qs = Tag.objects.all()
        qs = self._filter_by_user(qs)
        return qs

    def _filter_by_user(self, qs:QuerySet):
        qs = qs.filter(
            user=self.cleaned_data.get("user")
        )
        return qs