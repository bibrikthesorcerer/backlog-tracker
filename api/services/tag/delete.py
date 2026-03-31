from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from models_app.models import Tag    


class DeleteTag(ServiceWithResult):
    tag = ModelField(Tag)    
    
    def process(self):
        self.result = self.cleaned_data.get("tag").delete()
        return self