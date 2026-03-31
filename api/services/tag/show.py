from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import Tag    


class ShowTag(ServiceWithResult):
    id = forms.IntegerField()
    
    def process(self):
        self.result = Tag.objects.get(
            id=self.cleaned_data.get("id")
        )
        return self