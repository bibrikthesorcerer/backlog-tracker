from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.contrib.auth import get_user_model
from django import forms
from service_objects.errors import NotFound, ForbiddenError

from models_app.models import Tag, MediaItem


class CreateTag(ServiceWithResult):
    user = ModelField(get_user_model())
    title = forms.CharField(max_length=64)
    media_item_id = forms.IntegerField() #TODO: make it into list?
    
    custom_validations = ['_validate_user_is_owner_of_media_item']
    
    def process(self):
        # get or create a tag instance
        self.result, _foo = Tag.objects.get_or_create(
            title=self.cleaned_data.get("title"),
            user=self.cleaned_data.get("user")
        )
        # bind it to a media_item
        self.mi = self._get_media_item()
        self.run_custom_validations()
        self.mi.tags.add(self.result)
        return self

    def _get_media_item(self) -> MediaItem:
        try:
            return MediaItem.objects.get(
                id=self.cleaned_data.get("media_item_id")
            )
        except MediaItem.DoesNotExist:
            self.add_error(
                "media_item_id",
                NotFound(message="MediaItem with given ID does not exist.")
            )
            self.stop_process()
            
    def _validate_user_is_owner_of_media_item(self):
        if self.mi.user_id != self.cleaned_data.get("user").id:
            self.add_error("media_item_id", ForbiddenError("You are not an owner of MediaItem with provided ID"))
            self.stop_process()