from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import ForbiddenError, NotFound
from django.contrib.auth import get_user_model
from django import forms

from models_app.models import Tag, MediaItem    


class DeleteTag(ServiceWithResult):
    user =ModelField(get_user_model())
    tag = ModelField(Tag)    
    media_item_id = forms.IntegerField() #TODO: make it into list?
    
    custom_validations = ['_validate_user_is_owner_of_media_item']

    def process(self):
        # unbind mediaitems from tag
        self._unbind_tag_from_media_item()
        # count mediaitem_set on a tag
        # if it is empty, truly delete it
        self.result = self._delete_tag_if_unused()
        return self

    def _unbind_tag_from_media_item(self):
        tag: Tag = self.cleaned_data.get("tag")
        self.mi = self._get_media_item()
        self.run_custom_validations()
        tag.mediaitem_set.remove(self.mi)
    
    def _delete_tag_if_unused(self):
        tag: Tag = self.cleaned_data.get("tag")
        if tag.mediaitem_set.count() == 0:
            tag.delete()
            return True
        return False
    
    def _get_media_item(self) -> MediaItem:
        try:
            return MediaItem.objects.get(
                id=self.cleaned_data.get("media_item_id")
            )
        except MediaItem.DoesNotExist:
            self.add_error(
                "media_item_id",
                NotFound(message="MediaItem with given id does not exist.")
            )
            self.stop_process()

    def _validate_user_is_owner_of_media_item(self):
        if self.mi.user_id != self.cleaned_data.get("user").id:
            self.add_error("media_item_id", ForbiddenError("You are not an owner of MediaItem with provided ID"))
            self.stop_process()