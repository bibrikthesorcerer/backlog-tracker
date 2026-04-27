from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from models_app.models import MediaItem


class DeleteMediaItem(ServiceWithResult):
    media_item = ModelField(MediaItem)

    def process(self):
        self.cleaned_data.get("media_item").delete()
        return self