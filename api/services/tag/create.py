from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.contrib.auth import get_user_model
from django import forms

from models_app.models import Tag


class CreateTag(ServiceWithResult):
    user = ModelField(get_user_model())
    title = forms.CharField(max_length=64)
    
    def process(self):
        self.result = Tag.objects.get_or_create(
            title=self.cleaned_data.get("title"),
            user=self.cleaned_data.get("user")
        )
        return self